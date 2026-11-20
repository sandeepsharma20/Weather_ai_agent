import os
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Weather AI Assistant",
    page_icon="🌤️",
    layout="centered"
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .app-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .app-subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .feature-card {
        background-color: #1e293b;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #334155;
        margin-bottom: 10px;
    }

    .feature-card h3 {
        color: #38bdf8;
        font-size: 18px;
    }

    .feature-card p {
        color: #cbd5e1;
        font-size: 14px;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# ==========================================
# 4. INITIALIZE AI AGENT
# ==========================================

@st.cache_resource
def initialize_agent():

    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found in .env!")

    if not WEATHER_API_KEY:
        raise ValueError("WeatherAPI key not found in .env!")

    # Initialize Groq LLM

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
        api_key=GROQ_API_KEY
    )

    # ======================================
    # WEATHER TOOL
    # ======================================

    @tool
    def get_weather(city: str) -> dict:
        """
        Get current weather information for a city.

        Use this tool when users ask about
        temperature, humidity, wind speed
        or current weather conditions.
        """

        url = "https://api.weatherapi.com/v1/current.json"

        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "aqi": "no"
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            weather_info = {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "temperature": data["current"]["temp_c"],
                "feels_like": data["current"]["feelslike_c"],
                "humidity": data["current"]["humidity"],
                "weather": data["current"]["condition"]["text"],
                "wind_speed": data["current"]["wind_kph"],
                "uv_index": data["current"]["uv"],
                "last_updated": data["current"]["last_updated"]
            }

            return weather_info

        except requests.exceptions.HTTPError:

            try:
                error_data = response.json()

                return {
                    "error": error_data.get(
                        "error", {}
                    ).get(
                        "message",
                        "Weather API error"
                    )
                }

            except ValueError:
                return {"error": "Weather API request failed."}

        except requests.exceptions.RequestException as e:

            return {"error": f"Network error: {str(e)}"}

        except (KeyError, IndexError, TypeError):

            return {"error": "Unexpected weather API response!"}

    # ======================================
    # CREATE AGENT
    # ======================================

    agent = create_agent(

        model=llm,

        tools=[get_weather],

        system_prompt="""
        You are a helpful AI Weather Assistant.

        Responsibilities:

        1. Use the get_weather tool for current weather questions.
        2. Never invent weather information.
        3. Clearly communicate API errors.
        4. Answer general questions without using the weather tool.
        5. Give clear and friendly responses.
        6. Give recommendations only when supported by
           the retrieved weather information.
        """
    )

    return agent


# ==========================================
# 5. INITIALIZE SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# 6. APPLICATION HEADER
# ==========================================

st.markdown(
    '<div class="app-title">🌤️ Weather AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Your intelligent assistant for real-time weather information'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# 7. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🌦️ Weather AI")

    st.write("Your personal AI-powered weather assistant.")

    st.divider()

    st.subheader("Features")

    st.write("🌍 Real-time weather")
    st.write("🤖 AI-powered responses")
    st.write("💬 Interactive conversations")
    st.write("📊 Weather information")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("Built with Python, Streamlit, LangChain and Groq.")


# ==========================================
# 8. FEATURE CARDS
# ==========================================

if not st.session_state.messages:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🌍 Weather</h3>
            <p>Get current weather conditions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Agent</h3>
            <p>Ask questions naturally.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Real-time</h3>
            <p>Retrieve live weather data.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("### Try asking something:")

    suggestions = [
        "What's the weather in Delhi?",
        "Tell me the weather in Mumbai.",
        "What is humidity?",
        "How does an AI agent work?"
    ]

    cols = st.columns(2)

    for index, suggestion in enumerate(suggestions):

        with cols[index % 2]:

            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_prompt = suggestion
                st.rerun()


# ==========================================
# 9. DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# 10. CHAT INPUT
# ==========================================

prompt = st.chat_input("Ask me about the weather...")


# Handle suggestion buttons

if "pending_prompt" in st.session_state:

    prompt = st.session_state.pending_prompt

    del st.session_state.pending_prompt


# ==========================================
# 11. PROCESS USER MESSAGE
# ==========================================

if prompt:

    # Display user message

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                agent = initialize_agent()

                response = agent.invoke({

                    "messages": st.session_state.messages

                })

                answer = response["messages"][-1].content

                # Handle non-string content

                if not isinstance(answer, str):

                    answer = str(answer)

                st.markdown(answer)

                st.session_state.messages.append({

                    "role": "assistant",
                    "content": answer

                })

            except Exception as e:

                error_message = f"Something went wrong: {str(e)}"

                st.error(error_message)

    st.rerun()