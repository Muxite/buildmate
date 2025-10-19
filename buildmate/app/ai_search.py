from app.call_gemini import call_gemini
from app.fetch_webpage_content import fetch_webpage_content
from app.perform_search import perform_search

def ai_search(problem_context):
    """
    Performs an AI-guided, multi-step search and augmentation of the initial context.

    The process follows 7 steps: Summarize -> Search Query -> Perform Search ->
    Select Links -> Fetch Content -> Synthesize -> Append & Return.

    Args:
        problem_context: The initial long string of text describing the problem.

    Returns:
        The original context appended with the synthesized, useful information.
    """
    print("--- Starting AI Guided Search Process ---")

    # 1. Save context (Initial context is saved in problem_context)
    current_context = problem_context

    # Define a custom system instruction for synthesis steps
    synthesis_instruction = (
        "You are an expert researcher and technical writer. Your goal is to extract "
        "only the most critical, actionable information from the provided web content "
        "and structure it clearly to directly solve the original problem summary. "
        "Use bullet points and bolding for readability."
    )

    # --- Step 2: Summarize the problem ---
    print("\n[Step 2/7] Asking Gemini to summarize the initial problem...")
    summary_prompt = "Based on the extensive context provided, summarize the core problem and the user's ultimate goal in a single paragraph."
    problem_summary = call_gemini(summary_prompt, context=current_context)
    print(f"-> Problem Summary: {problem_summary}")

    # --- Step 3: Generate search query and perform search ---
    print("\n[Step 3/7] Asking Gemini for a targeted search query...")
    search_prompt = f"Based on this problem summary: '{problem_summary}', generate the single best search query that will yield the most useful technical solution. Only return the query string."
    search_query = call_gemini(search_prompt, context=problem_summary)

    print(f"-> Generated Query: {search_query}")
    search_results = perform_search(search_query)

    # --- Step 4: Ask Gemini to select good links from the search results ---
    print("\n[Step 4/7] Asking Gemini to select the most relevant links...")
    # Format search results neatly for the LLM
    results_str = "\n".join([
        f"URL: {r['uri']}\nTitle: {r['title']}\nSnippet: {r['snippet']}\n---"
        for r in search_results
    ])

    selection_prompt = (
        "Analyze the following search results and the problem summary. "
        "Select and list only the URLs of the top 1-3 most relevant results. "
        "Do not include any extra text, only the list of URLs, one per line."
    )
    link_selection_response = call_gemini(selection_prompt, context=problem_summary, search_results=results_str)

    # Utility function to parse the LLM response into a clean list of URLs
    selected_links = [
        line.strip()
        for line in link_selection_response.split('\n')
        if line.strip().startswith('http')
    ]
    print(f"-> Selected Links: {selected_links}")

    # --- Step 5: Visit all selected links and get the website results ---
    print("\n[Step 5/7] Fetching content from selected webpages...")
    web_contents = {}  # Changed from Dict[str, str]
    for link in selected_links:
        content = fetch_webpage_content(link)
        web_contents[link] = content

    # Format web contents for the final LLM synthesis
    web_content_str = "\n\n---\n\n".join([
        f"Source: {url}\nContent: {content}"
        for url, content in web_contents.items()
    ])

    # --- Step 6: Ask Gemini to write down useful information ---
    print("\n[Step 6/7] Asking Gemini to synthesize useful information...")
    synthesis_prompt = (
        f"Original Problem Summary: {problem_summary}\n\n"
        "Webpage Contents for Synthesis:\n"
        f"{web_content_str}"
        "\n\nBased on the summary and the webpage contents, write a concise, actionable summary of the useful information and recommendations."
    )

    useful_info = call_gemini(
        synthesis_prompt,
        system_instruction=synthesis_instruction
    )
    print("-> Synthesis Complete. Preparing final context.")

    # --- Step 7: Append to the original context and return ---
    print("\n[Step 7/7] Appending synthesis to original context.")
    final_context = (
            current_context +
            "\n\n======================================================\n"
            "|                 AI SEARCH AUGMENTATION               |\n"
            "======================================================\n\n"
            f"{useful_info}"
            "\n\n======================================================"
    )

    return final_context