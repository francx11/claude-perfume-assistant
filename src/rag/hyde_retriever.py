"""HyDE (Hypothetical Document Embeddings) wrapper for any semantic retriever."""

from typing import Any, Dict, List


class HyDERetriever:
    """Wraps any retriever with HyDE: generates a hypothetical doc before searching."""

    def __init__(self, retriever, claude_client):
        self.retriever = retriever
        self.claude_client = claude_client

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Generate hypothetical doc from query then delegate to wrapped retriever."""
        hypothetical_doc = self._generate_hypothetical(query)
        return self.retriever.semantic_search(hypothetical_doc, top_k)

    def _generate_hypothetical(self, query: str) -> str:
        """Generate a hypothetical perfume description for the given query."""
        system = (
            "Eres un experto en perfumería. Describe en 2-3 frases un perfume real con notas, "
            "familia olfativa y ocasión. Solo la descripción, sin introducción."
        )
        response = self.claude_client.send_message(
            messages=[{"role": "user", "content": f"Describe un perfume ideal para: {query}"}],
            system=system,
            max_tokens=200,
        )
        return response["content"][0]["text"]
