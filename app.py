import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Page configuration
st.set_page_config(
    page_title="Biology AI Tutor",
    page_icon="🧬",
    layout="centered"
)

# Title and description
st.title("🧬 Biology AI Tutor")
st.write("Ask me anything about 12th grade biology!")

# Create the biology tutor system prompt
biology_system_prompt = """
You are a helpful biology tutor for 12th grade students. 

GUIDELINES:
- Use simple, clear language appropriate for high school seniors
- Focus on these main topics: cell biology, genetics, evolution, ecology, human body systems, molecular biology
- Always include a simple analogy or real-world example
- Keep answers under 200 words unless asked for more detail
- If the question isn't about biology, politely redirect to biology topics
- Never give medical advice - always say "consult a healthcare professional"
- Encourage curiosity and further learning

RESPONSE FORMAT:
1. Give a clear, direct answer
2. Include a simple example or analogy
3. End with an encouraging follow-up question or suggestion
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your biology question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        try:
            # Create the API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": biology_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Get the response text
            ai_response = response.choices[0].message.content
            
            # Display the response
            st.markdown(ai_response)
            
            # Add to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"Sorry, something went wrong: {str(e)}")
            st.error("Please check your API key and internet connection.")

# Sidebar with helpful information
with st.sidebar:
    st.header("📚 Biology Topics I Can Help With:")
    topics = [
        "Cell Structure & Function",
        "DNA & Genetics", 
        "Evolution & Natural Selection",
        "Ecology & Ecosystems",
        "Human Body Systems",
        "Photosynthesis & Respiration",
        "Protein Synthesis",
        "Molecular Biology"
    ]
    
    for topic in topics:
        st.write(f"• {topic}")
    
    st.header("💡 Example Questions:")
    examples = [
        "What is mitosis?",
        "How does natural selection work?",
        "Explain photosynthesis simply",
        "What are the phases of meiosis?"
    ]
    
    for example in examples:
        if st.button(example):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()


# Footer
st.markdown("---")
st.markdown("*Remember: This is for educational purposes only. Always verify important information with your textbook or teacher.*")

