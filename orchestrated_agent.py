from service.llm import get_llm
from config.prompt import Orchestrator_agent_prompt, format_prompt


def Orchestrated(user_query, history, context):
    print("decision this is from orchestrator function")
    llm = get_llm()

    prompt = format_prompt(
        Orchestrator_agent_prompt,
        user_input=user_query,
        history=history,
        context=context,
        # stack_plan=state.stack_plan,
        # architecture=state.architecture,
        # generated_code=state.generated_code,
        # execution_output=state.execution_output,
        # execution_error=state.execution_error,
        # review_result=state.review_result,
        # security_report=state.security_report,
        # test_cases=state.test_cases,
        # documentation=state.documentation,
        # final_response=state.final_response,
    )
    response = llm.invoke(prompt).content.strip().lower()

    print("decision by Orchestrated agent", response)

    return response


# from service.llm import get_llm
# from config.prompt import Orchestrator_agent_prompt


# def Orchestrated(user_input):
#     Orchestrator_agent_prompt(user_input)
#     get_llm()
