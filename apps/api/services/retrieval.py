"""
Grounded Retrieval Service Implementation.
Performs hybrid keyword scoring and document relevance matching across ingested chunks.
"""

import re
from typing import List, Dict, Any
from ..domain.schemas import Evidence, EvidenceType, RetrievalMethod, Chunk
from .interfaces import RetrievalService
from .ingestion import ingestion_service


class GroundedRetrievalService(RetrievalService):
    """Retrieves grounded evidence items from active corpus chunks using keyword & term overlap scoring."""

    def retrieve_evidences(self, query: str, top_k: int = 5) -> List[Evidence]:
        chunks = ingestion_service.get_all_chunks()
        if not chunks:
            return []

        query_terms = set(re.findall(r'\w+', query.lower()))
        scored_evidences: List[Evidence] = []

        for chunk in chunks:
            chunk_text_terms = set(re.findall(r'\w+', chunk.text.lower()))
            if not query_terms:
                continue

            overlap = query_terms.intersection(chunk_text_terms)
            score = len(overlap) / len(query_terms)

            # Boost exact keyword matches relevant to troubleshooting
            important_keywords = ["overload", "reset", "start", "fuse", "relay", "resistance", "95", "96", "stator", "bearing", "vibration", "radial"]
            for kw in important_keywords:
                if kw in query.lower() and kw in chunk.text.lower():
                    score += 0.15

            # Clamp score between 0.0 and 1.0
            final_score = min(max(score, 0.0), 1.0)

            if final_score > 0.15:
                # Determine evidence type
                ev_type = EvidenceType.TEXT
                doc = ingestion_service.get_document(chunk.document_id)
                doc_type_val = doc.document_type.value if doc else ""

                if "table" in doc_type_val or "|" in chunk.text:
                    ev_type = EvidenceType.TABLE
                elif "diagram" in doc_type_val or "region" in chunk.text.lower():
                    ev_type = EvidenceType.DIAGRAM_SYMBOL if chunk.bounding_box else EvidenceType.IMAGE_REGION

                scored_evidences.append(
                    Evidence(
                        evidence_id=f"EVID-{chunk.chunk_id}",
                        source_id=chunk.document_id,
                        page=chunk.page_number,
                        region=chunk.bounding_box,
                        evidence_type=ev_type,
                        text=chunk.text,
                        score=round(final_score, 2),
                        retrieval_method=RetrievalMethod.HYBRID,
                    )
                )

        # Sort by score descending
        scored_evidences.sort(key=lambda e: e.score, reverse=True)
        return scored_evidences[:top_k]
