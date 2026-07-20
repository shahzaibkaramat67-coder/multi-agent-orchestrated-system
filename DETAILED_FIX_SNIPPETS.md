# Detailed Fix Instructions - Copy/Paste Solutions

## 🔴 CRITICAL FIX #1: orchestrated_agent.py Format String

**File**: `orchestrated_agent.py`  
**Location**: Lines 8-12

**BEFORE**:
```python
def Orchestrated(user_query, history, context):
    print("decision this is from orchestrator function")
    llm = get_llm()

    prompt = Orchestrator_agent_prompt.format(
        user_query,
        history,
        context,
        # stack_plan=state.stack_plan,
```

**AFTER**:
```python
def Orchestrated(user_query, history, context):
    print("decision this is from orchestrator function")
    llm = get_llm()

    prompt = Orchestrator_agent_prompt.format(
        user_query=user_query,
        history=history,
        context=context,
        # stack_plan=state.stack_plan,
```

---

## 🔴 CRITICAL FIX #2: Agent/orch_coder_agent.py Format String

**File**: `Agent/orch_coder_agent.py`  
**Location**: Lines 8-12

**BEFORE**:
```python
def CODING_ORCHESTRATOR(user_query, history, context):
    llm = get_llm()

    prompt = CODING_ORCHESTRATOR_AGENT_PROMPT.format(
        user_query,
        history,
        context,
        # architecture=state.architecture,
```

**AFTER**:
```python
def CODING_ORCHESTRATOR(user_query, history, context):
    llm = get_llm()

    prompt = CODING_ORCHESTRATOR_AGENT_PROMPT.format(
        user_query=user_query,
        history=history,
        context=context,
        # architecture=state.architecture,
```

---

## 🔴 CRITICAL FIX #3: Remove Bad Imports

**Files**: 
- `piplining.py` Line 8
- `router/route.py` Line 6

**PROBLEM LINE**:
```python
from Tools.coder_Tool.code_executor_Tool import code_executor_Tool
```

**SOLUTION**: Comment it out for now
```python
# from Tools.coder_Tool.code_executor_Tool import code_executor_Tool
```

Also need to remove any usages. In `router/route.py` around line 48:
```python
# BEFORE:
elif agent == "code_executor_Tool":
    return code_executor_Tool(user_input, Result)

# AFTER (comment out):
# elif agent == "code_executor_Tool":
#     return code_executor_Tool(user_input, Result)
```

---

## 🔴 CRITICAL FIX #4: Fix Function Arguments

**File**: `router/route.py`  
**Location**: Line 47

**BEFORE**:
```python
def selectAgent_for_coding(state):
    Result = state.history
    agent = state.next_agent
    user_input = state.user_query
    if agent == "code_generator_agent":
        return code_generator_agent(state.user_query, state.history)
```

**AFTER**:
```python
def selectAgent_for_coding(state):
    Result = state.history
    agent = state.next_agent
    user_input = state.user_query
    if agent == "code_generator_agent":
        return code_generator_agent(state.user_query)
```

---

## 🟠 HIGH FIX #5: Fix Agent Return Types

### Agent/answer_generator.py

**BEFORE**:
```python
def answer_generator(user_input):
    llm = get_llm()

    prompt = ANSWER_GENERATOR_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    print("response answer_generator :", response)

    return response
```

**AFTER**:
```python
def answer_generator(user_input):
    llm = get_llm()

    prompt = ANSWER_GENERATOR_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    print("response answer_generator :", response)

    return {
        "event": "answer_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"response": response}
    }
```

### Agent/researcher.py

**BEFORE**:
```python
def researcher(user_input):
    llm = get_llm()

    research_result = research(user_input)

    prompt = RESEARCHER_PROMPT.format(
        user_input=user_input, research_result=research_result
    )

    response = llm.invoke(prompt).content
    print("response researcher", response)

    return response
```

**AFTER**:
```python
def researcher(user_input):
    llm = get_llm()

    research_result = research(user_input)

    prompt = RESEARCHER_PROMPT.format(
        user_input=user_input, research_result=research_result
    )

    response = llm.invoke(prompt).content
    print("response researcher", response)

    return {
        "event": "research_completed",
        "message": response,
        "confidence": 1.0,
        "data": {"research": research_result, "response": response}
    }
```

### Agent/query_rewritter.py

**BEFORE**:
```python
def query_rewriter(user_input):
    llm = get_llm()

    prompt = QUERY_REWRITER_PROMPT.format(user_query=user_input)

    response = llm.invoke(prompt).content
    print("response query_rewriter", response)

    return response
```

