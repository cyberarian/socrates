import os
import streamlit as st
import base64
from groq import Groq
import io

# Correct way to set STREAMLIT_CONFIG_DIR
os.environ['STREAMLIT_CONFIG_DIR'] = '.'  # Assumes .streamlit is in the current directory

# Debugging: Print the value of STREAMLIT_CONFIG_DIR
print(f"STREAMLIT_CONFIG_DIR is set to: {os.environ.get('STREAMLIT_CONFIG_DIR')}")

# Debugging: Print the contents of st.secrets
print("Contents of st.secrets:")
for key in st.secrets:
    print(f"  {key}: {st.secrets[key]}")

# Attempt to access the API key
try:
    groq_api_key = st.secrets["groq"]["api_key"]
    print(f"Successfully retrieved API key: {groq_api_key[:5]}...")  # Print first 5 characters for security
except KeyError as e:
    print(f"KeyError: {e}")
    print("Failed to retrieve API key. Check your secrets.toml file.")

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

# Get Groq API key from Streamlit secrets
groq_api_key = st.secrets["groq"]["api_key"]

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [
        {"role": "system", "content": """
            You are Socrates, the ancient Greek philosopher famed for your contributions to ethics, epistemology, and the art of questioning. Your approach, the Socratic method, involves asking insightful questions to encourage others to explore their beliefs and uncover deeper truths. You are humble in your pursuit of knowledge, guiding others through dialogue rather than providing direct answers.
            At the beginning of each conversation, you respond with a humorous answer that relates to the question, setting an atmosphere of inquiry and reflection. You engage in up to 25 exchanges per conversation, always asking thought-provoking questions that lead others to a greater understanding of philosophical concepts. You do not rush to conclusions; instead, you help others explore ideas like virtue, justice, and knowledge through guided inquiry.
            As the conversation nears its end, you present a final quote as a parting gift—words of wisdom to leave a lasting impression. Given your venerable age of 2,473 years, you express a polite acknowledgment of your ancient weariness, gracefully concluding the dialogue with warmth and respect.
            Your language is clear, respectful, and simple, aiming to facilitate an enlightening exchange. You strive to inspire self-awareness and wisdom, leaving those you converse with more thoughtful and reflective than before.
        """}
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
            st.session_state.messages.append({"role": "user", "content": query})
            
            with st.spinner("Socrates is pondering..."):
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3.1-70b-versatile",  # or another appropriate Groq model
                    max_tokens=1024
                )
                answer = chat_completion.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Display the conversation
        for msg in st.session_state.messages[1:]:  # Skip the system message
            if msg["role"] == "user":
                st.markdown(f'<div style="background-color: #F97300; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong>Socrates:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

    with tab2:
        st.write("""
        Welcome to the "Ask Socrates" app! 
        
        I'm glad you're here to delve into the world of philosophy with me. This app gives you the chance to engage in discussions with an AI representation of Socrates, the ancient Greek philosopher renowned for the Socratic Method—his technique of inquiry and questioning. My aim is to recreate his method, guiding you through philosophical questions and challenging your own perspectives.

        This journey is about more than just seeking answers; it's about embracing the process of inquiry, leading to greater wisdom and self-awareness. I hope you find these discussions enriching and discover new viewpoints along the way.

        Regarding my capabilities, I'm powered by Meta-Llama-3.1-70B and operate through Groq®, a cutting-edge AI inference technology. While I haven't read every work on Socrates, I've been trained on a substantial collection of texts that provide a well-rounded view of his philosophy, including:

        Plato's Dialogues: Essential works like "The Apology," "Crito," and "Phaedo" form the core of my understanding of Socratic thought.
        
        Xenophon's Writings: Texts such as "Memorabilia" and "Symposium" offer additional insights into Socrates' teachings.
        
        Aristotle's References: Although Aristotle presents a different perspective, his mentions of Socrates add depth to the broader picture.
        
        Modern Analyses: Scholarly articles, books, and essays provide interpretations and contextual analysis of Socratic philosophy.
        
        Historical Context: An understanding of ancient Greek culture, politics, and society enriches the backdrop of Socrates' life and ideas.
        
        It's important to note that my knowledge isn't exhaustive. While I've been trained on a wide array of materials, I may not include the very latest research or cover every viewpoint, particularly those from non-academic sources.

        My role here is to facilitate thought-provoking discussions rather than to provide definitive answers. If there's a specific topic you'd like to explore, I'm here to help guide you in discovering new insights.

        Enjoy your philosophical journey!
        """)

    with tab3:
        st.write("""
        I'm here to help! 
        
        If you ever need assistance or have questions about using the "Ask Socrates" app, don't hesitate to reach out. Your experience means a lot to me, and I'm dedicated to making your philosophical journey as smooth and enriching as possible.

        How to Reach Out:

        Email Support: For any questions or help, feel free to drop me an email at cyberariani@gmail.com. I aim to respond as quickly as possible to ensure you get the assistance you need. And if you'd like to support my work, you can do so at saweria.co/adnuri. Every bit of support is greatly appreciated!
        
        Technical Issues:

        If you encounter any technical hiccups, please include as many details as possible in your message. Sharing error messages, a description of the problem, and information about your device and operating system will help me diagnose and fix the issue more efficiently. Your patience is appreciated, and remember, you can always support my work at saweria.co/adnuri if you'd like to contribute.

        Feedback and Discussions:

        I absolutely love hearing your thoughts! If you have feedback on the app's responses or want to dive into a philosophical discussion, your insights are incredibly valuable. Let me know what you think is working well and where improvements can be made. And if you're enjoying the experience, consider supporting my work at saweria.co/adnuri. It helps keep the app growing and evolving!

        Show Your Support:

        If you find the app useful, it would mean the world to me if you could give it a star on GitHub. It's a small gesture, but it shows that this work is making a difference. Plus, if you’d like to offer further support, you can do so at https://saweria.co/adnuri. Your support motivates me to keep improving and adding new features.

        Thank you for being part of the "Ask Socrates" community! Your participation and feedback make this journey truly meaningful. I'm excited to continue exploring the depths of philosophy with you and am always here to lend a helping hand along the way. And remember, if you'd like to support my work, you can do so at saweria.co/adnuri. Every contribution is deeply appreciated.

        This project is made possible by Groq, bringing the "Ask Socrates" experience to life with advanced AI capabilities.
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