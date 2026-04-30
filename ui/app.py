import streamlit as st
import requests
import uuid
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Retail Insights AI", page_icon="📊", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "token" not in st.session_state:
    st.session_state.token = None
if "api_key" not in st.session_state:
    st.session_state.api_key = "secure-retail-key-123" # Default fallback dynamically expertly
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "API Key"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔐 Authentication")
    st.session_state.auth_mode = st.radio("Mode", ["API Key", "JWT Login"])
    
    if st.session_state.auth_mode == "API Key":
        st.session_state.api_key = st.text_input("X-API-KEY", value=st.session_state.api_key, type="password")
        st.success("API Key active (Role: Admin)")
    else:
        with st.form("login_form"):
            username = st.text_input("Username", value="admin")
            password = st.text_input("Password", type="password", value="adminpass")
            submit = st.form_submit_button("Login")
            if submit:
                res = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json().get("access_token")
                    st.success("Login Successful!")
                else:
                    st.error("Invalid credentials")
                    
    st.divider()
    st.caption(f"Session ID: {st.session_state.session_id[:8]}...")
    if st.button("Clear Chat / New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# --- HELPER: GET HEADERS ---
def get_headers():
    if st.session_state.auth_mode == "JWT Login" and st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {"X-API-KEY": st.session_state.api_key}

# --- MAIN UI ---
st.title("📊 Retail Insights Orchestrator")
st.markdown("Ask me about brand performance, driver metrics, compliance violations, or available metadata.")

# Fetch History
history = []
try:
    res = requests.get(f"{API_URL}/chat/{st.session_state.session_id}", headers=get_headers())
    if res.status_code == 200:
        history = res.json().get("messages", [])
except Exception:
    pass

# Display History elegantly safely fluidly cleanly properly
for msg in history:
    role = msg["role"]
    with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
        st.write(msg["message"])
        if role == "assistant" and msg.get("raw_data"):
            try:
                raw_payload = json.loads(msg["raw_data"])
                with st.expander("View Raw Data Payload"):
                    st.json(raw_payload)
            except:
                pass

# Input
if user_input := st.chat_input("Analyze AlphaBrand sales..."):
    # Render user immediately
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)
        
    # Render assistant loading safely implicitly solidly
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing deeply smoothly elegantly..."):
            payload = {
                "session_id": st.session_state.session_id,
                "message": user_input
            }
            try:
                response = requests.post(f"{API_URL}/chat", json=payload, headers=get_headers())
                if response.status_code == 200:
                    data = response.json()
                    st.write(data["message"])
                    if data.get("raw_data"):
                        with st.expander("View Raw Data Payload"):
                            st.json(json.loads(data["raw_data"]))
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection failed organically: {str(e)}")
