import streamlit as st
import json
import os
import requests
from gitingest import ingest
import asyncio
from gitingest import ingest_async

st.set_page_config(page_title="RepoLingua", page_icon="📦", layout="wide")

# Languages for summarization and queries
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Hindi": "hi",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Thai": "th",
    "Japanese": "ja",
    "Arabic": "ar",
}

# Predefined questions
PREDEFINED_QUESTIONS = [
    "Summarize repository",
    "How to run the code",
    "Suggest code improvements",
    "Security vulnerabilities and fixes",
    "Custom question"
]

# Available models
MODELS = [
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    "meta-llama/Llama-3.3-70B-Instruct-Turbo"
]

def parse_repository(repo_url, format_type):
    """Parse repository using gitingest."""
    with st.spinner(f"Parsing repository {repo_url}..."):
        try:
            # Use synchronous version for simplicity
            summary, tree, content = ingest(repo_url)
            
            if format_type == "JSON":
                # Create a JSON structure that includes all data
                result = {
                    
                    "content": content
                }
                return json.dumps(result, indent=2)
            else:
                # Create a plain text representation
                text_output = f"# File Contents\n"
                for path, file_content in content.items():
                    text_output += f"\n## {path}\n```\n{file_content}\n```\n"
                
                return text_output
                
        except Exception as e:
            st.error(f"Error parsing repository: {str(e)}")
            return None

def query_repository(repo_content, question, language="English", model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", temperature=0.3, max_tokens=1500):
    """Query repository content using Together AI API."""
    api_key = os.environ.get("TOGETHER_API_KEY") or st.session_state.get("together_api_key")
    
    if not api_key:
        st.error("Together AI API key not found. Please enter it in the settings.")
        return None
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    if isinstance(repo_content, str) and repo_content.startswith("{"):
        try:
            repo_data = json.loads(repo_content)
            content_str = json.dumps(repo_data, indent=2)
        except:
            content_str = repo_content
    else:
        content_str = repo_content
    
    prompt = f"""<s>[INST] <<SYS>> You are a senior developer assistant. Analyze this codebase and answer the following question in {language}. IMPORTANT: You must answer the question in {language}.<</SYS>>

Repository Structure:
{content_str}

Question: {question}

Provide output in Markdown format with clear section headers where appropriate. [/INST]"""

    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    with st.spinner("Generating response..."):
        try:
            response = requests.post("https://api.together.xyz/v1/completions", 
                                    headers=headers, 
                                    json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['text']
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"Error calling Together AI API: {str(e)}")
            return None

def main():
    st.title("RepoLingua")
    st.write("Extract, analyze and summarize GitHub repositories in multiple languages")
    
    # Check for Together API key
    if "together_api_key" not in st.session_state:
        st.session_state.together_api_key = os.environ.get("TOGETHER_API_KEY", "")
    
    # Initialize session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = MODELS[0]
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = 1500
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.3
    
    # API key and model settings
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Together API Key", 
                              value=st.session_state.together_api_key,
                              type="password")
        if api_key:
            st.session_state.together_api_key = api_key
            
        st.subheader("Model Settings")
        st.session_state.selected_model = st.selectbox(
            "Model",
            options=MODELS,
            index=MODELS.index(st.session_state.selected_model)
        )
        
        st.session_state.max_tokens = st.slider(
            "Max Tokens",
            min_value=500,
            max_value=3000,
            value=st.session_state.max_tokens,
            step=100
        )
        
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )
    
    # Main input area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo-name")
    
    with col2:
        format_type = st.selectbox("Format", ["JSON"])
    
    if st.button("Parse Repository", disabled=not repo_url):
        content = parse_repository(repo_url, format_type)
        
        if content:
            st.session_state.repo_content = content
            st.session_state.format_type = format_type
            st.session_state.repo_url = repo_url
    
    # Display content if available
    if 'repo_content' in st.session_state:
        st.subheader("Repository Content Preview")
        
        with st.expander("Preview", expanded=False):
            preview_height = 300  # Fixed height preview with scrolling
            if st.session_state.format_type == "JSON":
                try:
                    parsed_json = json.loads(st.session_state.repo_content)
                    st.json(parsed_json)
                except json.JSONDecodeError:
                    st.text_area("Raw Content", st.session_state.repo_content, height=preview_height)
            else:
                st.markdown(st.session_state.repo_content)
        
        # Download button
        file_extension = "json" if st.session_state.format_type == "JSON" else "txt"
        
        st.download_button(
            label=f"Download as {file_extension.upper()}",
            data=st.session_state.repo_content,
            file_name=f"repository.{file_extension}",
            mime=f"application/{file_extension}" if file_extension == "json" else "text/plain"
        )
        
        # Repository Q&A section
        st.subheader("Ask Questions About the Repository")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            selected_language = st.selectbox("Response Language", list(LANGUAGES.keys()))
        
        with col1:
            question_type = st.selectbox("Question Type", PREDEFINED_QUESTIONS)
            
            if question_type == "Custom question":
                custom_question = st.text_input("Enter your question")
                question = custom_question
            else:
                question = question_type
        
        if st.button("Get Answer", disabled=not question):
            response = query_repository(
                st.session_state.repo_content, 
                question, 
                selected_language,
                st.session_state.selected_model,
                st.session_state.temperature,
                st.session_state.max_tokens
            )
            
            if response:
                st.session_state.repo_response = response
                st.session_state.response_language = selected_language
                st.session_state.current_question = question
        
        # Display response if available
        if 'repo_response' in st.session_state:
            st.markdown(st.session_state.repo_response)
            
            # Download response button
            st.download_button(
                label=f"Download Response",
                data=st.session_state.repo_response,
                file_name=f"repository_response_{LANGUAGES[st.session_state.response_language]}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()