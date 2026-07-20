# Multi-Agent Orchestration System Design

## 1. Overview

This project implements a multi-agent orchestration system for software development tasks. There are two levels of orchestration:

- **Main Orchestrator**: decides the high-level next step and whether the request should go to planning, research, coding, query rewriting, or answer generation.
- **Coding Orchestrator**: handles the software engineering workflow and selects the correct coding sub-agent, including the programming language and execution tool.

The user flow is:

1. User input enters `main.py`.
2. `piplining.py` creates `AgentState` and loops until completion.
3. `orchestrated_agent.py` decides the next top-level agent.
4. If coding is needed, `Agent/orch_coder_agent.py` decides the coding specialist and language path.
5. A code executor tool runs code when requested.
6. Final response is returned to the user.

## 2. Agents and Roles

### 2.1 Main Orchestrator

File: `orchestrated_agent.py`

Role:
- Decide routing based on the full shared state.
- Return one of: `planner`, `query_rewriter`, `researcher`, `orch_coder_agent`, `answer_generator`, or `FINISHED`.
- Do not write code or perform deep planning.

State used by the prompt:
- `user_query`
- `current_agent`
- `next_agent`
- `task_complete`
- `history`

Missing requirements:
- It should also get full lifecycle fields like `stack_plan`, `generated_code`, `execution_error`, `execution_output`, `review_result`, `security_report`, `test_cases`, and `documentation` when routing.

### 2.2 Coding Orchestrator

File: `Agent/orch_coder_agent.py`

Role:
- Coordinate the next coding step for software development tasks.
- Choose among coding specialists and tools.
- Do not generate code itself.

Sub-agents it should select:
- `Project_Architect_agent`
- `code_generator_agent`
- `solve_error_agent`
- `Code_Reviewer_agent`
- `Security_Auditor_agent`
- `Test_Generator_agent`
- `Documentation_Agent`
- `code_executor_Tool`

Current prompt input:
- `user_query`
- `architecture`
- `generated_code`
- `execution_error`
- `task_complete`
- `stack_plan`
- `execution_output`
- `review_result`
- `test_cases`

Missing / recommended additions:
- `history`
- `documentation`
- explicit `language` or `stack_plan` fields describing the implementation language and framework preferences.

### 2.3 Support Agents

These agents are not orchestrators but are used for output, evaluation, or quality control:

- `Agent/answer_generator.py`: general chat/knowledge responses.
- `Agent/critic.py`: critique agent outputs.
- `Agent/evaluator.py`: evaluate an agent result.
- `Agent/final_reponder.py`: produce the final formatted answer.

These are support tools and do not directly decide routing.

### 2.4 Normal Agents

Active agent functions in `router/route.py`:
- `planner`
- `query_rewriter`
- `researcher`
- `Project_Architect_agent`
- `code_generator_agent`
- `solve_error_agent`
- `Code_Reviewer_agent`
- `Security_Auditor_agent`
- `Test_Generator_agent`
- `Documentation_Agent`

Missing requirement:
- All agents that depend on conversation history should receive `state.history` explicitly.

## 3. Shared State Model

File: `State/state_agent.py`

`AgentState` fields:
- `user_query`
- `current_agent`
- `next_agent`
- `task_complete`
- `history`
- `architecture`
- `stack_plan`
- `generated_code`
- `execution_output`
- `execution_error`
- `review_result`
- `security_report`
- `test_cases`
- `documentation`
- `final_response`

Important notes:
- `task_complete` must be explicitly set when the workflow finishes.
- `final_response` should store the ultimate user answer.
- `next_agent` should be the output of the coder orchestrator, not an input to it.

## 4. Current Flow and Missing Pieces

### 4.1 Current `piplining.py` flow

1. Create state: `state = AgentState(user_query=user_input)`.
2. Loop while `not state.task_complete`.
3. Call `Orchestrated(state)`.
4. Set `state.current_agent = selected_agent`.
5. If `selected_agent == "finished"`, stop.
6. If not `orch_coder_agent`, call `selectAgent(state)`.
7. If `orch_coder_agent`, call `CODING_ORCHESTRATOR(state)` and set `state.next_agent`.

