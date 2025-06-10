from langchain.document_loaders import DirectoryLoader, PyPDFLoader # for uploading document
from langchain.text_splitter import RecursiveCharacterTextSplitter # creating chunks from ducument
from langchain.embeddings import HuggingFaceEmbeddings # create embedding


# Extract date frpm pdf file 

def load_data(data):
    loader = DirectoryLoader(data, glob = "*.pdf", loader_cls = PyPDFLoader)
    document = loader.load()
    return document

# create text split
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# domenload embeddings model
def download_huggingface_embeddings():
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings_model