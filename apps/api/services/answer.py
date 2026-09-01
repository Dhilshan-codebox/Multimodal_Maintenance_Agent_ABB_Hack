"""
Grounded Answer Generation Service Implementation.
Synthesizes technician troubleshooting answers backed strictly by retrieved evidence items.
"""

from typing import List
from ..domain.schemas import Answer, Evidence, Citation
from .interfaces import AnswerService
from .ingestion import ingestion_service


class GroundedAnswerService(AnswerService):
    """Generates grounded answers with strict citation provenance and safety notes."""

    def generate_answer(self, query: str, evidences: List[Evidence]) -> Answer:
        if not evidences or max((e.score for e in evidences), default=0.0) < 0.25:
            return Answer(
                answer_id="ANS-UNSUPPORTED",
                query=query,
                answer_text="UNSUPPORTED: I could not find grounded evidence in the available maintenance documentation to answer this question.",
                citations=[],
                evidences=[],
                confidence_score=0.0,
                is_supported=False,
                safety_warnings=[],
            )

        citations: List[Citation] = []
        answer_steps: List[str] = []
        safety_warnings: List[str] = [
            "ALWAYS perform Lockout/Tagout (LOTO) prior to opening terminal boxes or performing electrical checks.",
            "Verify zero electrical potential using a calibrated multimeter rated CAT III 1000V.",
        ]

        top_score = max(e.score for e in evidences)

        for idx, ev in enumerate(evidences[:3]):
            doc = ingestion_service.get_document(ev.source_id)
            doc_title = doc.title if doc else ev.source_id

            snippet = ev.text.replace("\n", " ").strip()
            if len(snippet) > 160:
                snippet = snippet[:157] + "..."

            cit = Citation(
                citation_id=f"CIT-{idx+1}",
                evidence_id=ev.evidence_id,
                document_title=doc_title,
                page=ev.page,
                snippet=snippet,
                confidence=ev.score,
            )
            citations.append(cit)

            answer_steps.append(f"• According to [{doc_title}, Page {ev.page}]:\n  {ev.text.strip()}")

        formatted_answer = f"Based on grounded evidence retrieved from official maintenance documentation:\n\n" + "\n\n".join(answer_steps)

        return Answer(
            answer_id=f"ANS-{hash(query) & 0xFFFFFF}",
            query=query,
            answer_text=formatted_answer,
            citations=citations,
            evidences=evidences[:3],
            confidence_score=top_score,
            is_supported=True,
            safety_warnings=safety_warnings,
        )
