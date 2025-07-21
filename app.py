from flask import Flask, render_template, jsonify, request
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecore # vector store form database
# import pinecore # vector database
from pinecore import Pinecore
from langchain.llms import CTransformers # load models
from langchain.prompts import PromptTemplate
from src.helper import download_huggingface_embeddings
from src.prompt import prompt_template
from dotenv import load_dotenv
import os

PINCORE_API_KEY  = os.environ.get('PINCORE_API_KEY')
PINCORE_API_ENV = os.environ.get('PINCORE_API_ENV')

embeddings = download_huggingface_embeddings()

# initail pincore 
pinecore.init(api_key = PINCORE_API_KEY, environment=PINCORE_API_ENV)
pinecore

index_name = "text" # enter index name from pincore database

# load data form vecotr database if load
docsearch = Pinecore.from_existing_index(index_name, embeddings)

prompt = PromptTemplate(template = prompt_template, input_variables=['context', 'question'])
chain_type_kwargs = {"prompt" : prompt}

llm = CTransformers(model= "model/llama-2-7b.chat.ggmlv3.q4_0", 
                    model_type= "llama", 
                    config = {'max_new_tokens':512, 'temperature': 0.8})

qa = RetrievalQA.from_chain_type(
    llm = llm, 
    chain_type = "stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k':2}), # k means two relwent answers
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

app = Flask()

@app.route('/')
def index():
    return render_template('templates/bot.html')


@app.route('/chat', method=['GET', 'POST'])
def chat():
    msg = request.form['msg']
    print(msg)
    result = qa({'query': msg})
    print("resposne", result['result'])
    return str(result['result'])

if __name__ == '__main__':
    app.run(debug=True)