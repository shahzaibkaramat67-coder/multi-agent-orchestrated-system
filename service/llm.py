from langchain_google_genai import ChatGoogleGenerativeAI

from config.setting import model, temprature

# from ollama import chat


def get_llm():
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temprature,
    )


# def coder_llm():
#     return chat(
#         model=model,
#         temperature=temprature,
#     )
