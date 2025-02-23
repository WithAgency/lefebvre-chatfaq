import os
from chat_rag.llms.base_llm import LLM
from chat_rag.llms.claude_client import ClaudeChatModel
# from chat_rag.llms.hf_llm import HFModel
from chat_rag.llms.mistral_client import MistralChatModel
from chat_rag.llms.openai_client import OpenAIChatModel
from chat_rag.llms.vllm_client import VLLMModel
from chat_rag.llms.gemini_client import GeminiChatModel
from chat_rag.llms.format_tools import format_tools, Mode


__all__ = [
    "LLM",
    "OpenAIChatModel",
    "VLLMModel",
    "ClaudeChatModel",
    "MistralChatModel",
    "GGMLModel",
    "HFModel",
    "format_tools",
]


LLM_CLASSES = {
    "claude": ClaudeChatModel,
    "mistral": MistralChatModel,
    "openai": OpenAIChatModel,
    "vllm": VLLMModel,
    "together": OpenAIChatModel,
    "gemini": GeminiChatModel,
}

def load_llm(llm_type: str, llm_name: str, base_url: str = None, model_max_length: int = None, api_key: str = None) -> LLM:
    
    # For Together model, set the fixed TOGETHER url
    if llm_type == "together":
        base_url = "https://api.together.xyz/v1"
        api_key = os.environ.get("TOGETHER_API_KEY")

    llm = LLM_CLASSES[llm_type](
        llm_name, base_url=base_url, api_key=api_key, model_max_length=model_max_length,
    )
    return llm
