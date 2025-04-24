#!/usr/bin/env python3
"""
Simple RAG CLI for document Q&A
"""
import os
import argparse
import sys
from rag.document_loader import load_document, scan_directory, is_supported_file
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
    
    # Prepare list of files to ingest
    files_to_ingest = []
    
    # Process each input path (file or directory)
    for path in args.paths:
        if os.path.isdir(path):
            # If it's a directory, scan for supported files
            print(f"Scanning directory: {path}...")
            try:
                dir_files = scan_directory(path, recursive=args.recursive)
                print(f"  Found {len(dir_files)} supported files")
                files_to_ingest.extend(dir_files)
            except Exception as e:
                print(f"Error scanning directory {path}: {e}")
        elif os.path.isfile(path):
            # If it's a file, check if it's supported
            if is_supported_file(path):
                files_to_ingest.append(path)
            else:
                print(f"Skipping unsupported file: {path}")
        else:
            print(f"Path not found: {path}")
    
    # Load and add documents
    total_files = len(files_to_ingest)
    successful_files = 0
    
    for i, file_path in enumerate(files_to_ingest, 1):
        print(f"[{i}/{total_files}] Loading {file_path}...")
        try:
            documents = load_document(file_path)
            add_documents(vector_store, documents)
            print(f"  Loaded and added {len(documents)} chunks")
            successful_files += 1
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
    
    print(f"\nIngestion complete: {successful_files}/{total_files} files processed successfully")
    print(f"Vector store location: {db_path}")

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
    
    # Get relevant documents
    print("Searching for relevant documents...")
    documents = similarity_search(vector_store, args.question, k=args.num_chunks)
    
    if args.raw_chunks:
        # Print raw chunks without LLM processing
        print("-" * 80)
        print(f"Top {len(documents)} relevant chunks:")
        for i, doc in enumerate(documents):
            print(f"\nChunk {i+1}:")
            print("-" * 40)
            print(doc.page_content)
        print("-" * 80)
    else:
        # Get LLM
        llm = get_llm_model()
        
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
    ingest_parser.add_argument("paths", nargs="+", help="Files or directories to ingest")
    ingest_parser.add_argument("--db-dir", default=DEFAULT_DB_DIR, help="Directory to store the vector database")
    ingest_parser.add_argument("--recursive", action="store_true", default=True, 
                              help="Recursively scan directories for files (default: True)")
    ingest_parser.add_argument("--no-recursive", action="store_false", dest="recursive",
                              help="Do not recursively scan directories")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the documents")
    query_parser.add_argument("question", help="Question to answer")
    query_parser.add_argument("--db-dir", default=DEFAULT_DB_DIR, help="Directory to store the vector database")
    query_parser.add_argument("--raw-chunks", action="store_true", help="Return raw chunks without LLM processing")
    query_parser.add_argument("--num-chunks", type=int, default=4, help="Number of chunks to return (default: 4)")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        ingest_documents(args)
    elif args.command == "query":
        answer_question(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
