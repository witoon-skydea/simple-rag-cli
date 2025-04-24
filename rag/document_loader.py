"""
Document loader module for RAG system
"""
import os
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_document(file_path: str) -> List:
    """
    Load a document from a file path and split it into chunks
    
    Args:
        file_path: Path to the document
        
    Returns:
        List of document chunks
    """
    _, file_extension = os.path.splitext(file_path)
    
    # Load document based on file extension
    if file_extension.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension.lower() == '.docx':
        loader = Docx2txtLoader(file_path)
    elif file_extension.lower() in ['.txt', '.md', '.csv']:
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks
