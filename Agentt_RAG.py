

from llmsherpa.readers.file_reader import LayoutPDFReader
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core import ServiceContext

from llama_index.core import SimpleDirectoryReader
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.core import set_global_service_context

from llama_index.core.tools import QueryEngineTool,ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.llms.groq import Groq
from llama_index.llms.openai import OpenAI

from llama_index.core.agent import AgentRunner, ReActAgent
from llama_index.agent.openai import OpenAIAgentWorker, OpenAIAgent
from llama_index.agent.openai import OpenAIAgentWorker

from llama_index.core.agent import ReActAgentWorker,FunctionCallingAgentWorker
from llama_index.core.agent import StructuredPlannerAgent

from langchain import hub
import streamlit as st
import os,constant

os.environ['OPENAI_API_KEY']=constant.OPENAI_API_KEY_PAID
os.environ['LLAMA_CLOUD_API_KEY']=constant.LLAMA_CLOUD_API_KEY
os.environ['GROQ_API_KEY']=constant.GROQ_API_KEY


# llm = Groq(model="llama3-8b-8192", api_key=constant.GROQ_API_KEY)
llm = OpenAI(model="gpt-3.5-turbo")

service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context=service_context)

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"

path1="./annualReport"
path2="./Q3FY24"
path3="./Q2FY24"
path4="./Q1FY24"

pdf_url_1 = "document/AnnualReport.pdf"
pdf_url_2="document/Earning-Deck-Q3FY24.pdf"
pdf_url_3="document/Earning-Deck-Q2FY24-1.pdf"
pdf_url_4="document/Earning-Deck-Q1FY24-1.pdf"

PDFs=[pdf_url_1,pdf_url_2,pdf_url_3,pdf_url_4]
paths=[path1,path2,path3,path4]

file1=SimpleDirectoryReader(input_files=[pdf_url_1]).load_data()
file2=SimpleDirectoryReader(input_files=[pdf_url_2]).load_data()
file3=SimpleDirectoryReader(input_files=[pdf_url_3]).load_data()
file4=SimpleDirectoryReader(input_files=[pdf_url_4]).load_data()

def AnnualReport(name,documents):
    if not os.path.exists(name):
        vector_index=VectorStoreIndex.from_documents(documents)
        vector_index.storage_context.persist(persist_dir=name)
    else:
        vector_index=load_index_from_storage(
            StorageContext.from_defaults(persist_dir=name)
        )

    query_engine = vector_index.as_query_engine(similarity_top_k=3, llm=llm)
    query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="Annual Report",
            description=(
                "Provides information about Mastek Ltd Annual Report and company details"
                "An annual report is a comprehensive report on a company's activities throughout the preceding year. "
                "Annual reports are intended to give shareholders and other interested people information about the company's activities and financial performance. "
            ),
        ),
    )
    return query_engine_tool


def get_tool(name, full_name, documents=None):
    if not os.path.exists(name):
        vector_index = VectorStoreIndex.from_documents(documents)
        vector_index.storage_context.persist(persist_dir=name)
    else:
        vector_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=name),
        )
    query_engine = vector_index.as_query_engine(similarity_top_k=3, llm=llm)
    query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name=full_name,
            description=(
                "Provides information about Mastek Ltd quarterly financials ending"
                f" {full_name}"
            ),
        ),
    )
    return query_engine_tool


Q3FY24 = get_tool(path2, "Q3FY24", documents=file2)
Q2FY24 = get_tool(path3, "Q2FY24", documents=file3)
Q1FY24 = get_tool(path4, "Q1FY24", documents=file4)

annualReport=AnnualReport(path1,documents=file1)

query_engine_tools = [annualReport,Q1FY24,Q2FY24,Q3FY24]

# agent = OpenAIAgent.from_tools(query_engine_tools, llm=llm, verbose=True)
agent = ReActAgent.from_tools(
    query_engine_tools,
    llm=llm,
    verbose=True,
)

response = agent.chat("What is EBITA growth over each Quarter (Q1FY24, Q2FY24, Q3FY24)?")

print(response)