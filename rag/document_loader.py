"""
Document loader module for RAG system
"""
import os
from typing import List, Set
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md', '.csv'}

def is_supported_file(file_path: str) -> bool:
    """
    Check if a file is supported for ingestion
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is supported, False otherwise
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in SUPPORTED_EXTENSIONS

def scan_directory(directory_path: str, recursive: bool = True) -> List[str]:
    """
    Scan a directory for supported files
    
    Args:
        directory_path: Path to the directory
        recursive: Whether to scan subdirectories recursively
        
    Returns:
        List of file paths
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"Not a directory: {directory_path}")
    
    supported_files = []
    
    # Walk through directory
    if recursive:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if is_supported_file(file_path):
                    supported_files.append(file_path)
    else:
        # Non-recursive scan
        for item in os.listdir(directory_path):
            file_path = os.path.join(directory_path, item)
            if os.path.isfile(file_path) and is_supported_file(file_path):
                supported_files.append(file_path)
    
    return supported_files

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
