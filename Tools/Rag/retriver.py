# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_classic.prompts import PromptTemplate
from service.llm import get_llm
import os

load_dotenv()


def retriver_from_vectorDB(user_input):

    # model = os.getenv("GEMINI_API_KEY")

    embedding_model = SentenceTransformer(os.getenv("EMBADDING_MODEL_SENTENCE"))

    retriver = Chroma.from_documents(
        embedding=embedding_model, persist_directory="CromaDB"
    )

    # retriver.as_retriever()

    PromptTemplate.from_template([("system", ""), ("Human", "")])

    retrive = retriver.as_retriever(user_input)
    llm = get_llm()
    llm.invoke(retrive)
