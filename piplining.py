from orchestrated_agent import Orchestrated
from router.route import selectAgent
from Agent.critic import critic
from Agent.evaluator import evaluator
from Agent.final_reponder import final_responder
from Agent.orch_coder_agent import CODING_ORCHESTRATOR
from router.route import selectAgent_for_coding
from coder_agents.solve_error_agent import solve_error_agent
from State.state_agent import AgentState
from router.route import query_rewriter
from State.state_agent import AgentMessage
from datetime import datetime

# from State.update_state import update_state


def run(user_input):

    state = AgentState(user_query=user_input)
    iteration_count = 0
    max_iteration_count = 10

    while not state.task_complete and iteration_count < max_iteration_count:
        iteration_count +=1
        # user_query = state.user_query
        # history = state.history
        # context = state.context
        # agent = state.current_agent

        # 1. Orchestrator decides next agent
        selected_agent = Orchestrated(state.user_query, state.history, state.context)
        if selected_agent == "finished":
            state.task_complete = True
            break
       
        # return final_responder_result

        print("selected_agent by orchestrator agent", selected_agent)

        # handle orchestrator FINISHED signal (LLM may return 'finished')

        # 2. NORMAL AGENTS
        if selected_agent != "orch_coder_agent":
            state.current_agent = selected_agent

            agent_result = selectAgent(
                state.current_agent, state.user_query, state.history
            )

            print("agent_result", agent_result["message"])
            
            critic_result = critic(agent_result["message"], user_input)
            print("critic_result : ",critic_result)
            while critic_result == "FAIL":
                return selectAgent(
                state.current_agent, state.user_query, state.history, critic_result
            )
                
            evaluator_result = evaluator(agent_result["message"], user_input, critic_result)
            if evaluator_result == "PASS":
                state.task_complete = True
                final_responder_result = final_responder(evaluator_result)
               
            
                print("this is agent_result", agent_result)
                state.context[state.current_agent] = final_responder_result

                state.history.append(
                    AgentMessage(
                        timestamp=datetime.now().isoformat(),
                        agent=state.current_agent,
                        event=agent_result["event"],
                        message=agent_result["message"],
                        confidence=agent_result.get("confidence", 1.0),
                        data=agent_result["data"],
                    )
                )
               
                # break;

            # state.history.append({"Agent": state.current_agent, "Result": agent_result})
                state.final_response = agent_result
            Orchestrated(state.user_query, state.history, state.context)
    
        else:
            coding_agent_name = CODING_ORCHESTRATOR(
                state.user_query, state.history, state.context
            )
            print("coding_agent_name form coding agent", coding_agent_name)
            if coding_agent_name == "finished":
                state.task_complete = True
                break
            state.next_agent = coding_agent_name
            agent_result = selectAgent_for_coding(state)

            print("this is agent_result", agent_result)

            state.context[state.next_agent] = agent_result

            state.history.append(
                AgentMessage(
                    timestamp=datetime.now().isoformat(),
                    agent=state.next_agent,
                    event=agent_result["event"],
                    message=agent_result["message"],
                    confidence=agent_result.get("confidence", 1.0),
                    data=agent_result["data"],
                )
            )
            state.final_response = agent_result
    return state.final_response

    # optional stop for simple responses
    # if selected_agent == "answer_generator":
    #     state.final_response = agent_result
    #     state.task_complete = True
    #     break

    # 3. CODING SYSTEM

    # if not state.stack_plan or len(state.stack_plan) == 0:
    #     stack_Coding_agent_name = "stack_planner_agent"
    #     stack_Coding_agent_result = selectAgent_for_coding(
    #         stack_Coding_agent_name, state
    #     )

    #     print("Coding_agent_result", stack_Coding_agent_result)

    #     state.stack_plan = stack_Coding_agent_result

    #     state.history.append(
    #         {
    #             "Agent": stack_Coding_agent_name,
    #             "Result": stack_Coding_agent_result,
    #         }
    #     )
    #     update_state(stack_Coding_agent_name, stack_Coding_agent_result, state)

    # else:
    #     Coding_agent_name = CODING_ORCHESTRATOR(state)

    #     Coding_agent_result = selectAgent_for_coding(Coding_agent_name, state)

    #     state.history.append(
    #         {
    #             "Agent": "orch_coder_agent",
    #             "sub_Agent": Coding_agent_name,
    #             "Result": Coding_agent_result,
    #         }
    #     )

    #     update_state(Coding_agent_name, Coding_agent_result, state)

    #     # optional: if coding is done
    # if state.task_complete:
    #     break

    # return state
    # state.current_agent = agent_name
    # # orch_coder_agent
    # print("agent_name", agent_name)
    # if state.current_agent == "orch_coder_agent":
    #     Sub_agent_name = CODING_ORCHESTRATOR(state.user_query)
    #     state.Next_agent = Sub_agent_name
    #     print("Sub_agent_name", Sub_agent_name)
    #     Sub_code_agent_result = selectAgent_for_coding(
    #         state.Next_agent, state.user_query
    #     )
    #     state.history.append(
    #         {"agent": state.Next_agent, "response": Sub_code_agent_result}
    #     )
    #     Sub_review = code_executor_Tool(state.history["response"])
    #     state.review_result = Sub_review["status"]
    #     while not state.review_result == "success":
    #         fixed_code = solve_error_agent(
    #             # error=Sub_review["stderr"], code=Sub_review["stdout"]
    #             state.execution_error = Sub_review["stderr"], state.execution_output = Sub_review["stdout"]
    #         )
    #         code_executor_Tool(fixed_code)
    #     # selectAgent_for_coding(Sub_review["stderr"])

    #     Sub_score = evaluator(Sub_code_agent_result)
    #     Sub_final_output = final_responder(Sub_code_agent_result)
    #     return {
    #         "agent": agent_name,
    #         "Sub_agent_name": Sub_agent_name,
    #         "agent_result": Sub_code_agent_result,
    #         "Sub_review": Sub_review,
    #         "Sub_score": Sub_score,
    #         "Sub_final_output": Sub_final_output,
    #     }

    # agent_result = selectAgent(agent_name, user_input)
    # print("agent_result", agent_result)
    # review = critic(agent_result)
    # score = evaluator(agent_result)
    # final_output = final_responder(agent_result)

    # return {
    #     "agent": agent_name,
    #     "agent_result": agent_result,
    #     "review": review,
    #     "score": score,
    #     "final_output": final_output,
    # }


