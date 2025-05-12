from langchain_mistralai import MistralAIEmbeddings

def get_embedder():
    # returns a LangChain-compatible embeddings instance
    return MistralAIEmbeddings(model="mistral-embed")
