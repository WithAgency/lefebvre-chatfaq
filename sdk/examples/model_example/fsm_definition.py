import random

from chatfaq_sdk.fsm import FSMDefinition, State, Transition
from chatfaq_sdk.layers import LMGeneratedText, Text


def send_greeting(ctx: dict):
    yield Text("Hello! How are you?")
    yield Text("I'm a chatbot for With Madrid. I can answer your questions about our website and its content.")
    yield Text("Feel free to ask me anything you need assistance with!", allow_feedback=False)


def send_answer(ctx: dict):
    last_payload = ctx["last_mml"]["stack"][0]["payload"]
    yield LMGeneratedText(last_payload, 1)
    yield Text(f"Tell me more")


greeting_state = State(name="Greeting", events=[send_greeting], initial=True)

answering_state = State(
    name="Answering",
    events=[send_answer],
)

_to_answer = Transition(
    dest=answering_state,
)

fsm_definition = FSMDefinition(
    states=[greeting_state, answering_state],
    transitions=[_to_answer],
    pre_load_models=[1],
)
