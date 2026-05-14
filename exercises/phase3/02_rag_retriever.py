"""
Phase 3 - Part A Exercise 2: RAG in LangChain
Wraps RAGRetriever as a LangChain BaseRetriever and plugs it into create_retrieval_chain.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import List

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough

from src.data.loader import DataLoader
from src.rag.embeddings import EmbeddingsGenerator
from src.rag.retriever import RAGRetriever

load_dotenv()


class PerfumeRetriever(BaseRetriever):
    """Wraps RAGRetriever as a LangChain BaseRetriever."""

    rag_retriever: RAGRetriever

    def _get_relevant_documents(self, query: str) -> List[Document]:
        results = self.rag_retriever.semantic_search(query, top_k=5)
        return [
            Document(
                page_content=f"{r.get('brand', '')} {r.get('name', '')}. Notes: {r.get('notes', '')}",
                metadata={"id": r.get("id", ""), "score": r.get("similarity_score", 0)},
            )
            for r in results
        ]


def format_docs(docs: List[Document]) -> str:
    """Concatenate document page_content for prompt injection."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    """Build LCEL RAG chain: PerfumeRetriever → prompt → Claude → str."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_loader = DataLoader(os.path.join(root, "data", "raw", "fragrantica.csv"))
    data_loader.load_data()

    embeddings_gen = EmbeddingsGenerator()
    rag = RAGRetriever(embeddings_gen, data_loader)
    rag.build_index(data_loader.get_all_perfumes())

    retriever = PerfumeRetriever(rag_retriever=rag)

    model = ChatAnthropic(model="claude-sonnet-4-6")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Eres experto en perfumes. Usa este contexto para responder:\n\n{context}"),
            ("human", "{question}"),
        ]
    )

    # LCEL pipe: retriever → format → prompt → model → parser
    chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | model | StrOutputParser()

    return chain


if __name__ == "__main__":
    chain = build_rag_chain()
    result = chain.invoke("Recomienda un perfume floral de verano")
    print("Respuesta:", result)