Missing or broken behavior:
- `state.task_complete` is never set for normal final responses.
- `state.final_response` is never assigned.
- `selectAgent_for_coding(state)` is incorrectly invoked.
- There is no validation that the orchestrator returned a valid agent name.
- `history` is appended but not consistently used as context.

### 4.2 Main Orchestrator responsibility

The main orchestrator should decide:
- whether the task is a planning task
- whether the task needs research
- whether the task needs coding
- whether the task is a simple answer

It should not decide implementation details such as exact language or code executor commands.

### 4.3 Coding Orchestrator responsibility

The coding orchestrator should decide:
- which coding sub-agent is next
- which implementation language or stack should be used
- whether to execute code or continue working on design or tests
- when to ask for documentation generation

So for a full app build request, the coding orchestrator is responsible for language selection.

## 5. Multi-Language Executor Design

Existing tool:
- `Tools/coder_Tool/code_executor_Tool.py`
- Only Python execution is implemented.

Recommended design:

### 5.1 Executor interface

Create a shared dispatcher:
- `Tools/code_executor/execute_code.py`

Functions:
- `execute_code(language, code, working_dir=None) -> dict`
- `language` is a string like `python`, `javascript`, `node`, `java`, `go`, `ruby`, `bash`, `php`.
- `code` is the source to execute.

Return structure should be standardized:

```python
{
  "status": "success" | "failed",
  "stdout": "...",
  "stderr": "...",
  "language": "python",
  "command": "python temp.py"
}
```

### 5.2 Language-specific executors

Create separate modules:

- `Tools/code_executor/python_executor.py`
- `Tools/code_executor/node_executor.py`
- `Tools/code_executor/java_executor.py`
- `Tools/code_executor/go_executor.py`
- `Tools/code_executor/ruby_executor.py`
- `Tools/code_executor/php_executor.py`
- `Tools/code_executor/bash_executor.py`

Each module should:
- write source to a temporary file or directory
- execute the correct interpreter/compiler command
- capture stdout and stderr
- clean up temporary files
- return the same standardized dictionary

### 5.3 Dispatcher example

The dispatcher should map language identifiers to executors:

```python
from Tools.code_executor.python_executor import python_execute
from Tools.code_executor.node_executor import node_execute

EXECUTORS = {
    "python": python_execute,
    "py": python_execute,
    "javascript": node_execute,
    "js": node_execute,
    "node": node_execute,
    "java": java_execute,
    "go": go_execute,
    "ruby": ruby_execute,
    "php": php_execute,
    "bash": bash_execute,
}


def execute_code(language, code, args=None):
    executor = EXECUTORS.get(language.lower())
    if not executor:
        return {
            "status": "failed",
            "stdout": "",
            "stderr": f"Unsupported language: {language}",
        }
    return executor(code, args=args)
```

### 5.4 How language selection should work

The `Agent/orch_coder_agent.py` prompt should include:
- `user_query`
- `stack_plan`
- `architecture`
- `generated_code`
- `execution_error`
- `execution_output`
- `review_result`
- `test_cases`
- `documentation`
- `history`

It should answer with the next coding agent name and optionally the language, e.g.:

```json
{
  "selected_agent": "code_generator_agent",
  "language": "python"
}
```

or as plain text with a stable format.

Then `piplining.py` should parse that response and store:
- `state.next_agent`
- `state.language` (new field recommended)

## 6. Full app/site build flow: 0 → 100

When a user asks: “Build a full app or site from 0 to 100”, the ideal flow is:

1. **Main Orchestrator receives the request**
   - Route to `planner` if requirements need structure.
   - If the request is already clearly a full app, route to `orch_coder_agent`.

2. **Planner / Requirements analysis**
   - `planner` extracts functional requirements, features, user roles, constraints.
   - Output should include what the app must do and any architecture constraints.
   - Use `state.history` so the planner knows prior context.

3. **Project architecture selection**
   - `Agent/orch_coder_agent.py` chooses `Project_Architect_agent` or `code_generator_agent`.
   - If no stack exists, `Project_Architect_agent` should define the stack.
   - This includes language, framework, frontend, backend, database, and deployment model.

4. **Stack planning and implementation plan**
   - `stack_planner_agent` can create a concrete implementation plan or project structure.
   - The result is stored in `state.stack_plan`.

