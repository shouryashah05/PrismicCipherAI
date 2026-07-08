import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings # we are using sentence-transformer embedding mode from huggingface
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from htmlTemplates import css, bot_template, user_template



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
           separator="\n",
           chunk_size=1000,
           chunk_overlap=200,
           length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorestore = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vectorestore



def get_conversation_chain(vectorstore):
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Contextualize user's question with chat history
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    retriever = vectorstore.as_retriever()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    
    # Prompt for QA
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know.\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # Create the final retrieval chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.warning("Please process your PDF documents first!")
        return

    response = st.session_state.conversation.invoke({
        "input": user_question,
        "chat_history": st.session_state.chat_history
    })
    st.session_state.chat_history.extend([
        HumanMessage(content=user_question),
        AIMessage(content=response["answer"])
    ])

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)



def main():
    load_dotenv()
    st.set_page_config(page_title="PrismicCipherAI", 
                       page_icon=":✨:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []

    st.header("PrismicCipherAI- Chat with multiple PDFs 📑:")
    user_question = st.text_input("Ask a Question about your document:")
    if user_question:
        handle_userinput(user_question)

    

    with st.sidebar:
       st.subheader("Your Documents")
       pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True) 
       if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                
                # get text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)



if __name__ == "__main__":
    main()