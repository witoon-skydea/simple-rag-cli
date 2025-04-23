#!/usr/bin/env python3
"""
Simple RAG CLI for document Q&A
"""
import os
import argparse
import sys
from rag.document_loader import load_document
from rag.vector_store import get_vector_store, add_documents, similarity_search
from rag.llm import get_llm_model, generate_response

# Constants
DEFAULT_DB_DIR = "db"

def ingest_documents(args):
    """
    Ingest documents into the vector store
    
    Args:
        args: Command line arguments
    """
    # Get vector store
    db_path = os.path.join(os.getcwd(), args.db_dir)
    vector_store = get_vector_store(db_path)
    
    # Load and add documents
    for file_path in args.files:
        print(f"Loading {file_path}...")
        try:
            documents = load_document(file_path)
            print(f"  Loaded {len(documents)} chunks")
            
            add_documents(vector_store, documents)
            print(f"  Added to vector store")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"Documents ingested successfully to {db_path}")

def answer_question(args):
    """
    Answer a question using the RAG system
    
    Args:
        args: Command line arguments
    """
    # Get vector store
    db_path = os.path.join(os.getcwd(), args.db_dir)
    
    if not os.path.exists(db_path):
        print(f"Error: Vector store not found at {db_path}")
        print("Please ingest documents first using the 'ingest' command")
        sys.exit(1)
    
    vector_store = get_vector_store(db_path)
    
    # Get LLM
    llm = get_llm_model()
    
    # Get relevant documents
    print("Searching for relevant documents...")
    documents = similarity_search(vector_store, args.question, k=4)
    
    # Generate response
    print("Generating response...\n")
    response = generate_response(llm, documents, args.question)
    
    # Print response
    print("-" * 80)
    print("Answer:")
    print(response.strip())
    print("-" * 80)

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser(description="Simple RAG CLI for document Q&A")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents")
    ingest_parser.add_argument("files", nargs="+", help="Files to ingest")
    ingest_parser.add_argument("--db-dir", default=DEFAULT_DB_DIR, help="Directory to store the vector database")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the documents")
    query_parser.add_argument("question", help="Question to answer")
    query_parser.add_argument("--db-dir", default=DEFAULT_DB_DIR, help="Directory to store the vector database")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        ingest_documents(args)
    elif args.command == "query":
        answer_question(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
