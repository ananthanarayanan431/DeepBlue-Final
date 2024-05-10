

from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
import os

import constant

os.environ['TAVILY_API_KEY'] = constant.TAVILY_API_KEY
os.environ['OPENAI_API_KEY'] = constant.OPENAI_API_KEY

def get_profile_url(name:str)->str:
    """Searches for company home profile page and return any 10 profile to related to company"""
    search=TavilySearchAPIWrapper()
    result=TavilySearchResults(api_wrapper=search)
    res=result.run(f"{name}")
    return res

def LinkReturn(companyName):
    res=[]
    for i in get_profile_url(companyName):
        res.append(i['url'])
    return res