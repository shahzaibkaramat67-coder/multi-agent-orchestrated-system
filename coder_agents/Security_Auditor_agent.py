from service.llm import get_llm
from config.coder_agent_prompt import SECURITY_AUDITOR_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Security_Auditor_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(SECURITY_AUDITOR_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Security_Auditor_agent :", response)

    return {
        "event": "security_audited",
        "message": response,
        "confidence": 1.0,
        "data": {"security_report": response}
    }
