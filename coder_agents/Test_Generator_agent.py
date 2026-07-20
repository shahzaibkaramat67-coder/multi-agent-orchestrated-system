from service.llm import get_llm
from config.coder_agent_prompt import TEST_GENERATOR_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Test_Generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = format_prompt(TEST_GENERATOR_AGENT_PROMPT, user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Test_Generator_agent :", response)

    return {
        "event": "tests_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"test_cases": response}
    }
