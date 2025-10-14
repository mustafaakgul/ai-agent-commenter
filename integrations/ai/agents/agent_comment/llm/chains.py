from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from .prompts import analysis_prompt, response_prompt, quality_check_prompt

# Chain setup for analysis, response, and quality check
def setup_chains(llm):
    analysis_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages(analysis_prompt),
        verbose=False
    )
    response_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages(response_prompt),
        verbose=False
    )
    quality_chain = LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_messages(quality_check_prompt),
        verbose=False
    )
    return analysis_chain, response_chain, quality_chain
