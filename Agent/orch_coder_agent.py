from service.llm import get_llm
from config.prompt import CODING_ORCHESTRATOR_AGENT_PROMPT, format_prompt
from rich import print


def CODING_ORCHESTRATOR(user_query, history, context):
    llm = get_llm()

    prompt = format_prompt(
        CODING_ORCHESTRATOR_AGENT_PROMPT,
        user_query=user_query,
        history=history,
        context=context,
        # architecture=state.architecture,
        # generated_code=state.generated_code,
        # execution_error=state.execution_error,
        # task_complete=state.task_complete,
        # stack_plan=state.stack_plan,
        # execution_output=state.execution_output,
        # review_result=state.review_result,
        # test_cases=state.test_cases,
    )

    response = llm.invoke(prompt).content

    print("response CODING_ORCHESTRATOR", response)
    return response
