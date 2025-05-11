import os
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_pinecone import PineconeVectorStore  # Use the dedicated package
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env
load_dotenv()

# Validate required env vars
def get_env_var(key: str):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value

# 1. Load CSV into Documents
def load_documents(csv_path: str):
    loader = CSVLoader(
        file_path=csv_path,
        csv_args={"delimiter": ","},
    )
    return loader.load()

# 2. Initialize Groq LLM
def init_llm():
    mistral_api_key = get_env_var("MISTRAL_API_KEY")
    os.environ["MISTRAL_API_KEY"] = mistral_api_key
    return ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    max_retries=2,
    
    )

# 3. Initialize Pinecone and Vector Store
def init_vector_store(documents):
    pinecone_api_key = get_env_var("PINECONE_API_KEY")
    pinecone_env = get_env_var("PINECONE_ENVIRONMENT")
    index_name = get_env_var("PINECONE_INDEX")

    # Create Pinecone client instance
    pc = Pinecone(
        api_key=pinecone_api_key,
        environment=pinecone_env,
    )

    # Create index if missing
    existing = pc.list_indexes().names()
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=1024,  # Dimension for mistral-embed
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=pinecone_env)
        )
    
    # Get the index
    index = pc.Index(index_name)

    # Create embedder
    embedder = MistralAIEmbeddings(model="mistral-embed")

    # Initialize LangChain Pinecone vector store using the dedicated package
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedder,
        text_key="page_content"
    )

    # Add documents (embeds & upserts into Pinecone)
    vector_store.add_documents(documents)
    return vector_store

# 4. Build QA Chain
def create_qa_chain(vector_store, llm):
    retriever = vector_store.as_retriever(search_kwargs={"k": 800})
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )

# Main initialization code
try:
    documents = load_documents(get_env_var("CSV_PATH"))
    llm = init_llm()
    vector_store = init_vector_store(documents)
    qa_chain = create_qa_chain(vector_store, llm)
    print("RAG system successfully initialized!")
except Exception as e:
    print(f"Error initializing RAG system: {e}")
    import traceback
    traceback.print_exc()