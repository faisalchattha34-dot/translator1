import streamlit as st
import requests
import os
import uuid

# ---------------------------
# Streamlit App UI
# ---------------------------
st.set_page_config(page_title="🌐 Language Translator", layout="centered")
st.title("🌐 Azure Language Translator")

# ---------------------------
# Load Azure Credentials
# ---------------------------
AZURE_KEY = os.environ.get("AZURE_TRANSLATOR_KEY")
AZURE_ENDPOINT = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
AZURE_REGION = os.environ.get("AZURE_TRANSLATOR_REGION")

if not AZURE_KEY:
    st.error("❌ Azure Translator Key missing. Please set environment variable: AZURE_TRANSLATOR_KEY")
    st.stop()

if not AZURE_ENDPOINT:
    st.error("❌ Azure Translator Endpoint missing. Please set environment variable: AZURE_TRANSLATOR_ENDPOINT")
    st.stop()

if not AZURE_REGION:
    st.error("❌ Azure Translator Region missing. Please set environment variable: AZURE_TRANSLATOR_REGION")
    st.stop()


# ---------------------------
# Translation Function
# ---------------------------
def translate_text(text, from_lang, to_lang):
    url = f"{AZURE_ENDPOINT}/translate?api-version=3.0&from={from_lang}&to={to_lang}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    body = [{"text": text}]

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    try:
        return result[0]["translations"][0]["text"]
    except:
        return "Error: Invalid API Response"


# ---------------------------
# UI Inputs
# ---------------------------
text = st.text_area("Enter text to translate:")

col1, col2 = st.columns(2)

with col1:
    from_lang = st.selectbox("From Language", ["en", "ur", "ar", "fr", "de", "zh", "hi"])
with col2:
    to_lang = st.selectbox("To Language", ["ur", "en", "ar", "fr", "de", "zh", "hi"])

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        translated = translate_text(text, from_lang, to_lang)
        st.subheader("Translated Text:")
        st.success(translated)
