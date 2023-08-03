import streamlit as st
import vertexai
from vertexai.preview.language_models import CodeGenerationModel, CodeChatModel, ChatModel, InputOutputTextPair
import google.auth
import requests
import webbrowser

# Google auth 
credentials = google.auth.default()

context = """In this guide, we learned how to create a simple React library that exports a custom Button component with various styles. We started by setting up a new directory for our React library project and initialized it using npm. Then, we installed the necessary dependencies, including React, prop-types, Babel, Webpack, and CSS loaders, to handle our library's code and assets.

With our project set up, we defined the custom Button component inside a components folder. The Button component accepts props for styling and functionality and has different styles based on the provided "variant" prop. We also created a Button.css file to define the styles for each variant of the button.

To make our library usable in other projects, we exported the Button component from an index.js file. Additionally, we configured Webpack with webpack.config.js to bundle our library into a single JavaScript file. We also added scripts to our package.json file for building and running the library.

Next, we created a sample React app that uses our newly created library. We installed the library by providing the local path to the built library file. Then, we imported and used the Button component in the sample app to create buttons with different styles.

By following these steps, we successfully created a reusable React library containing a custom Button component. This library can be easily integrated into various React projects, allowing us to encapsulate the Button's behavior and"""

# ------------------------- conversation ------------------------------------
def conversationalModel(input):
    vertexai.init(project="balmy-elevator-394120", location="us-central1")
    chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
    chat = chat_model.start_chat()
    result = chat.send_message(input, **parameters)
    return result

# # -------------------------- Promt testing ----------------------------------
def promtModel(input):
    vertexai.init(project="balmy-elevator-394120", location="us-central1")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
    model = CodeGenerationModel.from_pretrained("code-bison@001")
    chat = model.predict(
        prefix = prompt,
        **parameters
    )
    result = chat.send_message(input, **parameters)
    return result

# # ----------------------- with Context -------------------------------------
def contexModel(input):
    vertexai.init(project="balmy-elevator-394120", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat(
        context= context,
    )
    result = chat.send_message(input, **parameters)
    return result


# Set Hedding
st.title('Dragon\'S Den')

# Set Sidebar
with st.sidebar:
    st.title('Team - 2')
    st.write(
        'Deveroper Assistant')
    model = st.radio(
    "Try vertexaAI...",
    ('Conversation','promt','Context','API'))
    
    if model == 'Context':
        context = st.text_area('Context for the Model', placeholder="Input context", height=200)
        enter_button_disabled = not bool(context.strip())
        enter_button = st.button('Add Context', disabled=enter_button_disabled)

# Check if the selected model is different from the previously selected one
if st.session_state.get("selected_model") != model:
    # Clear the chat messages and update the selected model
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state.selected_model = model
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not credentials:
        st.info("Please add your Google Credentails to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if model == 'Conversation':
        response = conversationalModel(prompt)

    if model == 'promt':
        response = promtModel(prompt)
    
    if model == 'Context':
        response = contexModel(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)

if model == 'API':
    # type input
    typeInput = st.text_input("Boilerplate name you want to download: ")

    # destination input
    destinationInput = st.text_input("Destination folder name: ")

    # Submit button
    if typeInput and destinationInput:
        if st.button("Submit"):
            st.write("Boilerplate ", typeInput, "will be setup at /", destinationInput)

        # endpoint
        url = "http://localhost:9091/v1/dragon/generateUrl"

        # Data
        data = {
            'type': 'angular-login-register-dashboard-without-auth' or typeInput, 
            'location': 'test-angular-2' or destinationInput
        }   

        # # POST request
        response = requests.post(url, json=data)

        # Check the response status code
        if response.status_code == 200:
            print("POST request was successful!")
            st.write("Your Application is Ready:", response.text)
            if st.button("Open the app"):
                webbrowser.open_new_tab(response.text)
        else:
            st.write("POST request failed with status code:", response.status_code)