import streamlit as st
from exa_py import Exa

def get_attr(obj, attr_name):
    """Helper function to get attribute using dot notation or return None if it does not exist."""
    return getattr(obj, attr_name, None)

def process_search_results(response):
    try:
        # Extract the list of results from the response
        results = response.results if hasattr(response, 'results') else []

        # Initialize a list to store processed data
        processed_results = []

        # Loop through each result and extract the desired information
        for result in results:
            title = get_attr(result, 'title')
            url = get_attr(result, 'url')
            id_ = get_attr(result, 'id')
            score = get_attr(result, 'score')
            published_date = get_attr(result, 'publishedDate')
            author = get_attr(result, 'author')
            text = get_attr(result, 'text')
            highlights = get_attr(result, 'highlights')
            highlight_scores = get_attr(result, 'highlightScores')
            summary = get_attr(result, 'summary')

            # Store the processed result in a dictionary
            processed_results.append({
                'title': title,
                'url': url,
                'id': id_,
                'score': score,
                'published_date': published_date,
                'author': author,
                'text': text,
                'highlights': highlights,
                'highlight_scores': highlight_scores,
                'summary': summary
            })
            
        # Return the processed results
        return processed_results

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        return []


def main():
    st.title("Phrase Filters: Niche Company Finder")
    st.markdown("<style> .result-container { margin-bottom: 2rem; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; } .result-title { font-size: 1.2rem; font-weight: bold; color: #2c3e50; } .result-url { color: #2980b9; } .result-field { margin-top: 0.5rem; } </style>", unsafe_allow_html=True)

    # Step 1: API Key Inputs
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    exa_api_key = st.text_input("Enter your Exa API key:", type="password")

    if not openai_api_key or not exa_api_key:
        st.warning("Please enter both API keys to proceed.")
        st.stop()

    # Initialize the Exa API client
    exa = Exa(exa_api_key)

    # Step 2: Company Details Inputs
    company_suffix = st.text_input("Enter the company suffix (e.g., GmbH, Ltd):")
    company_description = st.text_area("Enter the company description:")

    if st.button("Generate Information"):
        if not company_suffix or not company_description:
            st.error("Please fill in both the company suffix and description.")
        else:
            try:
                # Generate the result using the Exa API
                response = exa.search_and_contents(
                    company_description,
                    type="neural",
                    use_autoprompt=True,
                    num_results=10,
                    text=True,
                    include_text=[company_suffix]
                )
                
                # Process the response to extract relevant data
                processed_results = process_search_results(response)

                if processed_results:
                    st.success("Results generated successfully!")
                    st.write("Similar Companies:")

                    # Display each result with styling
                    for result in processed_results:
                        st.markdown(f"""
                            <div class="result-container">
                                <div class="result-title">Title: {result['title'] if result['title'] else 'None'}</div>
                                <div class="result-field">URL: <a href="{result['url'] if result['url'] else '#'}" class="result-url">{result['url'] if result['url'] else 'None'}</a></div>
                                <div class="result-field">ID: {result['id'] if result['id'] else 'None'}</div>
                                <div class="result-field">Score: {result['score'] if result['score'] else 'None'}</div>
                                <div class="result-field">Published Date: {result['published_date'] if result['published_date'] else 'None'}</div>
                                <div class="result-field">Author: {result['author'] if result['author'] else 'None'}</div>
                                <div class="result-field">Text: {result['text'] if result['text'] else 'None'}</div>
                                <div class="result-field">Highlights: {result['highlights'] if result['highlights'] else 'None'}</div>
                                <div class="result-field">Highlight Scores: {result['highlight_scores'] if result['highlight_scores'] else 'None'}</div>
                                <div class="result-field">Summary: {result['summary'] if result['summary'] else 'None'}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No results found.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()