**AFTER**:
```python
def query_rewriter(user_input):
    llm = get_llm()

    prompt = QUERY_REWRITER_PROMPT.format(user_query=user_input)

    response = llm.invoke(prompt).content
    print("response query_rewriter", response)

    return {
        "event": "query_rewritten",
        "message": response,
        "confidence": 1.0,
        "data": {"rewritten_query": response}
    }
```

### Agent/planner.py

**BEFORE**:
```python
def planner(user_input, history):
    llm = get_llm()

    prompt = REQUIREMENT_ANALYSIS_AGENT_PROMPT.format(
        user_query=user_input, history=history
    )

    response = llm.invoke(prompt).content

    print("response planner", response)

    return response
```

**AFTER**:
```python
def planner(user_input, history):
    llm = get_llm()

    prompt = REQUIREMENT_ANALYSIS_AGENT_PROMPT.format(
        user_query=user_input, history=history
    )

    response = llm.invoke(prompt).content

    print("response planner", response)

    return {
        "event": "plan_created",
        "message": response,
        "confidence": 1.0,
        "data": {"plan": response}
    }
```

### Agent/final_reponder.py

**BEFORE**:
```python
def final_responder(agent_output: str):
    llm = get_llm()
    prompt = FINAL_RESPONDER_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content

    print("final responder agent :", response)

    return response
```

**AFTER**:
```python
def final_responder(agent_output: str):
    llm = get_llm()
    prompt = FINAL_RESPONDER_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content

    print("final responder agent :", response)

    return {
        "event": "final_response",
        "message": response,
        "confidence": 1.0,
        "data": {"response": response}
    }
```

### Agent/critic.py

**BEFORE**:
```python
def critic(agent_output: str):
    llm = get_llm()
    prompt = CRITIC_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content.strip().lower()

    print("response critic :", response)
    return response
```

**AFTER**:
```python
def critic(agent_output: str):
    llm = get_llm()
    prompt = CRITIC_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content.strip().lower()

    print("response critic :", response)
    return {
        "event": "critique_completed",
        "message": response,
        "confidence": 1.0,
        "data": {"critique": response}
    }
```

### Agent/evaluator.py

**BEFORE**:
```python
def evaluator(agent_output: str):
    llm = get_llm()
    prompt = EVALUATOR_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content.strip()
    print("response evaluator :", response)

    return response
```

**AFTER**:
```python
def evaluator(agent_output: str):
    llm = get_llm()
    prompt = EVALUATOR_PROMPT.format(agent_output=agent_output)
    response = llm.invoke(prompt).content.strip()
    print("response evaluator :", response)

    return {
        "event": "evaluation_completed",
        "message": response,
        "confidence": 1.0,
        "data": {"evaluation": response}
    }
```

### coder_agents/code_generator_agent.py

**BEFORE**:
```python
def code_generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = CODE_GENERATOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response code_generator_agent :", response)

    return response
```

**AFTER**:
```python
def code_generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = CODE_GENERATOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response code_generator_agent :", response)

    return {
        "event": "code_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"code": response}
    }
```

### coder_agents/Code_Reviewer_agent.py

**BEFORE**:
```python
def Code_Reviewer_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = CODE_REVIEW_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Code_Reviewer_agent :", response)

    return response
```

**AFTER**:
```python
def Code_Reviewer_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = CODE_REVIEW_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Code_Reviewer_agent :", response)

    return {
        "event": "code_reviewed",
        "message": response,
        "confidence": 1.0,
        "data": {"review": response}
    }
```

### coder_agents/Documentation_Agent.py

**BEFORE**:
```python
def Documentation_Agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = DOCUMENTATION_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Documentation_Agent :", response)

    return response
```

**AFTER**:
```python
def Documentation_Agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = DOCUMENTATION_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Documentation_Agent :", response)

    return {
        "event": "documentation_created",
        "message": response,
        "confidence": 1.0,
        "data": {"documentation": response}
    }
```

### coder_agents/Project_Architect_agent.py

**BEFORE**:
```python
def Project_Architect_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = PROJECT_ARCHITECTURE_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Project_Architect_agent :", response)

    return response
```

**AFTER**:
```python
def Project_Architect_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = PROJECT_ARCHITECTURE_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Project_Architect_agent :", response)

    return {
        "event": "architecture_designed",
        "message": response,
        "confidence": 1.0,
        "data": {"architecture": response}
    }
```

### coder_agents/Security_Auditor_agent.py

**BEFORE**:
```python
def Security_Auditor_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = SECURITY_AUDITOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Security_Auditor_agent :", response)

    return response
```

