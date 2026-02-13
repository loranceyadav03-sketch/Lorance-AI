import streamlit as st
import google.generativeai as genai

# Aapki Nayi API Key
API_KEY = "st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# Smart Model Setup: Ye khud dhoond lega ki kaunsa model chal raha hai
@st.cache_resource
def load_model():
    try:
        # Hum direct model list se pehla working model uthayenge
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(available_models[0])
    except Exception as e:
        return None

model = load_model()

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("Lorance Ai 🚀")

if model is None:
    st.error("Model nahi mil raha. Kya API key sahi hai?")
else:
    # Testing ke liye dikhayega ki kaunsa model connect hua
    st.caption(f"Connected: {model.model_name}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Dost, puchiye kuch bhi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:

            st.error(f"Error: {e}")
