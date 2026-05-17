import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="SHL AI Hiring Assistant",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(180deg, #0B1020 0%, #111827 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
            
.stChatInputContainer {
    max-width: 900px;
    margin: auto;
}

textarea {
    min-height: 45px !important;
}

.header-box {
    background: linear-gradient(135deg, #6C63FF, #4F46E5);
    padding: 28px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 35px rgba(79, 70, 229, 0.35);
}

.header-box h1 {
    margin: 0;
    font-size: 42px;
}

.header-box p {
    margin-top: 8px;
    font-size: 18px;
    opacity: 0.95;
}

.assessment-card {
    background: rgba(255, 255, 255, 0.96);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    border-left: 6px solid #6C63FF;
}

.assessment-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 8px;
}

.assessment-type {
    display: inline-block;
    background: #EEF2FF;
    color: #4338CA;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.assessment-link {
    text-decoration: none;
    background: #4F46E5;
    color: white !important;
    padding: 10px 16px;
    border-radius: 10px;
    font-weight: 600;
    display: inline-block;
}

.footer-note {
    text-align: center;
    color: #9CA3AF;
    margin-top: 35px;
    font-size: 14px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin: 24px 0 16px 0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🎯 SHL AI Hiring Assistant</h1>
    <p>Discover the right SHL assessments for every hiring decision in seconds.</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Describe your hiring requirement...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "user_name": "Jeevitha",
        "messages": st.session_state.messages
    }

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=20)
                data = response.json()

                reply = data.get("reply", "No response received.")
                recommendations = data.get("recommendations", [])

                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

                st.session_state.recommendations = recommendations

            except Exception as e:
               st.error(str(e))

if st.session_state.recommendations:
    st.markdown('<div class="section-title">Recommended Assessments</div>', unsafe_allow_html=True)

    for rec in st.session_state.recommendations:
        st.markdown(f"""
        <div class="assessment-card">
            <div class="assessment-title">{rec['name']}</div>
            <div class="assessment-type">{rec['test_type']}</div>
            <br>
            <a class="assessment-link" href="{rec['url']}" target="_blank">
                View Assessment
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(180deg, #0B1020 0%, #111827 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
    margin: auto;
}

.header-box {
    background: linear-gradient(135deg, #6C63FF, #4F46E5);
    padding: 28px;
    border-radius: 22px;
    color: white;
    margin: 0 auto 30px auto;
    max-width: 850px;
    text-align: center;
    box-shadow: 0 10px 35px rgba(79, 70, 229, 0.35);
}

.header-box h1 {
    margin: 0;
    font-size: 42px;
}

.header-box p {
    margin-top: 10px;
    font-size: 18px;
    opacity: 0.95;
}

.assessment-card {
    background: rgba(255, 255, 255, 0.96);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    border-left: 6px solid #6C63FF;
}

.assessment-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 8px;
}

.assessment-type {
    display: inline-block;
    background: #EEF2FF;
    color: #4338CA;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.assessment-link {
    text-decoration: none;
    background: #4F46E5;
    color: white !important;
    padding: 10px 16px;
    border-radius: 10px;
    font-weight: 600;
    display: inline-block;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin: 24px 0 16px 0;
    color: white;
}

.footer-note {
    text-align: center;
    color: #9CA3AF;
    margin-top: 35px;
    font-size: 14px;
}

/* INPUT FIX */
[data-testid="stChatInput"] {
    max-width: 850px;
    margin: auto;
}

[data-testid="stChatInput"] textarea {
    min-height: 45px !important;
    max-height: 45px !important;
    border-radius: 14px !important;
}
</style>
""", unsafe_allow_html=True)