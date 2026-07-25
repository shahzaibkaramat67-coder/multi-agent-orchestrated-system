from fastapi import FastAPI
from pydantic import BaseModel
from Guardrail.Input_Guardrail.Gardrail_Agent import Gardrail_Agent
from piplining import run
app = FastAPI()



class ChatRequest(BaseModel):
    query : str





@app.post("/Api/user/Chat")
def Input_GuardRail(request : ChatRequest):
    Guard_result = Gardrail_Agent(request.query)
    if Guard_result["decision"] == "PASS":
        return run(user_input = request.query)
    return Guard_result
   
    