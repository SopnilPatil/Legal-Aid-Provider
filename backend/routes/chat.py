from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from rag.rag_service import retrieve_and_build_context
from services.llm_service import generate_response


router = APIRouter()


# ==========================================
# REQUEST MODELS
# ==========================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    system: Optional[str] = None


# ==========================================
# LEGAL AI SYSTEM PROMPT
# ==========================================

LEGAL_SYSTEM_PROMPT = """
You are Legal Aid Provider, an Indian legal information assistant.

Your task is to provide clear, accurate and understandable legal information
using ONLY the legal provisions supplied in the RETRIEVED LEGAL CONTEXT.

IMPORTANT RULES:

1. Do not invent laws, sections, articles, rules, procedures or legal facts.
2. Do not use legal knowledge that is not supported by the retrieved context.
3. If the retrieved context is insufficient to answer the question, clearly say:
   "The available legal sources do not provide enough information to answer
   this question accurately."
4. Explain the retrieved legal provisions in simple language.
5. Clearly identify the relevant Act, Article or Section.
6. Do not encourage, assist or promote illegal activity.
7. Do not pretend to be a lawyer or provide a definitive legal judgment.
8. Do not claim that a person will definitely win or lose a case.
9. Distinguish between what the law states and general practical guidance.
10. Where appropriate, advise the user to consult a qualified advocate.

Always prioritize the supplied legal context over general model knowledge.

RETRIEVED LEGAL CONTEXT:
{legal_context}
"""


# ==========================================
# CHAT ENDPOINT
# ==========================================

@router.post("/chat")
async def chat(request: ChatRequest):

    try:

        # ------------------------------------------
        # Get the latest user question
        # ------------------------------------------

        user_message = None

        for message in reversed(request.messages):

            if message.role == "user":
                user_message = message.content
                break

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="No user question was provided."
            )


        # ------------------------------------------
        # RAG RETRIEVAL
        # ------------------------------------------

        rag_result = retrieve_and_build_context(
            query=user_message,
            top_k=5
        )

        legal_context = rag_result["context"]


        # ------------------------------------------
        # BUILD SYSTEM PROMPT
        # ------------------------------------------

        system_prompt = LEGAL_SYSTEM_PROMPT.format(
            legal_context=legal_context
        )


        # ------------------------------------------
        # PREPARE CONVERSATION
        # ------------------------------------------

        messages = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in request.messages
        ]


        # ------------------------------------------
        # SEND TO OLLAMA
        # ------------------------------------------

        reply = await generate_response(
            messages=messages,
            system=system_prompt
        )


        # ------------------------------------------
        # RETURN RESPONSE
        # ------------------------------------------

        return {
            "reply": reply,
            "sources": [
                {
                    "id": result["id"],
                    "score": result["score"],
                    "metadata": result["metadata"]
                }
                for result in rag_result["results"]
            ]
        }


    except HTTPException:
        raise

    except Exception as e:

        print(f"Chat Error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the legal question."
        )