# BNSS Production RAG Dataset

This package is organized for a legal RAG pipeline.

- `bnss_production.json`: canonical dataset for database ingestion.
- `bnss_sections.json`: 531 section records.
- `bnss_rag.jsonl`: retrieval records with metadata.
- `bnss_chapters.json`: chapter reference table.
- `bnss_schedules.json`: schedules kept separate from sections.
- `bnss_metadata.json`: dataset manifest.
- `bnss_validation_report.json`: technical QA report.

Important: `text.verbatim` is retained as the source representation. `text.search_text` is only a retrieval-cleaned copy. This package does not add AI-generated legal interpretations. Before public legal deployment, verify the source text against the authoritative current publication and record the source/version/date.
