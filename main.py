from piplining import run
from API.input import Input_GuardRail

# from pprint import pprint
# from rich import print
def userINput():
    
    while True:
        user_input = input("Ask Anything : ")
        if user_input == "exit":
            break
        response = Input_GuardRail(request = user_input)
        print("final response from run : ", response)
        
userINput()
