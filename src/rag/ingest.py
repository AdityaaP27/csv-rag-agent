import os, tempfile
import pandas as pd
from langchain_community.document_loaders.csv_loader import CSVLoader
from .preprocess import clean_dataframe

def load_documents(path: str):
    # Clean CSV via pandas
    df = pd.read_csv(path)
    df = clean_dataframe(df)

    # Save cleaned DF to platform temp dir
    tmp_dir  = tempfile.gettempdir()
    temp_path = os.path.join(tmp_dir, "cleaned.csv")
    df.to_csv(temp_path, index=False)

    # Load into LangChain Documents
    loader = CSVLoader(file_path=temp_path, csv_args={"delimiter": ","})
    return loader.load()
