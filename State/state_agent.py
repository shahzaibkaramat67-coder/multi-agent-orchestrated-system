# state/agent_state.py
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AgentMessage:
    timestamp: str = ""
    agent: str = ""
    event: str = ""
    message: str = ""
    confidence: float = 0.0
    data: Dict[str, Any] = field(default_factory=dict)


# @dataclass
# class AgentMessage:
#     timeStamp: str = ""
#     agent: str = ""
#     event: str = ""
#     message: str = ""


@dataclass
class AgentState:
    user_query: str = ""

    current_agent: str = ""
    next_agent: str = ""
    task_complete: bool = False

    history: List[AgentMessage] = field(default_factory=list)

    context: Dict[str, Any] = field(default_factory=dict)

    final_response: Dict[str, Any] = field(default_factory=dict)
    # routing_history: List[AgentMessage] = field(default_factory=list)

    # execution_history: List[AgentMessage] = field(default_factory=list)


# @dataclass
# class AgentState:
#     user_query: str = ""

#     current_agent: str = ""
#     next_agent: str = ""
#     task_complete: bool = False

#     history: List[Dict[str, Any]] = field(default_factory=list)

#     architecture: str = ""

#     # 🔥 CORE ADDITION
#     stack_plan: List[Dict[str, Any]] = field(default_factory=list)

#     generated_code: str = ""
#     execution_output: str = ""
#     execution_error: str = ""

#     review_result: str = ""
#     security_report: str = ""
#     test_cases: str = ""
#     documentation: str = ""

#     final_response: str = ""
