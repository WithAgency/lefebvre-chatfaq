import asyncio
from logging import getLogger
from typing import List, NamedTuple, Text, Union

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from back.apps.broker.consumers.message_types import RPCNodeType
from back.apps.broker.models import ConsumerRoundRobinQueue
from back.apps.broker.models.message import StackPayloadType
from back.apps.language_model.models import RAGConfig, LLMConfig
from back.common.abs.bot_consumers import BotConsumer
from back.utils import WSStatusCodes

logger = getLogger(__name__)


class State(NamedTuple):
    """
    Attributes
    ----------
    name: str
        A human readable name for describing the state
    events: List of str
        A list of strings which are the function's names needed to be executed right after we enter the state
    initial: bool
        It defines the initial state, there should only be 1
    """

    name: Text
    events: List[Text] = []
    initial: bool = False


class Transition(NamedTuple):
    """
    Attributes
    ----------
    source: str
        'from' state
        If source = None then it describes a state that can be accessed from any other state,
        referred as an 'ubiquitous state'.
    dest: str
        'to' state
    conditions: List of str
        A list of strings which are the function's names needed to be executed to determine if we can enter the 'dest'
        state
    unless: List of str
        The same as conditions but considering the function with a 'not' operator in front of it
    """

    dest: Text
    source: Text = None
    conditions: List[Text] = []
    unless: List[Text] = []