5. **Code generation stage**
   - The coder orchestrator chooses `code_generator_agent` with a specific language.
   - The agent generates code for each component or file.
   - `state.generated_code` is updated.

6. **Code execution and validation**
   - If execution is requested, call `code_executor_Tool` or a language-specific executor.
   - Store results in `state.execution_output` or `state.execution_error`.

7. **Debugging and repair**
   - If any execution error occurs, choose `solve_error_agent`.
   - The error agent repairs code and updates `state.execution_error` / `state.generated_code`.

8. **Quality review**
   - Run `Code_Reviewer_agent` to review generated code quality.
   - Store findings in `state.review_result`.

9. **Security and testing**
   - Run `Security_Auditor_agent` if security review is needed.
   - Run `Test_Generator_agent` to create tests and store them in `state.test_cases`.

10. **Documentation**
    - Run `Documentation_Agent` to produce README, setup guide, API docs.
    - Store documentation output in `state.documentation`.

11. **Finalize**
    - `final_responder` or `answer_generator` produces the user-facing summary.
    - Set `state.final_response` and `state.task_complete = True`.

## 7. Where language is decided

- The **main orchestrator** only decides whether coding is required.
- The **coding orchestrator** should decide which language, framework, or executor tool to use for actual implementation.
- This is the correct separation of responsibility.

If the user explicitly asks for Python, JavaScript, or another language, the coder orchestrator should record that choice and use the matching executor.

## 8. Recommended code changes

### 8.1 Add `language` to state

In `State/state_agent.py`, add:

```python
language: str = ""
```

### 8.2 Improve `piplining.py`

- validate orchestrator output
- set `state.task_complete` for final answers
- store `state.final_response`
- execute coder sub-agents correctly

### 8.3 Improve `Agent/orch_coder_agent.py`

- include `history` and `documentation`
- return a structured decision containing both the next agent and the chosen language

### 8.4 Build a dispatcher executor

Implement `Tools/code_executor/execute_code.py` and language-specific executors.

## 9. Example multi-language executor architecture

```
Tools/
  code_executor/
    __init__.py
    execute_code.py
    python_executor.py
    node_executor.py
    java_executor.py
    go_executor.py
    ruby_executor.py
    php_executor.py
    bash_executor.py
```

### Example dispatcher

```python
from Tools.code_executor.python_executor import python_execute
from Tools.code_executor.node_executor import node_execute

EXECUTORS = {
    "python": python_execute,
    "py": python_execute,
    "javascript": node_execute,
    "js": node_execute,
    "node": node_execute,
    "java": java_execute,
    "go": go_execute,
    "ruby": ruby_execute,
    "php": php_execute,
    "bash": bash_execute,
}


def execute_code(language, code, timeout=10):
    executor = EXECUTORS.get(language.lower())
    if not executor:
        return {
            "status": "failed",
            "stdout": "",
            "stderr": f"Unsupported language: {language}",
        }
    return executor(code, timeout=timeout)
```

## 10. Sample flow for a full app request

User: `Build a full e-commerce site with Python Flask and React from 0 to 100.`

1. Main orchestrator routes to `planner` or `orch_coder_agent`.
2. `planner` extracts requirements and stores them in `state.history`.
3. `orch_coder_agent` chooses `Project_Architect_agent`.
4. `Project_Architect_agent` defines stack:
   - Python Flask backend
   - React frontend
   - SQLite or PostgreSQL
   - Docker deployment
5. `stack_planner_agent` records the implementation plan.
6. `code_generator_agent` writes the first files.
7. `code_executor_Tool` runs the server or unit tests.
8. `solve_error_agent` fixes issues if execution fails.
9. `Code_Reviewer_agent` improves quality.
10. `Test_Generator_agent` creates tests.
11. `Documentation_Agent` writes README and deployment guide.
12. `final_responder` returns the completed app plan and results.

## 11. Conclusion

This system should separate concerns cleanly:

- **Main orchestrator**: route the task
- **Coding orchestrator**: manage coding lifecycle and language selection
- **State**: carry shared context and lifecycle signals
- **Executors**: run code in a standardized multi-language environment
- **Finalization**: stop the loop when the task is complete and return `state.final_response`

To fix your project, implement the missing prompt arguments, add clear completion conditions, and build a multi-language executor dispatcher. This document is the full design of how your system should work from a user request to a completed app site build.
