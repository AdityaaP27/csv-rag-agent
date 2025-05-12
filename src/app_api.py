import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile

from rag.config import CSV_PATH
from rag.ingest import load_documents
from rag.chain  import build_qa_chain

app = FastAPI(title="CSV RAG Q&A API")

# In-memory holder for the current chain
current_qa_chain = None

@app.post("/index")
async def index_csv(
    use_sample: bool = Form(True),
    file: UploadFile = File(None),
):
    """
    Ingest & index a new CSV. Always recreates Pinecone index fresh.
    """
    global current_qa_chain

    # 1) Determine CSV path
    if file and not use_sample:
        tmp = NamedTemporaryFile(delete=False, suffix=".csv")
        tmp.write(await file.read())
        tmp.close()
        csv_path = tmp.name
    else:
        csv_path = CSV_PATH

    try:
        # 2) Load, ingest, build chain
        docs = load_documents(csv_path)
        current_qa_chain = build_qa_chain(docs)
        return {"status": "indexed", "num_docs": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_csv(
    question: str = Form(...),
):
    """
    Query the currently indexed CSV. Requires prior /index call.
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if not current_qa_chain:
        raise HTTPException(status_code=400, detail="No data indexed. Call /index first.")
    try:
        answer = current_qa_chain.run(question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
