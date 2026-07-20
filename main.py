from piplining import run

# from pprint import pprint
# from rich import print

while True:
    user_input = input("Ask Anything : ")
    if user_input == "exit":
        break
    response = run(user_input)
    print("final response from run : ", response)
