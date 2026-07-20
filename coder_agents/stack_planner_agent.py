from service.llm import get_llm
from config.coder_agent_prompt import STACK_PLANNER_AGENT_PROMPT
from config.prompt import format_prompt
from rich import print


def Stack_planner(user_input):
    llm = get_llm()

    prompt = format_prompt(STACK_PLANNER_AGENT_PROMPT, user_query=user_input)

    response = llm.invoke(prompt).content
    print("response from Stack_planner agent", response)
    return {
        "event": "stack_planned",
        "message": response,
        "confidence": 1.0,
        "data": {"stack_plan": response}
    }
