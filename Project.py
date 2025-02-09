import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from groq import Groq
from dotenv import load_dotenv
import os
from PIL import Image

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Load local image
image_path = r"16304154_TaeJune15.jpg"  # Make sure this file is in your project folder

# Function to call Groq API
def groq_chat(prompt, system_prompt=""):
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

# Streamlit App Config
st.set_page_config(page_title="AI Multi-Usecase App", layout="wide")
st.sidebar.image(Image.open(image_path).resize((200, 100)), caption="AI-Powered App", use_column_width=False)
st.sidebar.title("🔮 Multi-Usecase AI App")
st.sidebar.markdown("💡 **Explore AI-powered tools for productivity!**")
option = st.sidebar.radio(
    "📌 Select a Feature:",
    ["Fake News Detection", "Advanced Translation", "Data Visualization", "Lead Generation", 
     "Text Summarization", "Sentiment Analysis", "Code Generation", "Resume Screening", 
     "Chatbot Q&A", "AI-Powered Report Writing"]
)

# Apply modern UI enhancements
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        }
        .stTextInput>div>div>input {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# 1. Fake News Detection
if option == "Fake News Detection":
    st.title("📰 Fake News Detection")
    user_input = st.text_area("✍️ Enter news text:")
    if st.button("🔍 Analyze"):
        result = groq_chat(user_input, "Analyze this news article and determine if it's real or fake based on verifiable facts and journalistic integrity.")
        st.success(result)

# 2. Advanced Translation
elif option == "Advanced Translation":
    st.title("🌍 Advanced Language Translation")
    user_text = st.text_area("📝 Enter text to translate:")
    target_lang = st.selectbox("🌐 Select Target Language", ["ta", "hi", "ml", "mr", "gu", "fr", "es", "de"])
    if st.button("🔄 Translate"):
        prompt = f"Translate the following text into {target_lang} using proper grammar and context: {user_text}"
        translation = groq_chat(prompt)
        st.text_area("📜 Translated Text", translation, height=100)

# 3. Data Visualization
elif option == "Data Visualization":
    st.title("📊 Data Visualization")
    file = st.file_uploader("📂 Upload CSV File", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.write("📌 **Preview of Uploaded Data:**", df.head())
        selected_column = st.selectbox("📌 Select a column to visualize", df.columns)
        fig = px.histogram(df, x=selected_column, title=f"📊 Distribution of {selected_column}")
        st.plotly_chart(fig)

# 4. Lead Generation
elif option == "Lead Generation":
    st.title("🎯 AI-Powered Lead Generation")
    industry = st.text_input("🏢 Enter Target Industry (e.g., AI, Finance, Healthcare)")
    keywords = st.text_area("🔎 Enter Keywords for Filtering Leads (comma-separated)")
    if st.button("🚀 Generate Leads"):
        prompt = f"Generate a well-structured list of potential leads in the {industry} industry using the following keywords: {keywords}. Include company name, contact email, and website."
        leads = groq_chat(prompt)
        st.text_area("📋 Generated Leads", leads, height=200)

# 5. Text Summarization
elif option == "Text Summarization":
    st.title("📄 AI-Powered Text Summarization")
    user_input = st.text_area("✍️ Enter text to summarize:")
    if st.button("📌 Summarize"):
        summary = groq_chat(user_input, "Summarize the given text in a concise yet informative manner.")
        st.text_area("📜 Summary", summary, height=200)

# 6. Sentiment Analysis
elif option == "Sentiment Analysis":
    st.title("😊 Sentiment Analysis")
    user_input = st.text_area("✍️ Enter text to analyze sentiment:")
    if st.button("📌 Analyze Sentiment"):
        sentiment = groq_chat(user_input, "Analyze this text and classify its sentiment as Positive, Negative, or Neutral with a short justification.")
        st.write(sentiment)

# 7. Code Generation
elif option == "Code Generation":
    st.title("💻 AI-Powered Code Generator")
    user_input = st.text_area("✍️ Describe the function/code you need:")
    if st.button("📌 Generate Code"):
        code = groq_chat(user_input, "Generate well-structured Python code based on this description, following best practices.")
        st.code(code, language="python")

# 8. Resume Screening
elif option == "Resume Screening":
    st.title("📄 AI Resume Screening")
    user_input = st.text_area("✍️ Enter job description or required skills:")
    if st.button("📌 Screen Resumes"):
        resumes = groq_chat(user_input, "Screen resumes based on this job description, selecting the best candidates with matching skills.")
        st.text_area("📋 Recommended Candidates", resumes, height=200)

# 9. Chatbot Q&A
elif option == "Chatbot Q&A":
    st.title("💬 AI Chatbot Q&A")
    user_input = st.text_area("💡 Ask a question:")
    if st.button("📌 Get Answer"):
        answer = groq_chat(user_input, "Provide a well-researched and concise answer to this question.")
        st.write(answer)

# 10. AI-Powered Report Writing
elif option == "AI-Powered Report Writing":
    st.title("📑 AI-Powered Report Writing")
    user_input = st.text_area("✍️ Enter topic or details for the report:")
    if st.button("📝 Generate Report"):
        report = groq_chat(user_input, "Write a comprehensive, structured report on this topic including key insights.")
        st.text_area("📖 Generated Report", report, height=300)

st.sidebar.info("💡 Built with **Groq API & Llama-3.3-70B** for AI-powered insights!")