class FSM:
    """
    FSM as in "Finite-State Machine".
    Bots are represented as an FSM: states are the various states of the bot.
    """

    channel_layer = get_channel_layer()

    def __init__(
        self,
        ctx: BotConsumer,
        states: List[State],
        transitions: List[Transition],
        current_state: State = None,
    ):
        """
        Parameters
        ----------
        ctx
            The connection context, usually useful to get the MML which triggered the state
        states
            They usually send messages to the user.
        transitions
            Contain the handlers and information that determines state changes.
        current_state
            It will usually be None when a new conversation a thus a new FSM starts. If the FSM come from a CachedFSM
            then it is when current_state is set to the cached current_state
        """
        from back.apps.broker.serializers.messages import MessageSerializer
        self.MessageSerializer = MessageSerializer

        self.last_aggregated_msg = {}
        self.ctx = ctx
        self.states = states
        self.transitions = transitions
        self.rpc_result_future: Union[asyncio.Future, None] = None

        self.current_state = current_state
        if not current_state:
            self.current_state = self.get_initial_state()

    async def start(self):
        await self.run_current_state_events()
        logger.debug(f"FSM start --> {self.current_state}")
        await self.save_cache()

    async def next_state(self):
        """
        It will cycle to the next state based on which transition returns a higher probability, once the next state
        is reached it makes sure everything is saved and cached into the DB to keep the system stateful
        """
        transitions = self.get_current_state_transitions()
        best_score = 0
        best_transition = None
        transition_data = {}
        for t in transitions:
            score, _data = await self.check_transition_condition(t)
            if score > best_score:
                best_transition = t
                best_score = score
                transition_data = _data
        if best_transition:
            logger.debug(f"FSM from ---> {self.current_state}")
            self.current_state = self.get_state_by_name(best_transition.dest)
            logger.debug(f"FSM to -----> {self.current_state}")
            await self.run_current_state_events(transition_data)
        await self.save_cache()

    async def run_current_state_events(self, transition_data=None):
        """
        It will call the RPC server, the procedure name is the event name declared in the fsm definition for the
        current state
        Parameters
        ----------
        transition_data: dict
            data coming from the result of the execution of the conditions. It might be useful for the state event, so
            we pass it along.
        """
        if transition_data is None:
            transition_data = {}

        for event_name in self.current_state.events:
            group_name = await database_sync_to_async(ConsumerRoundRobinQueue.get_next_consumer_group_name)(self.ctx.fsm_def.pk)

            data = {
                "type": "rpc_call",
                "status": WSStatusCodes.ok.value,
                "payload": {
                    "name": event_name,
                    "ctx": {
                        "transition_data": transition_data,
                        **(await self.ctx.serialize()),
                    },
                },
            }
            try:
                await self.channel_layer.group_send(group_name, data)
            except Exception as e:
                logger.error(f"Error while sending to RPC group {group_name}: {data}")
                raise e

    async def manage_rpc_response(self, data):
        """
        It will be called by the RPC Consumer when it receives a response from the RPC worker
        """
        if data["node_type"] == RPCNodeType.action.value:
            self.manage_last_llm_msg(data)
            id = await self.save_if_last_llm_msg(data)
            data["id"] = id
            await self.ctx.send_response(data)
        else:
            self.rpc_result_future.set_result(data)

    def manage_last_llm_msg(self, _new):
        _old = self.last_aggregated_msg
        if _new['stack'][0]["type"] in [StackPayloadType.llm_generated_text.value, StackPayloadType.rag_generated_text.value]:
            if _new["stack_id"] == _old.get("stack_id"):
                more_model_response = _new["stack"][0]['payload']['model_response']
                old_payload = _old["stack"][0]['payload']
                _new["stack"][0]['payload']['model_response'] = old_payload['model_response'] + more_model_response
        self.last_aggregated_msg = _new

    async def save_if_last_llm_msg(self, _new):
        if self.last_aggregated_msg.get("last"):
            if self.last_aggregated_msg['stack'][0]["type"] == StackPayloadType.rag_generated_text.value:
                rag_config_id = (await database_sync_to_async(RAGConfig.objects.get)(name=self.last_aggregated_msg['stack'][0]['payload']['rag_config_name'])).id
                self.last_aggregated_msg['stack'][0]['payload']["rag_config_id"] = rag_config_id

            elif self.last_aggregated_msg['stack'][0]['type'] == StackPayloadType.llm_generated_text.value:
                llm_config_id = (await database_sync_to_async(LLMConfig.objects.get)(name=self.last_aggregated_msg['stack'][0]['payload']['llm_config_name'])).id
                self.last_aggregated_msg['stack'][0]['payload']["llm_config_id"] = llm_config_id

            self.last_aggregated_msg["conversation"] = self.last_aggregated_msg["ctx"]["conversation_id"]
            serializer = self.MessageSerializer(data=self.last_aggregated_msg)
            print('>'*100)
            print(self.last_aggregated_msg)
            print('<'*100)
            await database_sync_to_async(serializer.is_valid)(raise_exception=True)
            return (await database_sync_to_async(serializer.save)()).id

    def get_initial_state(self):
        for state in self.states:
            if state.initial:
                return state
        raise Exception("There must be an initial state")

    def get_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state

    def get_current_state_transitions(self):
        return filter(
            lambda t: t.source == self.current_state.name or t.source is None,
            self.transitions,
        )

    async def check_transition_condition(self, transition):
        """
        For a transition it will compute its score based on all its conditions
        """
        max_score = 0 if transition.conditions else 1
        data = {}
        for condition_name in transition.conditions:
            score, _data = await self.run_condition(condition_name)
            if score > max_score:
                max_score = score
                data = _data

        un_max_score = 0
        for condition_name in transition.unless:
            score, _ = await self.run_condition(condition_name)
            if score > un_max_score:
                un_max_score = score

        return max_score - un_max_score, data

    async def run_condition(self, condition_name):
        """
        It will call the RPC server, 'condition_name' is the procedure the remote server should run
        Then it will wait util the response is back into the database
        Parameters
        ----------
        condition_name: str
            Name of the remote procedure to call

        Returns
        -------
        tuple[float, dict]
            The first float indicates the score, the returning dictionary is the result of the RPC

        """
        group_name = await database_sync_to_async(ConsumerRoundRobinQueue.get_next_consumer_group_name)(self.ctx.fsm_def.pk)

        data = {
            "type": "rpc_call",
            "status": WSStatusCodes.ok.value,
            "payload": {"name": condition_name, "ctx": await self.ctx.serialize()},
        }
        await self.channel_layer.group_send(group_name, data)
        self.rpc_result_future = asyncio.get_event_loop().create_future()
        logger.debug(f"Waiting for RCP call {condition_name} (condition)...")
        payload = await self.rpc_result_future
        logger.debug(f"...Receive RCP call {condition_name} (condition)")
        return payload["stack"]["score"], payload["stack"]["data"]

    async def save_cache(self):
        from back.apps.fsm.models import CachedFSM  # TODO: Resolve CI

        await database_sync_to_async(CachedFSM.update_or_create)(self)
