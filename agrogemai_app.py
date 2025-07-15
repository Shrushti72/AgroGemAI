import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai

# --- Firebase Setup ---
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/YUVA/OneDrive/Desktop/firebase/agrogemai-firebase-adminsdk-fbsvc-467cc9065f.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- Gemini API Setup ---
genai.configure(api_key="AIzaSyDLNzI2cp_x41P-U4ZImFbIlvZoifJZq-A")  # Replace with your new API key

# List available models
available_models = [m.name for m in genai.list_models()]
st.write("Available models:", available_models)

# Use the first generative model found, or show error
model_name = "models/gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# --- Streamlit App UI ---
st.title("🌾 AgroGemAI - Smart Farming Assistant")

soil_ph = st.text_input("Enter your Soil pH")
location = st.text_input("Enter your Location")
query = st.text_area("Ask anything about your farm (optional)")

if st.button("Get AI Advice"):
    user_prompt = f"My farm is in {location}. Soil pH is {soil_ph}. {query}"
    try:
        response = model.generate_content(user_prompt)
        st.success(response.text)
        # Save to Firestore
        db.collection("queries").add({
            "location": location,
            "soil_ph": soil_ph,
            "query": query,
            "response": response.text
        })
    except Exception as e:
        st.error(f"Error from Gemini API: {e}")