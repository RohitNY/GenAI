import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

OPENAI_API_KEY=""

st.header("Chatbot");

#upload pdf files
with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("upload a pdf", type="pdf")

#Extract the text
if file is not None:
    pdf_reader = PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()
        #st.write(text)

    #Break it into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    ) 

    chunks = text_splitter.split_text(text)
    #st.write(chunks)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vector_store = FAISS.from_texts(chunks, embeddings)
    #get user question
    user_question = st.text_input("Type your question here")
    #do similarity search
    if user_question:
        match = vector_store.similarity_search(user_question)
        st.write(match)