# ufoefboebfioengfie


# from orchestrated_agent import Orchestrated
# from router.route import selectAgent
# from Agent.critic import critic
# from Agent.evaluator import evaluator
# from Agent.final_reponder import final_responder
# from Agent.orch_coder_agent import CODING_ORCHESTRATOR
# from router.route import selectAgent_for_coding
# from Tools.coder_Tool.code_executor_Tool import code_executor_Tool
# from coder_agents.solve_error_agent import solve_error_agent
# from State.state_agent import AgentState
# from State.update_state import update_state


# def run(user_input):

#     state = AgentState(user_query=user_input)

#     while not state.task_complete:

#         # 1. Orchestrator decides next agent
#         selected_agent = Orchestrated(state)

#         print("selected_agent by orchestrator agent", selected_agent)

#         state.current_agent = selected_agent
#         # handle orchestrator FINISHED signal (LLM may return 'finished')
#         # if selected_agent == "finished":
#         #     state.task_complete = True
#         #     break

#         # 2. NORMAL AGENTS
#         if selected_agent != "orch_coder_agent":

#             agent_result = selectAgent(state)

#             state.history.append({"Agent": selected_agent, "Result": agent_result})

#             # optional stop for simple responses
#             # if selected_agent == "answer_generator":
#             #     state.final_response = agent_result
#             #     state.task_complete = True
#             #     break

#         # 3. CODING SYSTEM
#         else:

#             if not state.stack_plan or len(state.stack_plan) == 0:
#                 stack_Coding_agent_name = "stack_planner_agent"
#                 stack_Coding_agent_result = selectAgent_for_coding(
#                     stack_Coding_agent_name, state
#                 )

#                 print("Coding_agent_result", stack_Coding_agent_result)

#                 state.stack_plan = stack_Coding_agent_result

#                 state.history.append(
#                     {
#                         "Agent": stack_Coding_agent_name,
#                         "Result": stack_Coding_agent_result,
#                     }
#                 )
#                 update_state(stack_Coding_agent_name, stack_Coding_agent_result, state)

#             else:
#                 Coding_agent_name = CODING_ORCHESTRATOR(state)

#                 Coding_agent_result = selectAgent_for_coding(Coding_agent_name, state)

#                 state.history.append(
#                     {
#                         "Agent": "orch_coder_agent",
#                         "sub_Agent": Coding_agent_name,
#                         "Result": Coding_agent_result,
#                     }
#                 )

#                 update_state(Coding_agent_name, Coding_agent_result, state)

#                 # optional: if coding is done
#             if state.task_complete:
#                 break

#     return state
