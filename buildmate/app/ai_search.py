from app.fetch_webpage_content import fetch_webpage_content
from app.perform_search import perform_search
from app.call_gemini import GeminiClient


def ai_search(problem_context: str) -> str:
    gemini = GeminiClient()
    """
    Performs an AI-guided, multi-step search and augmentation of the initial context.

    Steps:
        1. Summarize the code problem.
        2. Generate a query.
        3. Perform a search via Brave API
        4. Select most relevant links based on title and summary
        5. Extract plain text from the links
        6. Extract a summary of useful information from the website
        7. Return useful results that can aid the agent.

    Args:
        problem_context: Initial problem description.

    Returns:
        Original context appended with synthesized, useful information.
    """
    print("--- Starting AI Guided Search Process ---")
    current_context = problem_context

    synthesis_instruction = (
        "You are an expert researcher and technical writer. "
        "Extract only the most critical, actionable information from the provided web content. "
        "Structure it clearly, using bullet points and bolding for readability."
    )

    # Step 2: Summarize the problem
    print("\n[Step 2/7] Summarizing the problem...")
    problem_summary = gemini.generate(
        prompt="Summarize the core problem and the user's ultimate goal in a single paragraph.",
        context=current_context
    )
    print(f"-> Problem Summary: {problem_summary}")

    # Step 3: Generate search query
    print("\n[Step 3/7] Generating search query...")
    search_query = gemini.generate(
        prompt=(
            f"Based on this problem summary: '{problem_summary}', "
            "generate the single best search query that will yield the most useful technical solution. "
            "Only return the query string."
        ),
        context=problem_summary
    )
    print(f"-> Generated Query: {search_query}")
    search_results = perform_search(search_query)

    # Step 4: Select relevant links
    print("\n[Step 4/7] Selecting most relevant links...")
    results_str = "\n".join(
        f"URL: {r['uri']}\nTitle: {r['title']}\nSnippet: {r['snippet']}\n---"
        for r in search_results
    )
    link_selection_response = gemini.generate(
        prompt=(
            "Analyze the following search results and problem summary. "
            "Select and list only the URLs of the top 1-3 most relevant results, one per line."
        ),
        context=problem_summary,
        reference=results_str
    )
    selected_links = [line.strip() for line in link_selection_response.splitlines() if line.strip().startswith("http")]
    print(f"Selected Links: {selected_links}")

    # Step 5: Fetch content
    print("\n[Step 5/7] Fetching webpage content...")
    web_contents = {link: fetch_webpage_content(link) for link in selected_links}

    # Step 6: Synthesize useful information
    print("\n[Step 6/7] Synthesizing useful information...")
    web_content_str = "\n\n---\n\n".join(
        f"Source: {url}\nContent: {content}" for url, content in web_contents.items()
    )
    synthesis_prompt = (
        f"Original Problem Summary: {problem_summary}\n\n"
        f"Webpage Contents for Synthesis:\n{web_content_str}\n\n"
        "Based on the summary and the webpage contents, write a concise, actionable summary "
        "of the useful information and recommendations."
    )
    useful_info = gemini.generate(
        prompt=synthesis_prompt,
        system_instruction=synthesis_instruction
    )
    print("-> Synthesis Complete.")

    # Step 7: Append to original context
    print("\n[Step 7/7] Appending synthesis to original context.")
    final_context = (
        "\n\n======================================================\n"
        "|                 AI SEARCH AUGMENTATION               |\n"
        "======================================================\n\n"
        f"{useful_info}\n\n"
        "======================================================"
    )

    return final_context
