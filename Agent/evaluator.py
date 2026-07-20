from service.llm import get_llm
from config.prompt import EVALUATOR_PROMPT, format_prompt
from rich import print


def evaluator(agent_output: str, user_input : str, critic_feedback : str):
    llm = get_llm()
    prompt = format_prompt(EVALUATOR_PROMPT, agent_output=agent_output, user_input=user_input, critic_feedback=critic_feedback)
    response = llm.invoke(prompt).content.strip()
    print("response evaluator :", response)

    return {
        "event": "evaluation_completed",
        "message": response,
        "confidence": 1.0,
        "data": {"evaluation": response}
    }
