import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai


def get_pdf_text(pdf_doc):
    text = ""
    for pdf in pdf_doc:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, model_name, api_key):
    genai.configure(api_key=api_key)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversation_chain(model_name, api_key):
    genai.configure(api_key=api_key)
    
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. 
    If the answer is not in the provided context, just say "answer is not available in the context", don't provide the wrong answer.\n\n
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, model_name, api_key):
    genai.configure(api_key=api_key)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversation_chain(model_name, api_key)
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    st.write("Reply:", response["output_text"])


def main():
    st.set_page_config("Chat PDF Multiple PDF Chat App")
    st.header("Chat With PDF Using Gemini")

    with st.sidebar:
        st.title("Menu:")
        
        
        api_key = st.text_input("Enter your Google API Key", type="password")
        model_name = st.selectbox(
            "Select Gemini Model",
            ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"],
            index=2
        )
        
        pdf_doc = st.file_uploader("Upload PDF files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if not api_key:
                st.warning("Please enter your API key before processing.")
            elif not pdf_doc:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_doc)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks, model_name, api_key)
                    st.success("Done!")

    user_question = st.text_input("Ask a question about the PDF documents:")
    if user_question:
        if not api_key:
            st.warning("Please enter your API key before asking a question.")
        else:
            user_input(user_question, model_name, api_key)


if __name__ == "__main__":
    main()
