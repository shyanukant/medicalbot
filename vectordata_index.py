from src.helper import download_huggingface_embeddings, text_split, load_data
from langchain.vectorstores import Pinecore # vector store form database
import pinecore # vector database
from dotenv import load_dotenv
import os

load_dotenv()

PINCORE_API_KEY  = os.environ.get('PINCORE_API_KEY')
PINCORE_API_ENV = os.environ.get('PINCORE_API_ENV')

# extracted data 
extracted_data = load_data('data/')

text_chunks = text_split(extracted_data)
embeddings = download_huggingface_embeddings()

# initail pincore 
pinecore.init(api_key = PINCORE_API_KEY, environment=PINCORE_API_ENV)

index_name = "text" # enter index name from pincore database

# Create Embeddings for each of the text chunks and storing on pinecore vector database
docsearch = Pinecore.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)


# load data form vecotr database if load
docsearch = Pinecore.from_existing_index(index_name, embeddings)
