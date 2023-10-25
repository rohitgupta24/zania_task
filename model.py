import os
import sys
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma 
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from prompt import prompt

os.environ["OPENAI_API_KEY"] = ""

DB_FAISS_PATH = 'vectorstore/db_faiss'

embeddings = OpenAIEmbeddings()
db = FAISS.load_local(DB_FAISS_PATH, embeddings)

import json

# List of questions
questions = [
    "What is the name of the company?",
    "Who is the CEO of the company?",
    "What is their vacation policy?",
    "What is the termination policy?"
]

# Write questions to a JSON file
with open('questions.json', 'w') as json_file:
    json.dump({"questions": questions}, json_file)




#Function for similarity search
def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)

    page_contents_array = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return page_contents_array


# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=prompt)

def generate_responses(questions):
    response_blob = {}

    for question in questions:
        best_practice = retrieve_info(question)
        response = chain.run(message=question, best_practice=best_practice)
        response_blob[question] = response

    # Write responses to a JSON file
    with open('responses.json', 'w') as json_file:
        json.dump(response_blob, json_file)

# Call the generate_responses function
generate_responses(questions)


