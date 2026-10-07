# BNS RAG Dataset

Generated from the uploaded `BNS.pdf` (Bharatiya Nyaya Sanhita, 2023, Act No. 45 of 2023), version stated in the PDF as on 6 October 2025.

## Files
- `bns_sections.json` — 358 section-level records; best source-of-truth dataset.
- `bns_rag.jsonl` — embedding/vector-store ready chunks with metadata.
- `bns_search_chunks.json` — same chunks as a JSON array for inspection.
- `bns_chapters.json` — chapter-to-section mapping.
- `bns_metadata.json` — dataset metadata.
- `bns_validation_report.json` — structural validation.

## Recommended RAG pipeline
1. Load `bns_rag.jsonl`.
2. Embed the `text` field.
3. Store vectors with the `metadata` object.
4. Retrieve top-k chunks using semantic search.
5. Optionally rerank by section/chapter relevance.
6. Generate the answer only from retrieved legal text and show `section` + `source_page_start/end` as citations.

## Important
This dataset does **not** invent cognizable/bailable/court classifications. Those classifications belong to procedural/schedule material such as BNSS schedules and should be joined as a separate source if the legal assistant needs them.
