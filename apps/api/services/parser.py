"""
Simple Document Parser Implementation for Day 1 Corpus Extraction.
Parses text manuals, scanned SOP extracts, table matrices, SVG diagrams, and spec sheets.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from ..domain.schemas import Document, Page, Chunk, DocumentType, RegionBoundingBox

class SimpleDocumentParser:
    """Parses seed files and uploaded documents into structured Document, Page, and Chunk objects."""

    def parse_file(self, file_path: str) -> Tuple[Document, List[Page], List[Chunk]]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = path.name
        doc_id = filename.replace(".", "_").upper()
        doc_type = self._detect_doc_type(filename)
        content = path.read_text(encoding="utf-8", errors="ignore")

        pages, chunks = self._extract_pages_and_chunks(doc_id, filename, doc_type, content)

        doc = Document(
            document_id=doc_id,
            title=self._format_title(filename),
            file_path=str(path),
            document_type=doc_type,
            page_count=len(pages),
            metadata={"filename": filename, "chunk_count": len(chunks)},
        )

        return doc, pages, chunks

    def _detect_doc_type(self, filename: str) -> DocumentType:
        fn = filename.lower()
        if "manual" in fn:
            return DocumentType.MANUAL
        elif "scanned" in fn or "sop" in fn:
            return DocumentType.SCANNED_PDF
        elif "table" in fn or "matrix" in fn:
            return DocumentType.TROUBLESHOOTING_TABLE
        elif "wiring" in fn or "schematic" in fn or fn.endswith(".svg"):
            return DocumentType.WIRING_DIAGRAM
        elif "spec" in fn:
            return DocumentType.SPEC_SHEET
        return DocumentType.MANUAL

    def _format_title(self, filename: str) -> str:
        name = filename.rsplit(".", 1)[0].replace("_", " ").title()
        return name

    def _extract_pages_and_chunks(
        self, doc_id: str, filename: str, doc_type: DocumentType, content: str
    ) -> Tuple[List[Page], List[Chunk]]:
        pages: List[Page] = []
        chunks: List[Chunk] = []

        # Split by explicit page markers (e.g., "### Page 1:", "Page 1 of 2", "Page 1")
        page_splits = re.split(r'(?i)(?:###\s*Page\s*(\d+)|Page\s*(\d+)(?:\s*of\s*\d+)?)', content)

        if len(page_splits) > 1:
            current_page_num = 1
            i = 0
            while i < len(page_splits):
                part = page_splits[i]
                if part is None:
                    i += 1
                    continue
                if part.isdigit():
                    current_page_num = int(part)
                    i += 1
                    continue

                text_part = part.strip()
                if text_part:
                    page_obj = Page(
                        page_id=f"{doc_id}_P{current_page_num}",
                        document_id=doc_id,
                        page_number=current_page_num,
                        text_content=text_part,
                    )
                    pages.append(page_obj)

                    page_chunks = self._chunk_text(doc_id, current_page_num, text_part, doc_type, filename)
                    chunks.extend(page_chunks)
                i += 1
        else:
            # Single page document
            page_obj = Page(
                page_id=f"{doc_id}_P1",
                document_id=doc_id,
                page_number=1,
                text_content=content,
            )
            pages.append(page_obj)
            chunks.extend(self._chunk_text(doc_id, 1, content, doc_type, filename))

        return pages, chunks

    def _chunk_text(
        self, doc_id: str, page_num: int, text: str, doc_type: DocumentType, filename: str
    ) -> List[Chunk]:
        chunks: List[Chunk] = []

        # If SVG / Diagram, parse regions specifically
        if doc_type == DocumentType.WIRING_DIAGRAM or filename.endswith(".svg"):
            region_matches = re.findall(r'Region\s+([A-D])\s*\(([^)]+)\):\s*([^.\n]+)', text)
            if region_matches:
                for region_letter, title, desc in region_matches:
                    chunk_id = f"{doc_id}_P{page_num}_REG_{region_letter}"
                    bbox = self._get_region_bbox(region_letter)
                    chunks.append(
                        Chunk(
                            chunk_id=chunk_id,
                            document_id=doc_id,
                            page_number=page_num,
                            text=f"Region {region_letter} ({title}): {desc}",
                            bounding_box=bbox,
                            metadata={"region_name": f"Region {region_letter}", "title": title},
                        )
                    )

        # Split paragraphs/sections
        sections = [s.strip() for s in text.split("\n\n") if s.strip()]
        for idx, sec in enumerate(sections):
            if len(sec) < 15:
                continue
            chunk_id = f"{doc_id}_P{page_num}_C{idx+1}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=doc_id,
                    page_number=page_num,
                    text=sec,
                    metadata={"section_index": idx},
                )
            )

        return chunks

    def _get_region_bbox(self, region_letter: str) -> RegionBoundingBox:
        coords = {
            "A": RegionBoundingBox(x_min=0.10, y_min=0.10, x_max=0.90, y_max=0.25),
            "B": RegionBoundingBox(x_min=0.10, y_min=0.35, x_max=0.50, y_max=0.50),
            "C": RegionBoundingBox(x_min=0.55, y_min=0.35, x_max=0.80, y_max=0.50),
            "D": RegionBoundingBox(x_min=0.81, y_min=0.35, x_max=0.95, y_max=0.60),
        }
        return coords.get(region_letter, RegionBoundingBox(x_min=0.0, y_min=0.0, x_max=1.0, y_max=1.0))
