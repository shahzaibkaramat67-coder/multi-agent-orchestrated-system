from service.llm import get_llm

# from service.llm import coder_llm
from rich import print

from config.coder_agent_prompt import CODE_GENERATOR_AGENT_PROMPT


def code_generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(CODE_GENERATOR_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response code_generator_agent :", response)

    return {
        "event": "code_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"code": response}
    }
