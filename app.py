import streamlit as st
import requests
import uuid

st.set_page_config(page_title="🌐 Language Translator", layout="centered")
st.title("🌐 Azure Language Translator")

# ---------------------------
# User Inputs For Azure Settings
# ---------------------------
st.sidebar.header("🔐 Azure Translator Settings")

AZURE_KEY = st.sidebar.text_input("Azure Key", type="password")
AZURE_ENDPOINT = st.sidebar.text_input("Azure Endpoint", "https://api.cognitive.microsofttranslator.com")
AZURE_REGION = st.sidebar.text_input("Azure Region", "eastasia")

if not AZURE_KEY:
    st.warning("Please enter your Azure Translator Key in the left sidebar.")
else:
    st.success("Azure Key Loaded Successfully!")


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
    except Exception as e:
        return f"Error: {result}"


# ---------------------------
# UI
# ---------------------------
text = st.text_area("Enter text:")

col1, col2 = st.columns(2)
with col1:
    from_lang = st.selectbox("From Language", ["en", "ur", "ar", "fr", "de", "zh", "hi"])
with col2:
    to_lang = st.selectbox("To Language", ["ur", "en", "ar", "fr", "de", "zh", "hi"])

if st.button("Translate"):
    if not AZURE_KEY:
        st.error("❌ Please enter Azure Key in the sidebar!")
    elif not text.strip():
        st.warning("Please enter text to translate.")
    else:
        result = translate_text(text, from_lang, to_lang)
        st.subheader("Translated Text:")
        st.success(result)
