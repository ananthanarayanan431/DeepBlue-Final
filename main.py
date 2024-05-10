
from llama_index.llms.openai import OpenAI
from llama_index.core.storage import StorageContext
from llama_index.core.response.pprint_utils import pprint_response
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,load_index_from_storage,ServiceContext
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import set_global_service_context

from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.chat_engine import CondenseQuestionChatEngine

import os,constant
import streamlit as st

os.environ['OPENAI_API_KEY']=constant.OPENAI_API_KEY_PAID
os.environ['GROQ_API_KEY']=constant.GROQ_API_KEY

storage_path = "./FullThings"
documents_path = "./document"

llm = Groq(model="llama3-8b-8192", api_key=constant.GROQ_API_KEY)
service_context = ServiceContext.from_defaults(llm=llm)
Settings.embed_model = OpenAIEmbedding(model_name='text-embedding-3-large')
set_global_service_context(service_context)

@st.cache_resource(show_spinner=False)
def initialize():
    if not os.path.exists(storage_path):
        documents = SimpleDirectoryReader('document').load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=storage_path)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=storage_path)
        index = load_index_from_storage(storage_context)
    return index

st.set_page_config(
    page_title="Let's talk to your Company Data",
    page_icon=":company:",
    layout="centered"
)

index = initialize()
memory = ChatMemoryBuffer.from_defaults(token_limit=540000)

def clear_chat_history():
    st.session_state['messages'] = [
        {'role': 'assistant', 'content': "Let's talk to your company data"}
    ]

def main():
    st.title("Talk to your company information")
    st.sidebar.button("Clear chat History", on_click=clear_chat_history)
    if "messages" not in st.session_state.keys():
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Ask me a question !"}
        ]

    # chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    chat_engine = index.as_chat_engine(chat_mode="condense_question",
                                       memory=memory,
                                       # system_prompt=(
                                       #     "You are a chatbot, able to have normal interactions, as well as talk"
                                       #     " about an Mastek Annual Report."
                                       # ),
                                       context_prompt=(
                                           "You are a chatbot, able to have normal interactions, as well as talk"
                                            " about an discussing of Mastek Annual Report."
                                           "Here are the relevant documents for the context:\n"
                                           "{context_str}"
                                           "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
                                       ),
                                       llm=OpenAI(temperature=0.6),
                                       verbose=True)

    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                pprint_response(response, show_source=True)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
main()