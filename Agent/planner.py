from service.llm import get_llm
from config.prompt import REQUIREMENT_ANALYSIS_AGENT_PROMPT, format_prompt
from rich import print


def planner(user_input, history, critic_feedback):
    llm = get_llm()

    prompt = format_prompt(
        REQUIREMENT_ANALYSIS_AGENT_PROMPT,
        user_input=user_input,
        history=history,
        critic_feedback=critic_feedback
    )

    response = llm.invoke(prompt).content

    print("response planner", response)

    return {
        "event": "plan_created",
        "message": response,
        "confidence": 1.0,
        "data": {"plan": response}
    }
