from service.llm import get_llm
from config.prompt import QUERY_REWRITER_PROMPT, format_prompt
from rich import print


def query_rewriter(user_input, critic_feedback):
    llm = get_llm()

    prompt = format_prompt(QUERY_REWRITER_PROMPT, user_input=user_input, critic_feedback=critic_feedback)

    response = llm.invoke(prompt).content
    print("response query_rewriter", response)

    return {
        "event": "query_rewritten",
        "message": response,
        "confidence": 1.0,
        "data": {"rewritten_query": response}
    }
