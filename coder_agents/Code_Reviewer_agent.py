from service.llm import get_llm
from config.coder_agent_prompt import CODE_REVIEW_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Code_Reviewer_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(CODE_REVIEW_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Code_Reviewer_agent :", response)

    return {
        "event": "code_reviewed",
        "message": response,
        "confidence": 1.0,
        "data": {"review": response}
    }
