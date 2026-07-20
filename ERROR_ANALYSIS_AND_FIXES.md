# Error Analysis and Fixes

## 1. Original Error

When running the application, the following failure occurred:

```text
KeyError: 'user_input'
```

It happened while the planner agent was preparing its prompt for the LLM.

### Stack Trace Summary

The failure followed this path:

1. [main.py](main.py)
2. [piplining.py](piplining.py)
3. [router/route.py](router/route.py)
4. [Agent/planner.py](Agent/planner.py)
5. [config/prompt.py](config/prompt.py)

The error was raised inside the planner because the prompt template was being formatted with Python’s built-in string formatting mechanism.

---

## 2. Root Cause

The prompt template in [config/prompt.py](config/prompt.py) contained placeholders such as:

```python
{user_input}
{history}
```

At the same time, the template also contained JSON-style examples with literal braces, for example:

```text
{
    "event": "COMPLETED"
}
```

Python’s `str.format()` interprets every `{...}` block as a formatting placeholder. Because the prompt included literal braces for JSON examples, the formatter treated them as part of the formatting syntax and raised a `KeyError`.

In short:

- the real placeholders were valid,
- but the prompt also contained literal braces for example JSON,
- and the old formatting logic could not distinguish between the two.

---

## 3. Why It Happened

The planner was using code similar to this:

```python
prompt = REQUIREMENT_ANALYSIS_AGENT_PROMPT.format(
    user_input=user_input,
    history=history
)
```

This works only when the whole template contains placeholders that are meant for substitution and no literal braces that should be preserved as-is.

In this project, the prompt templates were large and included structured JSON examples, so the direct `.format()` call was fragile and caused the crash.

---

## 4. The Fix Applied

A safe formatter was introduced in [config/prompt.py](config/prompt.py).

### What changed

Instead of using Python’s raw `.format()`, the project now uses a custom formatter that:

- replaces only the intended placeholders,
- preserves literal braces used in JSON examples,
- raises a clear `KeyError` only when a real placeholder is missing.

### New helper

The new helper is implemented as:

```python
def format_prompt(template: str, **kwargs) -> str:
    ...
```

This helper processes only real placeholders such as:

```python
{user_input}
{history}
```

and leaves JSON braces untouched.

---

## 5. Files Updated

The fix was applied across the following files:

- [config/prompt.py](config/prompt.py)
- [Agent/planner.py](Agent/planner.py)
- [Agent/orch_coder_agent.py](Agent/orch_coder_agent.py)
- [Agent/query_rewritter.py](Agent/query_rewritter.py)
- [Agent/answer_generator.py](Agent/answer_generator.py)
- [Agent/critic.py](Agent/critic.py)
- [Agent/evaluator.py](Agent/evaluator.py)
- [Agent/final_reponder.py](Agent/final_reponder.py)
- [Agent/researcher.py](Agent/researcher.py)
- [orchestrated_agent.py](orchestrated_agent.py)
- [coder_agents/code_generator_agent.py](coder_agents/code_generator_agent.py)
- [coder_agents/Code_Reviewer_agent.py](coder_agents/Code_Reviewer_agent.py)
- [coder_agents/Documentation_Agent.py](coder_agents/Documentation_Agent.py)
- [coder_agents/Project_Architect_agent.py](coder_agents/Project_Architect_agent.py)
- [coder_agents/Security_Auditor_agent.py](coder_agents/Security_Auditor_agent.py)
- [coder_agents/solve_error_agent.py](coder_agents/solve_error_agent.py)
- [coder_agents/stack_planner_agent.py](coder_agents/stack_planner_agent.py)
- [coder_agents/task_desomposer.py](coder_agents/task_desomposer.py)
- [coder_agents/Test_Generator_agent.py](coder_agents/Test_Generator_agent.py)

---

## 6. Additional Issue Found

While investigating the main error, I found the same pattern in other agents as well. That means the bug was not limited to the planner.

The project had multiple places where prompt templates were being formatted with `.format()` directly. Those were updated too so the fix is consistent across the orchestration system.

---

## 7. Regression Test Added

A regression test was created in:

- [tests/test_prompt_formatting.py](tests/test_prompt_formatting.py)

The test verifies that:

- real placeholders are replaced correctly,
- literal JSON braces remain intact,
- missing placeholders still raise a clear error.

---

## 8. Verification

The solution was verified with the following command:

```powershell
python -m unittest tests.test_prompt_formatting
```

Result:

```text
Ran 2 tests in 0.001s

OK
```

---

## 9. Final Summary

The error was caused by prompt-template formatting conflicts between actual placeholders and literal braces used in the JSON examples inside the prompt text.

The fix was to replace the unsafe formatting approach with a safer one that handles placeholders correctly while preserving JSON examples.

This resolved the planner crash and also prevented the same issue from appearing in the other agent prompt paths.
