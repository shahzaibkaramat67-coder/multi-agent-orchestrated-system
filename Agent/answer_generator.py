from service.llm import get_llm
from config.prompt import ANSWER_GENERATOR_PROMPT, format_prompt
from rich import print


def answer_generator(user_input, critic_feedback):
    llm = get_llm()

    prompt = format_prompt(ANSWER_GENERATOR_PROMPT, user_input=user_input, critic_feedback=critic_feedback)

    response = llm.invoke(prompt).content
    print("response answer_generator :", response)

    return {
        "event": "answer_generated",
        "message": response,
        # "confidence": 1.0,
        "data": {"response": response}
    }
