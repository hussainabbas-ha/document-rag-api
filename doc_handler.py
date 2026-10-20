from langchain_community.document_loaders import Docx2txtloader, pypdfloader, Textloader, unstructured_file_loader

def load_documents(file_path:str)-> list:
    
    """
    Load documents from the various file formats using the langchain community document loaders.

    Args:
        file_path (str): The path to the document file.

    Returns:
        List[Documents]: A list of all Loaded Documents.
    
    """

    if file_path.endswith('.pdf'):
        loader = pypdfloader.PyPDFLoader(file_path)

    elif file_path.endswith('.docs'):
        loader = Docx2txtloader.Docx2txtLoader(file_path)

    elif file_path.endswith('.txt'):
        loader = Textloader.Textloader(file_path)
    
    return loader.load()

def load_unstructured_documents(file_path: str) -> list:
    
    '''
    Load the unstructured documents from the files using the langchain community unstructured file loader
    
    '''
