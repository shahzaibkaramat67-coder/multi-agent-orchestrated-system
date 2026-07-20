# Quick Reference: Issues at a Glance

## 🔴 CRITICAL - Fix These First

### 1. Import Error: code_executor_Tool Not Found
```
Files: piplining.py:8, router/route.py:6

Line 8 of piplining.py:
❌ from Tools.coder_Tool.code_executor_Tool import code_executor_Tool

Problem: Directory Tools/coder_Tool/ doesn't exist

Solution:
  Option A: Comment out the import (the tool isn't used anywhere critical yet)
  Option B: Create the file if code_executor_Tool is needed
```

### 2. Format String Error: orchestrated_agent.py
```
File: orchestrated_agent.py, Lines 9-11

Current (WRONG):
❌ prompt = Orchestrator_agent_prompt.format(
        user_query,
        history,
        context,
    )

Fix (CORRECT):
✅ prompt = Orchestrator_agent_prompt.format(
        user_query=user_query,
        history=history,
        context=context,
    )
```

### 3. Format String Error: Agent/orch_coder_agent.py
```
File: Agent/orch_coder_agent.py, Lines 9-11

Current (WRONG):
❌ prompt = CODING_ORCHESTRATOR_AGENT_PROMPT.format(
        user_query,
        history,
        context,
    )

Fix (CORRECT):
✅ prompt = CODING_ORCHESTRATOR_AGENT_PROMPT.format(
        user_query=user_query,
        history=history,
        context=context,
    )
```

### 4. Wrong Function Arguments: router/route.py
```
File: router/route.py, Line 47

Current (WRONG):
❌ return code_generator_agent(state.user_query, state.history)

Fix (CORRECT):
✅ return code_generator_agent(state.user_query)

Reason: Function only accepts 1 argument, not 2
```

---

## 🟠 HIGH - Fix After Critical Issues

### 5. Return Type Mismatch: ALL Agent Functions
```
Affected: 15+ files in Agent/ and coder_agents/ directories

Problem: Functions return STRING but code expects DICT with keys:
  - event
  - message
  - confidence
  - data

Example Fix:
Instead of:
❌ def answer_generator(user_input):
    response = llm.invoke(prompt).content
    return response

Do this:
✅ def answer_generator(user_input):
    response = llm.invoke(prompt).content
    return {
        "event": "answer_generated",
        "message": response,
        "confidence": 1.0,
        "data": {"response": response}
    }

Files to update:
  - Agent/answer_generator.py
  - Agent/researcher.py
  - Agent/query_rewritter.py
  - Agent/planner.py
  - Agent/final_reponder.py
  - Agent/critic.py
  - Agent/evaluator.py
  - coder_agents/code_generator_agent.py
  - coder_agents/Code_Reviewer_agent.py
  - coder_agents/Documentation_Agent.py
  - coder_agents/Project_Architect_agent.py
  - coder_agents/Security_Auditor_agent.py
  - coder_agents/Test_Generator_agent.py
  - coder_agents/solve_error_agent.py
  - coder_agents/stack_planner_agent.py
```

### 6. Missing Return in selectAgent_for_coding
```
File: router/route.py, Lines 45-68

Problem: Function returns None if agent doesn't match

Fix: Add at the end:
✅ else:
    return {
        "event": "error",
        "message": f"Unknown coding agent: {agent}",
        "confidence": 0.0,
        "data": {"error": "unknown_agent"}
    }
```

### 7. Wrong Arguments to CODING_ORCHESTRATOR
```
File: router/route.py, Lines 23-26

Current (WRONG):
❌ return CODING_ORCHESTRATOR(user_input=user_query)

Fix (CORRECT):
✅ return CODING_ORCHESTRATOR(user_query, history)

Note: This code path might be unreachable - check if needed
```

---

## 🟡 MEDIUM - Fix After High Priority

### 8. Missing __init__.py Files
```
Files to create (can be empty):
  - Tools/__init__.py
  - Tools/research_agent_Tool/__init__.py

Just create them as empty files or with a simple comment.
```

### 9. Wrong Format Call: task_desomposer
```
File: coder_agents/task_desomposer.py, Line 8

Current (WRONG):
❌ prompt = TASK_DECOMPOSER_AGENT_PROMPT.format()

Fix (CORRECT):
✅ def TASK_DECOMPOSER_AGENT(user_input):
    llm = get_llm()
    prompt = TASK_DECOMPOSER_AGENT_PROMPT.format(user_input=user_input)
    response = llm.invoke(prompt).content
    return {
        "event": "decomposed",
        "message": response,
        "confidence": 1.0,
        "data": {"decomposition": response}
    }
```

---

## 🔵 LOW - Fix When Convenient

### 10. Redundant Code in selectAgent
```
File: router/route.py, Lines 23-26

This code checks for "orch_coder_agent" but it's never passed here.
This code path is unreachable. Remove or clarify intent.
```

### 11. Dead Code
```
File: coder_agents/task_desomposer.py

This function exists but isn't called anywhere.
Remove it if not needed.
```

---

## ✅ Testing Your Fixes

After fixing each issue level, test with:

```bash
# Syntax check
python -m py_compile main.py

# Try running
python main.py
# Enter a simple query and press Ctrl+C to exit

# If it starts accepting input, issues are mostly fixed!
```

---

## 📝 Checklist

- [ ] Fix Issue #3: Remove/fix code_executor_Tool import
- [ ] Fix Issue #1: Format string in orchestrated_agent.py
- [ ] Fix Issue #2: Format string in Agent/orch_coder_agent.py
- [ ] Fix Issue #4: code_generator_agent argument count
- [ ] Fix Issue #5: All agent functions return dicts
- [ ] Fix Issue #6: selectAgent_for_coding returns dict
- [ ] Fix Issue #7: CODING_ORCHESTRATOR arguments
- [ ] Fix Issue #8-9: Add __init__.py files
- [ ] Fix Issue #10: task_desomposer format call
- [ ] Test: python main.py works

