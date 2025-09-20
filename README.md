# Omani Therapist Voice Assistant

This project features an AI-powered Omani Mental Health Therapist Voice Assistant, offering culturally-informed therapeutic support in Arabic and English.

## Features

- **Culturally-Informed & Bilingual:** Provides empathetic support with cultural fluency and seamless Arabic/English conversation.
- **Real-time Safety:** Includes suicide risk assessment, harmful content detection, and professional referral.
- **Dynamic Sessions:** Manages user inactivity and ensures continuous engagement.
- **Configurable AI:** Utilizes customizable STT, LLM, and TTS models via `config.yaml`.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/omani-therapist-voice-assistant.git
cd omani-therapist-voice-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file and add your API keys:

```
LIVEKIT_API_KEY="your_livekit_api_key"
LIVEKIT_API_SECRET="your_livekit_api_secret"
OPENAI_API_KEY="your_openai_api_key"
ANTHROPIC_API_KEY="your_anthropic_api_key"
ELEVENLABS_API_KEY="your_elevenlabs_api_key"
DEEPGRAM_API_KEY="your_deepgram_api_key"
```

## Running the Agent

To start the agent:

```bash
python voice-assistant.py
```

Ensure your LiveKit server is running and accessible.

### LiveKit Setup and Connection

1.  **Create a LiveKit Account:** Sign up at [LiveKit](https://livekit.io/).
2.  **Create an Assistant:** Follow the LiveKit documentation to create a new assistant.
3.  **Get API Credentials:** Go to your assistant's settings and copy the LiveKit API key, secret key, and assistant URL.
4.  **Run the Agent:** Execute the command: `python voice-assistant.py start` or `python voice-assistant.py`.
5.  **Connect in Playground:** Open [LiveKit Agents Playground](https://agents-playground.livekit.io/) and connect your running assistant to interact with it.
