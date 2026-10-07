from rag.search import search_legal_provisions


# ============================================================
# RETRIEVAL SETTINGS
# ============================================================

MIN_SIMILARITY_SCORE = 0.50
MIN_SCORE_GAP = 0.015


# ============================================================
# RETRIEVE LEGAL CONTEXT
# ============================================================

def retrieve_legal_context(query: str, top_k: int = 5):
    """
    Retrieve relevant legal provisions for a user query.

    Args:
        query: User's legal question.
        top_k: Number of provisions to retrieve.

    Returns:
        List of retrieved legal provisions.
    """

    if not query or not query.strip():
        return []

    results = search_legal_provisions(
        query=query.strip(),
        top_k=top_k
    )

    return results


# ============================================================
# CHECK RETRIEVAL RELEVANCE
# ============================================================

def check_retrieval_relevance(results: list):
    """
    Check whether the retrieved legal provisions appear
    sufficiently relevant to the user's question.

    This is only a basic safeguard. It does not determine
    legal correctness.
    """

    if not results:
        return False

    # Highest similarity result
    top_score = results[0].get("score", 0.0)

    # Basic minimum similarity check
    if top_score < MIN_SIMILARITY_SCORE:
        return False

    # If multiple results exist, check whether the top result
    # is meaningfully stronger than the weakest retrieved result.
    if len(results) >= 2:

        second_score = results[1].get("score", 0.0)

        score_gap = top_score - second_score

        # A very small gap means the retrieval is not clearly
        # identifying one strong result.
        #
        # We do NOT reject solely because of a small gap here,
        # because multiple legal provisions can legitimately
        # have similar relevance.

        if score_gap < MIN_SCORE_GAP:
            pass

    return True


# ============================================================
# BUILD LEGAL CONTEXT
# ============================================================

def build_legal_context(results: list):
    """
    Convert retrieved legal provisions into a context
    that can later be provided to the LLM.
    """

    if not results:
        return "No relevant legal provisions were found."

    context_parts = []

    for i, result in enumerate(results, start=1):

        metadata = result.get("metadata", {})

        law_name = metadata.get("law_name", "Unknown law")
        provision_type = metadata.get("provision_type", "")
        provision_number = metadata.get("provision_number", "")
        provision_title = metadata.get("provision_title", "")

        legal_text = result.get("text", "")

        source = f"{law_name}"

        if provision_type and provision_number:
            source += f" — {provision_type.title()} {provision_number}"

        if provision_title:
            source += f" — {provision_title}"

        context_parts.append(
            f"""
LEGAL SOURCE {i}
Source: {source}
Similarity Score: {result.get("score", 0):.4f}

Legal Text:
{legal_text}
""".strip()
        )

    return "\n\n".join(context_parts)


# ============================================================
# COMPLETE RAG RETRIEVAL
# ============================================================

def retrieve_and_build_context(query: str, top_k: int = 5):
    """
    Complete RAG retrieval step.

    User Query
        ↓
    Sentence Transformer
        ↓
    FAISS Retrieval
        ↓
    Relevance Check
        ↓
    Legal Context
    """

    results = retrieve_legal_context(
        query=query,
        top_k=top_k
    )

    # --------------------------------------------------------
    # RELEVANCE CHECK
    # --------------------------------------------------------

    is_relevant = check_retrieval_relevance(results)

    if not is_relevant:

        return {
            "query": query,
            "results": [],
            "context": (
                "The available legal sources do not provide "
                "enough relevant information to answer this "
                "question accurately."
            ),
            "relevant": False
        }

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context = build_legal_context(results)

    return {
        "query": query,
        "results": results,
        "context": context,
        "relevant": True
    }


# ============================================================
# DIRECT RAG TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LEGAL AID PROVIDER - RAG SERVICE TEST")
    print("=" * 60)

    query = input("\nEnter your legal question: ").strip()

    if not query:
        print("\nNo question entered.")
        exit()

    rag_result = retrieve_and_build_context(
        query=query,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("RETRIEVED LEGAL CONTEXT")
    print("=" * 60)

    print(rag_result["context"])

    print("\n" + "=" * 60)
    print("RELEVANCE STATUS")
    print("=" * 60)

    print("Relevant:", rag_result["relevant"])

    print("\n" + "=" * 60)
    print("RAG RETRIEVAL COMPLETED")
    print("=" * 60)