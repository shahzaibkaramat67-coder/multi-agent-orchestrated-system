from service.llm import get_llm
from config.prompt import FINAL_RESPONDER_PROMPT, format_prompt
from rich import print


def final_responder(agent_output: str, critic_feedback):
    llm = get_llm()
    prompt = format_prompt(FINAL_RESPONDER_PROMPT, agent_output=agent_output, critic_feedback=critic_feedback)
    response = llm.invoke(prompt).content

    print("final responder agent :", response)

    return {
        "event": "final_response",
        "message": response,
        "confidence": 1.0,
        "data": {"response": response}
    }
