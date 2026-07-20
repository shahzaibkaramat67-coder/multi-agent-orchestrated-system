from service.llm import get_llm
from config.coder_agent_prompt import PROJECT_ARCHITECTURE_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Project_Architect_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(PROJECT_ARCHITECTURE_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Project_Architect_agent :", response)

    return {
        "event": "architecture_designed",
        "message": response,
        "confidence": 1.0,
        "data": {"architecture": response}
    }
