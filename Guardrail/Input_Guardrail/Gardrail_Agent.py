from service.llm import get_llm
from config.prompt import format_prompt
from Guardrail.Input_Guardrail.input_Gardrail_prompt import INPUT_GUARDRAIL_PROMPT

def Gardrail_Agent(request):
    llm = get_llm()
    
    prompt = format_prompt(INPUT_GUARDRAIL_PROMPT,userinput=request)
    
    response = llm.invoke(prompt)
    
    return response
