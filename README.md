# 🌤️ Weather AI Assistant

An AI-powered weather assistant built with Python, Streamlit, LangChain, Groq, and a live weather API. The app uses natural-language chat to answer weather questions and provide information such as temperature, humidity, wind speed, UV index, and current conditions.

## Features

- 💬 Interactive Streamlit chat interface
- 🤖 Groq-hosted AI responses through LangChain
- 🌍 Real-time weather lookup for cities worldwide
- 🌡️ Temperature and "feels like" information
- 💧 Humidity, wind, UV index, and weather conditions
- 🔄 Suggested prompts and conversation clearing
- 🛡️ API, network, and malformed-response error handling

## How It Works

1. The user submits a weather or general-purpose question.
2. LangChain connects the prompt to a Groq chat model.
3. For current-weather questions, the agent calls the `get_weather` tool.
4. The tool retrieves live data from WeatherAPI and formats the response.
5. Streamlit displays the answer and preserves chat history in the session.

## Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/)
- [WeatherAPI](https://www.weatherapi.com/)
- [Requests](https://requests.readthedocs.io/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)

## Prerequisites

- Python 3.10 or newer
- A Groq API key
- A WeatherAPI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sandeepsharma20/Weather_ai_agent.git
cd Weather_ai_agent
```

### 2. Create and activate a virtual environment

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_weatherapi_key
```

The `.env` file is intentionally excluded by `.gitignore` so API credentials are not committed to Git.

> **Note:** The application currently reads `OPENWEATHER_API_KEY`, even though it sends requests to the WeatherAPI service. Keep that variable name unless you update `main.py`.

## Running the App

```bash
streamlit run main.py
```

Streamlit will print a local URL, usually `http://localhost:8501`, where you can open the app in your browser.

## Example Questions

- "What's the weather in Delhi?"
- "Tell me the weather in Mumbai."
- "What is the humidity in London?"
- "How windy is it in New York?"
- "What does UV index mean?"
- "How does an AI agent work?"

## Project Structure

```text
Weather_ai_agent/
├── main.py          # Streamlit UI, LangChain agent, and WeatherAPI tool
├── requirements.txt # Python dependencies
├── .gitignore       # Local environment and virtual environment exclusions
└── __pycache__/     # Python runtime cache files
```

## Configuration Details

The Groq model is configured in `main.py` as:

```python
openai/gpt-oss-120b
```

The weather tool sends a request to:

```text
https://api.weatherapi.com/v1/current.json
```

It requests Celsius temperature, feels-like temperature, humidity, condition, wind in kph, UV index, and the last update time.

## Security

- Never commit `.env` or API keys.
- Rotate a key immediately if it is exposed publicly.
- Use environment-variable management or Streamlit secrets for deployed environments.

## Deployment

The app can be deployed to Streamlit Community Cloud or another Python-compatible hosting platform.

Before deployment:

1. Push the repository to GitHub.
2. Add `GROQ_API_KEY` and `OPENWEATHER_API_KEY` as secret/environment variables in the hosting platform.
3. Set the entry point to `main.py`.

## Known Notes

- The repository is named `Weather_ai_agent`, but the live weather provider implemented in `main.py` is WeatherAPI rather than OpenWeather.
- The application should be run from the repository directory so that `.env` is discovered correctly.
- `__pycache__/` is generated locally and is not application source code.

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

No license has been specified for this repository. Contact the repository owner for permission details before redistribution or commercial use.
