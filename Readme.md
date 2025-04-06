

# RepoLingo: GitHub Repository Analysis Tool

## Overview
RepoLingo is a Streamlit application designed to extract, analyze, and summarize GitHub repositories in multiple languages. It utilizes the Together AI API for querying repository content and provides features for downloading responses.

## Features
*   **Repository Parsing**: Ingests GitHub repositories using the `gitingest` library.
*   **Multi-Language Support**: Summarizes and queries repository content in various languages, including English, Spanish, French, German, Chinese, Hindi, Urdu, Vietnamese, Thai, Japanese, and Arabic.
*   **Predefined Questions**: Offers a set of predefined questions for analyzing the repository, such as summarizing the repository, suggesting code improvements, and identifying security vulnerabilities.
*   **Custom Questions**: Allows users to input custom questions about the repository.
*   **Model Settings**: Supports selecting different models (e.g., Llama-4-Maverick-17B-128E-Instruct-FP8) and adjusting temperature and max tokens for the API requests.

## Requirements
*   Python 3
*   Streamlit
*   Requests
*   Gitingest

## Usage
1.  Clone the repository.
2.  Install the required packages using `pip install -r requirements.txt`.
3.  Set your Together AI API key in the settings sidebar.
4.  Enter the GitHub repository URL and select the format (JSON).
5.  Click "Parse Repository" to ingest and analyze the repository content.
6.  Choose a question type or enter a custom question and select the response language.
7.  Click "Get Answer" to generate a response.

## API Documentation
The application uses the Together AI API for querying repository content. You can find more information about the API and its usage in the [Together AI documentation](https://docs.together.ai/docs/quickstart).

## Contributing
Contributions are welcome. Please submit a pull request with your changes and a brief description.


## Known Issues
*   Handling large repositories may take significant time and resources.
*   The Together AI API may have usage limits and requirements.

## Future Development
*   Support for more repository formats (e.g., Markdown, HTML).
*   Integration with more AI models and APIs.

## Acknowledgments
RepoLingo was developed using Streamlit, Gitingest, and the Together AI API. Special thanks to the developers of these libraries and services.
