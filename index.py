# reloader.py
import os
import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, target_script):
        self.target_script = target_script
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.terminate() # or .kill()
            self.process.wait()
        print(f"Starting {self.target_script}...")
        self.process = subprocess.Popen([sys.executable, self.target_script])

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'): # Only react to Python file changes
            print(f"File changed: {event.src_path}. Reloading...")
            self.start_script()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reloader.py <your_script.py>")
        sys.exit(1)

    target_script = sys.argv[1]
    path = "D:\the studio Tech\SM_Handle_RAG_Project\main.py" # Watch current directory

    event_handler = MyHandler(target_script)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Textloader
from langchain_community.document_loaders import pypdfloader



fewshot_prompt = """you are an helpful AI assistant that helps users to find information  """ 

from watchdog.observers import Observer

observer = Observer()

if observer.is_alive():
    observer.stop()
    observer.kill('when the file is changed and saved')

from doc_handler import load_documents, load_unstructured_documents
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

file_path = "D:\the studio Tech\SM_Handle_RAG_Project\documents.pdf" #  load document from the local path for now to load

loader = load_documents(file_path)

print(f"Loaded {len(loader)} documents from {file_path}")

print(f"MetaData of the document: {loader[0].metadata}")

print(f"Content of the document: {loader[0].content} ")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

documents = text_splitter.split_documents(loader)

chunks = [doc.page_content for doc in documents]

print(f"Number of chunks created: {len(chunks)}")

def print_chunks(chunks, num_chunks=5):
    print(f"Printing first {num_chunks} chunks:")
    for i, chunk in enumerate(chunks[:num_chunks]):
        print(f"chunk {i+1}: ")
        print(chunk)

    return chunks[:num_chunks]


def search_chunks(query, chunks, top_k=3, similarity='cosine'):
    # Vectorize the chunks and the query
    vectorizer = TfidfVectorizer().fit(chunks + [query])
    chunk_vectors = vectorizer.transform(chunks)
    query_vector = vectorizer.transform([query])

    if similarity == 'cosine':
        # Cosine similarity
        similarities = (chunk_vectors @ query_vector.T).toarray().flatten()
        norms = np.linalg.norm(chunk_vectors.toarray(), axis=1) * np.linalg.norm(query_vector.toarray())
        similarities = similarities / (norms + 1e-10)
    elif similarity == 'dot':
        # Dot product
        similarities = (chunk_vectors @ query_vector.T).toarray().flatten()
    else:
        raise ValueError("similarity must be 'cosine' or 'dot'")

    # Get top_k most similar chunks
    top_indices = similarities.argsort()[::-1][:top_k]
    results = [(chunks[i], similarities[i]) for i in top_indices]
    return results

# Example usage:
query = "Your search query here"
results = search_chunks(query, chunks, top_k=3, similarity='cosine')
for i, (chunk, score) in enumerate(results):
    print(f"\nResult {i+1} (score: {score:.4f}):\n{chunk}")



insert the document
pdf: via link
qa pairs: via json file
or text file

def inser_pdf_via_link(link):
    
    """
    Insert a PDF document from a given link into the system
    """
    from langchain_community.document_loaders import PyPDFLoader
    
    loader = PyPDFLoader(link)

# Splitting the document into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len # Using len function to calculate the length of the text
)
texts = splitter.split_documents(data)
# print(len(texts))

if not pdf:
    raise ValueError("No PDF document found at the provided link.")
    
    # Process the PDF document
    pdf = loader.load()
    
    # Split the document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(pdf)
    
    # Print the number of chunks created
    print(f"Number of chunks created: {len(documents)}")
    
    return documents

if not qa_pairs:
    raise ValueError("No QA pairs found in the provided JSON file.")
