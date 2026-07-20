from service.llm import get_llm
from config.prompt import CRITIC_PROMPT, format_prompt
from rich import print


def critic(agent_result: str, user_input: str):
    llm = get_llm()
    prompt = format_prompt(CRITIC_PROMPT, agent_output=agent_result, user_input=user_input)
    response = llm.invoke(prompt).content.strip().lower()

    print("response critic :", response)
    
    return response 
    # return {
    #     "event": "critique_completed",
    #     "message": response,
    #     "confidence": 1.0,
    #     "data": {"critique": response}
    # }
