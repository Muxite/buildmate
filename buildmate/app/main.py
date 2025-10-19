from app.ai_search import ai_search

if __name__ == "__main__":
    # Example problem context
    problem_context = """
    I am trying to learn about high-concurrency Python programming. 
    I want to understand alternatives to asyncio, including libraries like Gevent and Eventlet,
    and how to use them effectively in real-world applications.
    """

    print("=== Running AI Search Test ===")
    final_result = ai_search(problem_context)

    print("\n=== AI Search Augmented Context ===")
    print(final_result)
