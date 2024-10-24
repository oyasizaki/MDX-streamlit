import streamlit as st
import requests

# Constants
BASE_API_URL = "http://68.183.143.199:7861"
FLOW_ID = "7e8111b0-13b8-45e2-a47b-3f7392715314"
ENDPOINT = ""  # Use the endpoint from your Langflow setup
background_image_url = "https://raw.githubusercontent.com/oyasizaki/MDX/29d0be7b087b6adb22a85677e50fb0a110b1f30b/AI.jpg"  # Replace with your image URL

# Function to run the flow
def run_flow(message: str) -> dict:
    """
    Run a flow with a given message.

    :param message: The message to send to the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT or FLOW_ID}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    response = requests.post(api_url, json=payload)
    return response.json()

# Function to extract the desired message
def extract_message(response: dict) -> str:
    try:
        # Navigate to the message inside the response structure
        return response['outputs'][0]['outputs'][0]['results']['message']['text']
    except (KeyError, IndexError):
        return "No valid message found in response."

# Streamlit App
def main():
    # Set the background image using CSS
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url('https://raw.githubusercontent.com/oyasizaki/MDX/29d0be7b087b6adb22a85677e50fb0a110b1f30b/AI.jpg');
            background-size: cover;
            background-position: center;
            height: 100vh;
            color: white; /* Optional: Change text color for better visibility */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for the footer content
    with st.sidebar:
        st.markdown(
            """
            ### This Chat Interface is developed to provide awareness on the capabilities of Generative AI and the technology stack available to support the Generative AI Ecosystem. You may explore the following tools that have contributed in the development of SHRDC's Generative AI programs:

            - **SHRDC** -[link](https://www.shrdc.org.my/)
            - **Langflow** -[link](https://www.langflow.org/)
            - **Langfuse** -[link](https://langfuse.com/)
            - **Ollama** -[link](https://ollama.com/)
            - **JamAI Base** -[link](https://docs.jamaibase.com/)
            - **LlamaFactory** -[link](https://github.com/hiyouga/LLaMA-Factory)
            - **KNIME Analytics Platform** -[link](https://www.knime.com/knime-analytics-platform)
            - **AMD** -[link](https://www.amd.com/en.html)
            - **OpenAI** -[link](https://openai.com/)

            --------------------------------------------
            ## Event
            - **Programme Book** -[Download](https://mdec.my/static/pdf/mdx/Programme%20Book%20211024.pdf)
            - **MDX** -[link](https://mdec.my/mdx)


            --------------------------------------------

            ## Contact our SHRDC team:
            - **Didie SHRDC** -[WhatsApp](https://wa.me/601115620274)
            - **Farid Aizat MSF Sales** -[WhatsApp](https://wa.me/601111000305)
            - **Dr. Chua** -[WhatsApp](https://wa.me/60122828653)



            ---------------------------------------------



            Developed by SHRDC team in support of the MDX Event to provide awareness on the capabilities of Generative AI.

            ### Developers:
            - **Oyasi** - [LinkedIn](https://www.linkedin.com/in/oyasizakiananta)

            DM for any issues.
            """,
            unsafe_allow_html=True
        )

    st.markdown(
    """
    <h1 style='font-size: 24px;'>SHRDC-Copilot 🤖</h1>
    <p style='font-size: 18px;'>This is a chat interface in development phase to provide information on SHRDC's programs and participating events.
    Currently facilitating questions regarding the MDX 2024.</p>
    """,
    unsafe_allow_html=True
    )
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input box for user message
    if query := st.chat_input("Ask me anything..."):
        # Add user message to session state
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
            }
        )
        with st.chat_message("user"):
            st.write(query)

        # Call the Langflow API and get the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                assistant_response = extract_message(run_flow(query))
                message_placeholder.write(assistant_response)

        # Add assistant response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
            }
        )

if __name__ == "__main__":
    main()
