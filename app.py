import streamlit as st
import os
from pathlib import Path
import chat

# Set page config
st.set_page_config(
    page_title="LLM Chat Interface",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant","content":"Welcome to the project information system! What do you want to know about my projects?"}]
if "current_path" not in st.session_state:
    st.session_state.current_path = "heliosraz"
if "model" not in st.session_state:
    @st.cache_resource
    def load_model():
        return chat.ChatLLM()
    st.session_state.model = load_model()


# Function to get all files in heliosraz directory
def get_files(directory: str="heliosraz"):
    if os.path.isfile(directory):
        return []
    base_path = Path(directory)
    items = set()
    for item in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, item)):
            items.add(item)
        else:
            items.add(os.path.join(directory.split("/")[-1], item))
    if directory != "heliosraz":
        items.add("..")
    return sorted(list(items))

def navigate_to(path):
    try:
        if path == "..":
            # Go up one directory
            st.session_state.current_path = os.path.dirname(st.session_state.current_path)
        else:
            # Navigate into the selected directory
            st.session_state.current_path = os.path.join(st.session_state.current_path, path)
    except FileNotFoundError:
        navigate_to("/".join(path.split("/")[:-1]))

# Sidebar for file search
with st.sidebar:
    st.title("File Search")
    st.text_input("Current path", st.session_state.current_path, disabled=True)
    
    # Get and filter files
    filtered_files = get_files(st.session_state.current_path)
    
    # Display files
    st.write(f"Found {len(filtered_files)} files")
    for file in filtered_files:
        if st.button(f"{file}", key=f"btn_{file}"):
            navigate_to(file)
            st.rerun()

# Main chat interface
st.title("Project Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        response = st.session_state.model.generate(st.session_state.messages)
        st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
