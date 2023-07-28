import streamlit as st
from google.cloud import aiplatform
import vertexai
# from langchain.llms import VertexAI
from vertexai.preview.language_models import CodeGenerationModel, CodeChatModel
import google.auth

credentials = google.auth.default()
     
st.title('Dragon\'S Den')

# Set Sidebar
with st.sidebar:
    st.title('Team - 2')
    st.write(
        'Deveroper Assistant')
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not credentials:
        st.info("Please add your Google Credentails to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

#     vertexai.init(project="balmy-elevator-394120", location="us-central1")
#     parameters = {
#         "temperature": 0.2,
#         "max_output_tokens": 1024
#     }
#     model = CodeGenerationModel.from_pretrained("code-bison@001")
#     response = model.predict(
#         prefix = prompt,
#         **parameters
#     )

    vertexai.init(project="balmy-elevator-394120", location="us-central1")
    chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
    chat = chat_model.start_chat()
    # print(f"Response from Model: {response.text}")
    response = chat.send_message(prompt, **parameters)
    

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
