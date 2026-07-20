from service.llm import get_llm
from config.coder_agent_prompt import DOCUMENTATION_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Documentation_Agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(DOCUMENTATION_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Documentation_Agent :", response)

    return {
        "event": "documentation_created",
        "message": response,
        "confidence": 1.0,
        "data": {"documentation": response}
    }
