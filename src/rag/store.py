from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from .config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX
from .embed import get_embedder

def init_vector_store(documents):
    # 1) Init Pinecone client
    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    # 2) Delete existing index if present (fresh start)
    if PINECONE_INDEX in pc.list_indexes().names():
        pc.delete_index(PINECONE_INDEX)
    # 3) Create index
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV),
    )
    # 4) Connect to index
    index = pc.Index(PINECONE_INDEX)
    # 5) Wrap with LangChain store
    embedder     = get_embedder()
    vector_store = PineconeVectorStore(
        index=index, embedding=embedder, text_key="page_content"
    )
    # 6) Upsert documents
    vector_store.add_documents(documents)
    return vector_store
