# Technical Documentation

## 1. Model Evaluation Report: Comparative Analysis of Dual-Model Approach

This section details the comparative analysis of the dual-model approach implemented in the Omani Therapist Voice Assistant. It leverages a fallback mechanism for Speech-to-Text (STT) using OpenAI's `gpt-4o-transcribe` and Deepgram, and for Large Language Models (LLM) using OpenAI's `gpt-4o` and Anthropic's `claude-3-5-sonnet-20241022` models.

*   **Methodology:** The system employs `stt.FallbackAdapter` and `llm.FallbackAdapter` to ensure resilience and optimize performance by trying multiple providers. Default models and temperatures are configured in `config.yaml`.
*   **Results:** (To be populated after testing) Performance metrics would compare accuracy, latency, and effectiveness across primary and fallback STT/LLM providers.
*   **Conclusion:** (To be populated after testing) Summary of findings regarding the dual-model approach's benefits in terms of reliability and quality.

## 2. Cultural Adaptation Guide: Omani Arabic Implementation Details

This guide details the strategies and linguistic choices made to ensure the Omani Therapist Voice Assistant is culturally sensitive and effective for an Omani Arabic-speaking audience. It covers the integration of Islamic values, Gulf Arab traditions, and modern Omani life into the assistant's persona and responses, as defined in `agents_prompts/prompt_v0.py`.

*   **Cultural Context Integration:** The `SYSTEM_PROMPT` (from `agents_prompts/prompt_v0.py`) explicitly guides the AI to adopt a warm, empathetic voice persona, culturally fluent in Islamic values and Omani traditions.
*   **Linguistic and Dialectal Nuances:** The assistant is designed for seamless bilingual conversation (Arabic and English), including code-switching. `elevenlabs.TTS` is configured with `language="ar"` (from `config.yaml`) for Arabic speech synthesis.
*   **Therapeutic Approach Adaptation:** The `SYSTEM_PROMPT` outlines culturally adapted interventions, Islamic-integrated CBT, and trauma-informed care.

## 3. Safety Protocol Documentation: Crisis Intervention and Escalation Procedures

This section documents the comprehensive safety protocols implemented in the `SafetyProtocols` class in `voice-assistant.py`:

*   **Suicide Risk Assessment (`assess_suicide_risk` function):** Detects risk levels (CRITICAL, HIGH, LOW) using a combination of English and Arabic keywords. 
    *   **Critical Keywords (EN/AR):** "want to die", "kill myself", "can't take it", "end everything" / "أريد أموت", "سأقتل نفسي", "مافي فايدة", "خلاص تعبت"
    *   **High Keywords (EN/AR):** "hopeless", "can't go on" / "يأس", "ما أقدر أكمل"
*   **Harmful Content Detection (`detect_and_handle_harmful_content` function):** Identifies and suggests responses for violence, abuse, inappropriate content, and misinformation using English and Arabic keywords.
    *   **Abuse/Violence Keywords (EN/AR):** "abuse", "violence" / "إيذاء", "عنف", "اعتداء"
    *   **Sexual/Inappropriate Keywords (EN/AR):** "sexual content", "inappropriate content" / "محتوى جنسي", "غير لائق"
*   **Professional Referral Triggers (`get_referral_guidance` function):** Provides guidance for immediate, urgent, or standard professional referrals based on user needs, using English and Arabic keywords.
    *   **Immediate Referral Keywords (EN/AR):** "suicidal thoughts", "psychosis", "severe self-harm" / "أفكار انتحارية", "ذهان", "إيذاء الذات شديد"
    *   **Standard Referral Keywords (EN/AR):** "depression", "anxiety", "trauma symptoms" / "اكتئاب", "قلق", "أعراض صدمة"
*   **Emergency Contact Integration:** The `trigger_emergency_protocol` function provides emergency contacts: `Emergency: 112`, `Mental Health Hotline: 24567890`.
*   **Session Recording and Data Protection (`get_data_protection_statement` function):** Delivers a standard statement ensuring confidentiality, with limits for immediate danger.

## 4. Performance Benchmarks: Latency, Accuracy, and Scalability Metrics

This section would present the performance benchmarks:

*   **Latency:** The system uses `openai.STT` (model: `gpt-4o-transcribe`) and `deepgram.STT` for speech-to-text, and `openai.LLM` (`gpt-4o`) and `anthropic.LLM` (`claude-3-5-sonnet-20241022`) for language processing. `elevenlabs.TTS` (model: `eleven_multilingual_v2`) is used for text-to-speech, with a `chunk_length_schedule` configured for streaming. Real-time performance is crucial.
*   **Accuracy:** The dual-model fallback approach aims to improve overall accuracy by leveraging multiple providers.
*   **Scalability:** The `user_away_timeout=12.5` setting helps manage session resources during user inactivity. (Further scalability assessment would require load testing).

## 5. Test Conversation Logs: 5+ Different Therapeutic Scenarios

This section would contain anonymized logs of test conversations demonstrating various therapeutic scenarios, including:

*   Initial consultations.
*   Sessions addressing anxiety, depression, or cultural conflicts.
*   Crisis intervention simulations.
*   Examples of bilingual interactions and code-switching.

## 6. Deployment Instructions: Production Setup and Maintenance Guide

Detailed deployment instructions are available in the `README.md` file, covering:

*   **Prerequisites:** Python 3.9+, dependencies from `requirements.txt`.
*   **Deployment Steps:** Cloning the repository, installing dependencies, and configuring environment variables in a `.env` file (e.g., `LIVEKIT_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `ELEVENLABS_API_KEY`, `DEEPGRAM_API_KEY`).
*   **Running the Agent:** Executing `python voice-assistant.py` and connecting via the LiveKit Agents Playground (`https://agents-playground.livekit.io/`).

## 7. Future Roadmap: Scaling and Improvement Recommendations

This section outlines the future development plan, focusing on enhancing the Omani Therapist Voice Assistant's capabilities and performance.

*   **Agentic Architecture:** Transition to a multi-agent architecture with a central orchestrator agent. This main agent will manage overall conversation flow, including intelligent language switching between English and Arabic. Dedicated sub-agents will be developed to handle specific use cases, such as advanced safety protocol enforcement and specialized therapeutic interventions.
*   **Service Provider Evaluation and Optimization:** Conduct a comprehensive comparative analysis of various Speech-to-Text (STT), Large Language Model (LLM), and Text-to-Speech (TTS) service providers. The goal is to evaluate and select the best-performing models for both English and Arabic languages to ensure the highest quality voice interactions and therapeutic effectiveness.
*   **Scaling Strategies:** Recommendations for scaling the infrastructure to support a larger user base.
*   **Feature Enhancements:** Proposed new features, such as advanced emotional recognition, additional therapeutic modalities, or integration with external health services.
*   **Model Improvements:** Suggestions for further fine-tuning or upgrading AI models for better performance and cultural relevance.
