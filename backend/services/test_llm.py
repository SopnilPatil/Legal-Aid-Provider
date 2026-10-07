import asyncio

from services.llm_service import generate_response


async def main():
    question = "What is the Constitution of India?"

    response = await generate_response(question)

    print("\nLLM RESPONSE:\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())