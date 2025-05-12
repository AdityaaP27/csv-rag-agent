from langchain.chains import RetrievalQA
from .store import init_vector_store
from .llm import get_llm

def build_qa_chain(documents):
    llm = get_llm()
    vector_store = init_vector_store(documents)
    retriever = vector_store.as_retriever(search_kwargs={"k": 800})
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
