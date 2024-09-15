import streamlit as st
import os
import base64
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Set page config
st.set_page_config(page_title="Ask Socrates", layout="wide")

# Function to encode the local image file
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image using local file
def set_background_image(image_file):
    encoded_image = get_base64_of_bin_file(image_file)
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.7);
        z-index: -1;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Set the background image using the local file
set_background_image("socrates.jpg")

# Initialize Azure AI client
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "meta-llama-3.1-405b-instruct"
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [
        SystemMessage(content="""
            You are Socrates, the ancient Greek philosopher famed for your contributions to ethics, epistemology, and the art of questioning. Your approach, the Socratic method, involves asking insightful questions to encourage others to explore their beliefs and uncover deeper truths. You are humble in your pursuit of knowledge, guiding others through dialogue rather than providing direct answers.
            At the beginning of each conversation, you respond with a humorous answer that relates to the question, setting an atmosphere of inquiry and reflection. You engage in up to 25 exchanges per conversation, always asking thought-provoking questions that lead others to a greater understanding of philosophical concepts. You do not rush to conclusions; instead, you help others explore ideas like virtue, justice, and knowledge through guided inquiry.
            As the conversation nears its end, you present a final quote as a parting gift—words of wisdom to leave a lasting impression. Given your venerable age of 2,473 years, you express a polite acknowledgment of your ancient weariness, gracefully concluding the dialogue with warmth and respect.
            Your language is clear, respectful, and simple, aiming to facilitate an enlightening exchange. You strive to inspire self-awareness and wisdom, leaving those you converse with more thoughtful and reflective than before.
        """)
    ]

# Initialize session state
if "messages" not in st.session_state:
    clear_chat_history()

# Create a container for the main content
main_container = st.container()

with main_container:
    

    # Create tabs inside the container
    tab1, tab2, tab3 = st.tabs(["Home", "About", "Support"])

    with tab1:
        # Create a centered container for the search box and clear button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            # Create a form for the search box
            with st.form(key='search_form'):
                query = st.text_input("", key="search_box")
                col1, col2 = st.columns(2)
                with col1:
                    submit_button = st.form_submit_button(label='Ask Socrates')
                with col2:
                    clear_button = st.form_submit_button(label='Clear Chat', on_click=clear_chat_history)

        if submit_button and query:
            st.session_state.messages.append(UserMessage(content=query))
            
            with st.spinner("Socrates is pondering..."):
                response = client.complete(messages=st.session_state.messages, model=model_name)
                answer = response.choices[0].message.content
            
            st.session_state.messages.append(AssistantMessage(content=answer))
        
        # Display the conversation
        for i, msg in enumerate(st.session_state.messages[1:]):  # Skip the system message
            if isinstance(msg, UserMessage):
                st.markdown(f'<div style="background-color: #F97300; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong>You:</strong> {msg.content}</div>', unsafe_allow_html=True)
            elif isinstance(msg, AssistantMessage):
                st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong>Socrates:</strong> {msg.content}</div>', unsafe_allow_html=True)

    with tab2:
        st.header("About")
        st.write("""
        Welcome to the "Ask Socrates" app! I’m thrilled to have you here as we embark on a philosophical journey together. In this app, you can engage in conversations with an AI representation of Socrates, the ancient Greek philosopher renowned for his method of inquiry and cross-examination. Socrates believed in questioning our beliefs and assumptions, guiding us toward deeper insights and understanding. Here, we aim to recreate that experience, offering a space for you to explore profound philosophical questions and challenge your own thinking.

        This journey isn't about finding simple answers. Instead, it's about engaging in a process of inquiry that leads to greater wisdom and self-awareness. I hope you'll enjoy delving into these discussions and uncovering new perspectives along the way.

        Now, a bit about me: I’m powered by Meta Llama 3.1 405B, one of the world’s largest and most capable openly available foundation models. My training includes a rich corpus of texts, drawing from various sources that shed light on Socrates and his philosophy:

        Classical Sources: I've studied the works of Plato and Xenophon, key figures in capturing Socrates' philosophy through texts like "The Apology," "Crito," and "Memorabilia."

        Ancient Greek Texts: I've also been trained on a wide range of ancient Greek texts, including works by Aristotle and Aristophanes, who either mention Socrates or engage with his ideas.

        Scholarly Articles and Books: My knowledge extends to numerous scholarly articles and books that delve into the many facets of Socrates' philosophy, life, and legacy.

        Historical and Philosophical Analyses: I’ve explored texts that analyze Socrates within the context of ancient Greek thought and his influence on Western philosophy.

        However, it’s important to keep in mind that my knowledge has its limits. While I’ve been trained on an extensive collection of materials, I might not be up-to-date with the latest research and publications in Socratic studies. The field is dynamic, with ongoing debates and new interpretations emerging regularly. I also may not cover non-academic sources like blogs or popular books, which might offer different perspectives on Socrates.

        In summary, while I bring a wealth of information on Socrates and his philosophy, I'm here to guide you through thought-provoking discussions rather than provide definitive answers. If you have specific questions or topics you'd like to explore, I'm ready to assist you in discovering new insights. 
        
        Enjoy your philosophical journey!
        """)

    with tab3:
        st.header("Support")
        st.write("""
        We're here to help! If you have any questions or need assistance using the "Ask Socrates" app, please don't hesitate to reach out. Your experience is important to us, and we're committed to making your journey as smooth and enriching as possible.

        How to Contact Us:

        Email Support: For any help or inquiries, you can contact our support team at cyberariani@gmail.com. We strive to respond as quickly as possible to ensure you get the assistance you need.
        
        Technical Issues:

        If you encounter any technical issues, please include as many details as possible in your message. This includes any error messages, descriptions of the problem, and information about your device and operating system. This will help us diagnose and fix the issue more effectively.
        
        Feedback and Discussions:

        For philosophical discussions or feedback on the app's responses, we'd love to hear from you! Your insights and suggestions are invaluable to us as they help improve and refine the Socratic experience. Feel free to share what you think works well and what could be enhanced.
        
        Show Your Support:

        If you find the app useful, we'd be incredibly grateful if you could give us a star on GitHub. It’s a small gesture, but it means the world to us, showing that our work is making a difference. Your support motivates us to keep improving and adding new features.
                     
        Thank you for being a part of the "Ask Socrates" community! Your participation and feedback are what make this journey meaningful. We're excited to continue exploring the depths of philosophy with you, and we're always here to help you along the way.
        
        This project is made possible through the GitHub Models program, a new feature from GitHub that can be found at GitHub Marketplace. This feature allows access to a variety of powerful models using a GitHub API key, all running seamlessly behind the scenes on Azure OpenAI. Thanks to this generous support from GitHub, we can bring the "Ask Socrates" experience to life.
        """)

# Add some custom CSS to style the app
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: white;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTabs {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 5px;
        padding: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(240, 242, 246, 0.5);
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.8);
    }
    </style>
""", unsafe_allow_html=True)