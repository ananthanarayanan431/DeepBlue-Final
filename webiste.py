
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_groq.chat_models import ChatGroq

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import os,constant

os.environ['OPENAI_API_KEY']=constant.OPENAI_API_KEY_PAID
os.environ['GROQ_API_KEY']=constant.GROQ_API_KEY

from NameLink import LinkReturn

def website():
    def get_vectorstore_from_url(url):

        storage = "./URL content"
        loader = WebBaseLoader(url)
        document = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
        )
        document_chunks = text_splitter.split_documents(document)

        if not os.path.exists(storage):
            vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings(), persist_directory=storage)
        else:
            vector_store = Chroma(persist_directory=storage, embedding_function=OpenAIEmbeddings())

        return vector_store

    def clear_chat_history():
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': "Let's talk to your company data"}
        ]

    def get_context_retriever_chain(vector_store):
        llm = ChatGroq(model="llama3-8b-8192", api_key=constant.GROQ_API_KEY)
        retriever = vector_store.as_retriever()

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user",
             "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])
        retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
        return retriever_chain

    def get_conversational_rag_chain(retriever_chain):
        llm = ChatGroq(model="llama3-8b-8192", api_key=constant.GROQ_API_KEY)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
        return create_retrieval_chain(retriever_chain, stuff_documents_chain)

    def get_response(user_input):
        retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
        conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
        response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_input
        })
        return response['answer']

    def app():
        # st.set_page_config(page_title="Company Home page")
        # st.title("Talk to your Company Home Page")
        with st.sidebar:
            st.header("Settings")
            Company_Name = st.text_input("Company Name:")

        if Company_Name is None or Company_Name == "":
            st.info("Please enter a Company Name")

        else:
            st.sidebar.button("Clear chat History", on_click=clear_chat_history)
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    AIMessage(content="Hello, I am a Mastek bot. How can I help you?"),
                ]
            if "vector_store" not in st.session_state:
                st.session_state.vector_store = get_vectorstore_from_url(LinkReturn(Company_Name))

            user_query = st.chat_input("What's app?")
            if user_query is not None and user_query != "":
                response = get_response(user_query)
                st.session_state.chat_history.append(HumanMessage(content=user_query))
                st.session_state.chat_history.append(AIMessage(content=response))

            for message in st.session_state.chat_history:
                if isinstance(message, AIMessage):
                    with st.chat_message("AI"):
                        st.write(message.content)
                elif isinstance(message, HumanMessage):
                    with st.chat_message("Human"):
                        st.write(message.content)

    app()