import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from tempfile import NamedTemporaryFile
from rag_agent import load_documents, init_llm, init_vector_store, create_qa_chain

app = FastAPI(title="CSV RAG Q&A API")

@app.post("/query")
async def query_csv(
    question: str = Form(...),
    use_sample: bool = Form(True),
    file: UploadFile = File(None)
):
    try:
        if file and not use_sample:
            # Save uploaded file to temp file
            with NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name
        else:
            tmp_path = os.getenv("CSV_PATH", "data.csv")

        # Load and process file
        docs = load_documents(tmp_path)
        llm = init_llm()
        vector_store = init_vector_store(docs)
        qa_chain = create_qa_chain(vector_store, llm)

        answer = qa_chain.run(question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
