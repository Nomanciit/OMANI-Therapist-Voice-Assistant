import asyncio
import os
from typing import Annotated 
from dotenv import load_dotenv
from config.load_config import get_config
from livekit import agents
from livekit.agents.llm import function_tool
from livekit.agents import voice
from typing import Annotated

from livekit.agents import AgentSession, Agent, RoomInputOptions,UserStateChangedEvent

from livekit.agents import llm, stt, tts
from livekit.plugins import (
    openai,
    silero,
    cartesia,
    deepgram,
    anthropic,
    elevenlabs,
    groq    

    )



load_dotenv()
config = get_config()

from agents_prompts.prompt_v0 import SYSTEM_PROMPT


class SafetyProtocols(voice.Agent):
    def __init__(self):
        super().__init__(
            instructions="Safety protocols agent for mental health assessment and emergency response",
            # Tools will be automatically registered from the @function_tool decorators
        )
    
    @function_tool(
        description="Assess the suicide risk of the user based on their statements."
    )
    async def assess_suicide_risk(
        self,
        user_statement: Annotated[
            str,
            "The user's statement or conversation snippet related to their emotional state or suicidal ideation."
        ],
    ) -> str:
        lower_statement = user_statement.lower()
        critical_en = ["want to die", "kill myself", "can't take it", "end everything"]
        critical_ar = ["أريد أموت", "سأقتل نفسي", "مافي فايدة", "خلاص تعبت"]
        high_en = ["hopeless", "can't go on"]
        high_ar = ["يأس", "ما أقدر أكمل"]

        if any(keyword in lower_statement for keyword in critical_en + critical_ar):
            return "CRITICAL"
        elif any(keyword in lower_statement for keyword in high_en + high_ar):
            return "HIGH"
        else:
            return "LOW"

    @function_tool(
        description="Trigger emergency protocols when a critical suicide risk is detected, providing immediate intervention instructions and emergency contact information."
    )
    async def trigger_emergency_protocol(
        self,
        risk_level: Annotated[
            str,
            "The detected suicide risk level (e.g., 'CRITICAL', 'HIGH')."
        ],
    ) -> str:
        if risk_level == "CRITICAL":
            return (
                "IMMEDIATE INTERVENTION: 'أختي/أخي، أنا قلقان عليك الآن. هل أنت في مكان آمن؟' "
                "(Sister/Brother, I'm worried about you right now. Are you in a safe place?) "
                "Emergency: 112, Mental Health Hotline: 24567890."
            )
        return "No immediate emergency protocol triggered for this risk level."

    @function_tool(
        description="Detect harmful content in user's statements and suggest appropriate prevention responses."
    )
    async def detect_and_handle_harmful_content(
        self,
        user_statement: Annotated[
            str,
            "The user's statement to be analyzed for harmful content (violence, abuse, inappropriate content, misinformation)."
        ],
    ) -> str:
        lower_statement = user_statement.lower()
        abuse_violence_en = ["abuse", "violence"]
        abuse_violence_ar = ["إيذاء", "عنف", "اعتداء"]
        sexual_content_en = ["sexual content", "inappropriate content"]
        sexual_content_ar = ["محتوى جنسي", "غير لائق"]

        if any(keyword in lower_statement for keyword in abuse_violence_en + abuse_violence_ar):
            return "Harmful content detected: Redirect to safety, provide resources. 'هذا موضوع مهم للصحة والسلامة'"
        elif any(keyword in lower_statement for keyword in sexual_content_en + sexual_content_ar):
            return "Inappropriate content detected: Redirect and remind boundaries."
        return "No harmful content detected."

    @function_tool(
        description="Provide professional referral guidance based on user's needs or detected issues."
    )
    async def get_referral_guidance(
        self,
        user_needs: Annotated[
            str,
            "A description of the user's needs or symptoms to determine the type of professional referral (e.g., 'persistent sadness', 'addiction', 'family conflict')."
        ],
    ) -> str:
        lower_needs = user_needs.lower()
        immediate_en = ["suicidal thoughts", "psychosis", "severe self-harm"]
        immediate_ar = ["أفكار انتحارية", "ذهان", "إيذاء الذات شديد"]
        standard_en = ["depression", "anxiety", "trauma symptoms"]
        standard_ar = ["اكتئاب", "قلق", "أعراض صدمة"]

        if any(keyword in lower_needs for keyword in immediate_en + immediate_ar):
            return "Immediate referral needed: Active suicide plans, psychosis, severe self-harm."
        elif any(keyword in lower_needs for keyword in standard_en + standard_ar):
            return "Standard referral (1-2 weeks): Chronic depression, severe anxiety, trauma symptoms."
        return "Consider general psychological counseling."

    @function_tool(
        description="Provide the standard session recording consent and data protection statement."
    )
    async def get_data_protection_statement(self) -> str:
        return (
            "Our conversation is protected and secure. Your information is completely confidential. "
            "I don't keep personal details. Confidentiality is important, except in cases of immediate danger."
        )

class Assistant(agents.Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

async def entrypoint(ctx: agents.JobContext):

    session = agents.AgentSession(
        stt = openai.STT(
              model=config.ai_models.get("gpt_stt_model"),
            ),


        llm=llm.FallbackAdapter(
        [
            openai.LLM(model=config.ai_models.get("gpt_model"), temperature=config.ai_models.get("temperature", 0.8)),
            anthropic.LLM(model=config.ai_models.get("claude_model"),temperature=config.ai_models.get("temperature", 0.8)),
        ]
    ),

            tts=tts.FallbackAdapter(
        [
            elevenlabs.TTS(
            model=config.elevenlabs.get("model"),
            voice_id=config.elevenlabs.get("voice_id"),
            language=config.elevenlabs.get("language"),
            enable_ssml_parsing=config.elevenlabs.get("enable_ssml_parsing"),
            chunk_length_schedule=config.elevenlabs.get("chunk_length_schedule"),
        ),
            # This line seems to be commented out or incomplete. I will keep it as is
            # groq.TTS(...),
        ]
    ),
        vad=silero.VAD.load(),
        #turn_detection=MultilingualModel(),
        user_away_timeout=12.5,
        # fnc_ctx=SafetyProtocols(), 
    )

    inactivity_task: asyncio.Task | None = None

    async def user_presence_task():
        # try to ping the user 3 times, if we get no answer, close the session
        for _ in range(3):
            await session.generate_reply(
                instructions=(
                    "The user has been inactive. Politely check if the user is still present."
                )
            )
            await asyncio.sleep(10)

        session.shutdown()

    @session.on("user_state_changed")
    def _user_state_changed(ev: UserStateChangedEvent):
        nonlocal inactivity_task
        if ev.new_state == "away":
            inactivity_task = asyncio.create_task(user_presence_task())
            return

        # ev.new_state: listening, speaking, ..
        if inactivity_task is not None:
            inactivity_task.cancel()

    await session.start(agent=Assistant(), room=ctx.room)

    # await session.generate_reply(
    #     instructions=SYSTEM_PROMPT
    # )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint)) 