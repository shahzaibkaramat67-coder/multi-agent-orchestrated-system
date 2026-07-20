from Agent.orch_coder_agent import CODING_ORCHESTRATOR
from Agent.answer_generator import answer_generator
from Agent.researcher import researcher
from Agent.query_rewritter import query_rewriter
from Agent.planner import planner
# from Tools.coder_Tool.code_executor_Tool import code_executor_Tool
from coder_agents.code_generator_agent import code_generator_agent
from coder_agents.Code_Reviewer_agent import Code_Reviewer_agent
from coder_agents.Documentation_Agent import Documentation_Agent
from coder_agents.Project_Architect_agent import Project_Architect_agent
from coder_agents.Security_Auditor_agent import Security_Auditor_agent
from coder_agents.Test_Generator_agent import Test_Generator_agent
from coder_agents.solve_error_agent import solve_error_agent
from coder_agents.stack_planner_agent import Stack_planner


def selectAgent(agent, user_query, history, critic_result=None):

    print("that is state from the router for selectAgent", agent)

    # agent = state.current_agent
    # history = state.history
    # user_input = state.user_query

    if agent == "orch_coder_agent":
        return CODING_ORCHESTRATOR(user_input=user_query, history=history)

    elif agent == "researcher":
        return researcher(user_input=user_query, critic_feedback=critic_result)

    elif agent == "query_rewriter":
        return query_rewriter(user_input=user_query, critic_feedback=critic_result)

    elif agent == "planner":
        return planner(user_input=user_query, history=history, critic_feedback=critic_result)

    else:
        return answer_generator(user_input=user_query,critic_feedback=critic_result)


def selectAgent_for_coding(state):
    Result = state.history
    agent = state.next_agent
    user_input = state.user_query
    if agent == "code_generator_agent":
        return code_generator_agent(state.user_query)

    # elif agent == "code_executor_Tool":
    #     return code_executor_Tool(user_input, Result)

    elif agent == "stack_plan":
        return Stack_planner(state.user_query)

    elif agent == "Project_Architect_agent":
        return Project_Architect_agent(state.user_query)

    elif agent == "solve_error_agent":
        return solve_error_agent(state.user_query)

    elif agent == "Code_Reviewer_agent":
        return Code_Reviewer_agent(state.user_query)

    elif agent == "Security_Auditor_agent":
        return Security_Auditor_agent(state.user_query)

    elif agent == "Test_Generator_agent":
        return Test_Generator_agent(state.user_query)

    elif agent == "Documentation_Agent":
        return Documentation_Agent(state.user_query)
    else:
        return {
            "event": "error",
            "message": f"Unknown coding agent: {agent}",
            "confidence": 0.0,
            "data": {"error": "unknown_agent"}
        }


# def language_executor():
#     print("language executer route")


# def selectAgent_for_coding(state):
#     """Normalize agent names and update the shared AgentState accordingly."""
#     # name = str(agent_name).lower()
#     name = (state.current_agent,)
#     result = state.history[-1]["Result"]

#     if name == "code_generator_agent":
#         state.generated_code = result

#     elif name == "solve_error_agent":
#         state.execution_error = result

#     elif "code_executor" in name:
#         state.execution_output = result

#     elif "code_reviewer" in name:
#         state.review_result = result

#     elif "security" in name or "security_auditor" in name:
#         state.security_report = result

#     elif "test_generator" in name or name.startswith("test"):
#         state.test_cases = result

#     elif "document" in name or "documentation" in name:
#         state.documentation = result

#     elif "stack" in name or name == "stack_planner_agent" or name == "stack_plan":
#         state.stack_plan = result

#     else:
#         print(f"[WARN] Unknown agent state update: {name}")

#     return state
