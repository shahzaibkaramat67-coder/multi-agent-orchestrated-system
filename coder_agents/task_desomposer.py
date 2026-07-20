from service.llm import get_llm
from config.coder_agent_prompt import TASK_DECOMPOSER_AGENT_PROMPT
from config.prompt import format_prompt


def TASK_DECOMPOSER_AGENT():
    llm = get_llm()

    prompt = format_prompt(TASK_DECOMPOSER_AGENT_PROMPT)

    response = llm.invoke(prompt).content

    return {
        "event": "task_decomposed",
        "message": response,
        "confidence": 1.0,
        "data": {"decomposition": response}
    }
