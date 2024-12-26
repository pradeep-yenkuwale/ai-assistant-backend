
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma

from langchain.embeddings.openai import OpenAIEmbeddings  # Adjust if using a different embedding model
from app.constants.constants import CONTEXT
from app.constants.prompts import GENERAL_PROMPT, FUTURE_BOOKINGS, LANGUAGE_PROMPT, SUGGEST_TRIPS, GREETINGS

from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Set a openai key to access the openai apis
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY") or ""

def prepare_prompt(query, language, context):        
    # Set it global as it would get modified
    global GREETINGS
    if(len(query.split()) == 1 and (query not in GREETINGS)):
        GREETINGS = GREETINGS + ", " + query 

    not_greetings = query.lower() not in GREETINGS.lower()

    if (context == CONTEXT['SUGGEST_TRIPS'] and not_greetings):
        query += SUGGEST_TRIPS
    elif (context == CONTEXT['PEOPLE_INTERESTS'] and not_greetings):
        query += SUGGEST_TRIPS
    elif (context == CONTEXT['FUTURE_BOOKING'] and not_greetings):
        query += FUTURE_BOOKINGS
    else:
        if not_greetings:
            query += GENERAL_PROMPT
    
    if(language == "ar"):
        query += LANGUAGE_PROMPT
    return query
# help(ConversationalRetrievalChain)
def configure_model(callback):
    try:
        # load the data to train the AI model
        loader = TextLoader("app/data/data.json")
        
        documents = loader.load()
        
        embeddings = OpenAIEmbeddings()  # Adjust to your embedding model

        vectorstore = Chroma.from_documents(documents, embeddings)

        # Get the Conversational Change for asked query
        chain = ConversationalRetrievalChain.from_llm(
            llm = ChatOpenAI(model="gpt-4o", callbacks=[callback]),
            retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
            )
        return chain
    except Exception as error:
        print("error ia m hee now", error)
