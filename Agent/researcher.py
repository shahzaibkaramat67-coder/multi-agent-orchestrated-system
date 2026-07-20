from service.llm import get_llm
from config.prompt import RESEARCHER_PROMPT, format_prompt
from Tools.research_agent_Tool.research import research
from rich import print


def researcher(user_input,critic_feedback):
    llm = get_llm()

    research_result = research(user_input)

    prompt = format_prompt(
        RESEARCHER_PROMPT,
        user_input=user_input, research_result=research_result, critic_feedback=critic_feedback
    )

    response = llm.invoke(prompt).content
    print("response researcher", response)

    return {
        "event": "research_completed",
        "message": response,
        "confidence": 1.0,
        "data": {"research": research_result, "response": response}
    }
