from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()


def setup_cromaDB(document):
    document = PyPDFLoader("")
    doc = document.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = splitter.split_documents(documents=doc)

    embedding_model = SentenceTransformer(os.getenv("EMBADDING_MODEL_SENTENCE"))

    Chroma.add_documents(
        documents=chunks, embedding=embedding_model, persist_directory="CromaDB"
    )