**AFTER**:
```python
def Security_Auditor_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = SECURITY_AUDITOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Security_Auditor_agent :", response)

    return {
        "event": "security_audited",
        "message": response,
        "confidence": 1.0,
        "data": {"security_report": response}
    }
```

### coder_agents/Test_Generator_agent.py

**BEFORE**:
```python
def Test_Generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = TEST_GENERATOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Test_Generator_agent :", response)

    return response
```

**AFTER**:
```python
def Test_Generator_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = TEST_GENERATOR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response Test_Generator_agent :", response)

    return {
        "event": "tests_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"test_cases": response}
    }
```

### coder_agents/solve_error_agent.py

**BEFORE**:
```python
def solve_error_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = SOLVE_ERROR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response solve_error_agent :", response)

    return response
```

**AFTER**:
```python
def solve_error_agent(user_input):
    llm = get_llm()
    # coder_llm = coder_llm()

    prompt = SOLVE_ERROR_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content
    # response = coder_llm.invoke(prompt)

    print("response solve_error_agent :", response)

    return {
        "event": "error_solved",
        "message": response,
        "confidence": 1.0,
        "data": {"solution": response}
    }
```

### coder_agents/stack_planner_agent.py

**BEFORE**:
```python
def Stack_planner(user_input):
    llm = get_llm()

    prompt = STACK_PLANNER_AGENT_PROMPT.format(user_query=user_input)

    response = llm.invoke(prompt).content
    print("response from Stack_planner agent", response)
    return response
```

**AFTER**:
```python
def Stack_planner(user_input):
    llm = get_llm()

    prompt = STACK_PLANNER_AGENT_PROMPT.format(user_query=user_input)

    response = llm.invoke(prompt).content
    print("response from Stack_planner agent", response)
    return {
        "event": "stack_planned",
        "message": response,
        "confidence": 1.0,
        "data": {"stack_plan": response}
    }
```

---

## 🟠 HIGH FIX #6: Add Missing Return Statement

**File**: `router/route.py`  
**Location**: End of `selectAgent_for_coding` function (after line 67)

**ADD BEFORE THE FINAL CLOSING BRACE**:
```python
    else:
        return {
            "event": "error",
            "message": f"Unknown coding agent: {agent}",
            "confidence": 0.0,
            "data": {"error": "unknown_agent"}
        }
```

---

## 🟠 HIGH FIX #7: Fix CODING_ORCHESTRATOR Call (Optional Fix)

**File**: `router/route.py`  
**Location**: Lines 23-26 (might be unreachable code - verify first)

**BEFORE**:
```python
    if agent == "orch_coder_agent":
        return CODING_ORCHESTRATOR(user_input=user_query)
```

**AFTER** (if you decide to keep it):
```python
    if agent == "orch_coder_agent":
        return CODING_ORCHESTRATOR(user_query, history)
```

**NOTE**: This code might be dead code. Verify that selectAgent is ever called with "orch_coder_agent".

---

## 🟡 MEDIUM FIX #8: Create Missing __init__.py Files

Create two empty files:

**File**: `Tools/__init__.py`
```python
# Package marker
```

**File**: `Tools/research_agent_Tool/__init__.py`
```python
# Package marker
```

---

## 🟡 MEDIUM FIX #9: Fix task_desomposer.py

**File**: `coder_agents/task_desomposer.py`

**BEFORE**:
```python
from service.llm import get_llm
from config.coder_agent_prompt import TASK_DECOMPOSER_AGENT_PROMPT


def TASK_DECOMPOSER_AGENT():
    llm = get_llm()

    prompt = TASK_DECOMPOSER_AGENT_PROMPT.format()

    response = llm.invoke(prompt).content

    return response
```

**AFTER**:
```python
from service.llm import get_llm
from config.coder_agent_prompt import TASK_DECOMPOSER_AGENT_PROMPT


def TASK_DECOMPOSER_AGENT(user_input):
    llm = get_llm()

    prompt = TASK_DECOMPOSER_AGENT_PROMPT.format(user_input=user_input)

    response = llm.invoke(prompt).content

    return {
        "event": "task_decomposed",
        "message": response,
        "confidence": 1.0,
        "data": {"decomposition": response}
    }
```

---

## ✅ Verification Steps

After making all changes, test:

```bash
# 1. Check syntax
python -m py_compile main.py
echo "Syntax OK"

# 2. Try importing (should not error)
python -c "from piplining import run; print('Imports OK')"

# 3. Try running (will wait for input)
python main.py
# Type: "hello"
# Press Enter
# Should see responses, no errors
# Press Ctrl+C to exit
```

