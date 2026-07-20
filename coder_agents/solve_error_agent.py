from service.llm import get_llm

# from service.llm import coder_llm

from config.coder_agent_prompt import SOLVE_ERROR_AGENT_PROMPT
from rich import print


def solve_error_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(SOLVE_ERROR_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response solve_error_agent :", response)

    return {
        "event": "error_solved",
        "message": response,
        "confidence": 1.0,
        "data": {"solution": response}
    }
