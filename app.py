import streamlit as st
from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import CodeGenerationModel
import google.auth

credentials = google.auth.default()
     
st.title('Dragon\'S Den')

# prompt = "Can you write code"
prompt = st.chat_input("Write something")

vertexai.init(project="balmy-elevator-394120", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 1024
}
model = CodeGenerationModel.from_pretrained("code-bison@001")
response = model.predict(
    prefix = "{prompt}",
    **parameters
)

with st.chat_message("A"):
    st.write(prompt)

if prompt:
    with st.chat_message("user"):
        st.write(f"Response from Model: {response.text}")