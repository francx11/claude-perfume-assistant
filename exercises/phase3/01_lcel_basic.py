"""
Phase 3 - Part A Exercise 1: LCEL Basic Chain
Equivalent to OrchestratorAgent.process_query() but using LangChain pipe syntax.
"""

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatAnthropic(model="claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a perfume expert. Give concise, helpful recommendations."), ("human", "{question}")]
)

# LCEL pipe: prompt → model → parser
chain = prompt | model | StrOutputParser()

if __name__ == "__main__":
    result = chain.invoke({"question": "Recommend a fresh summer perfume"})
    print(result)
