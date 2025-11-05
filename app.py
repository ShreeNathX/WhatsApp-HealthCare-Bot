import os
import time
import logging
import requests
import tempfile
import io
from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langdetect import detect
import backoff

# --- Gemini SDK for AI Core Logic ---
import google.genai as genai
from google.genai import types
from google.genai.errors import APIError

# ----------------------------------------------------
# ⚙️ CONFIGURATION & CLIENT SETUP
# ----------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Initialize Gemini and Twilio clients for messaging and media handling
gemini_client = genai.Client() if GEMINI_API_KEY else None
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN) else None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("healthassistant")

app = Flask(__name__)
user_sessions = {}

# ----------------------------------------------------
# 🧭 CONSTANTS & SAFETY DEFINITIONS
# ----------------------------------------------------
SESSION_TIMEOUT = 300 # Reset session after 5 minutes of inactivity

# Keywords that end the conversation gracefully
EXIT_WORDS = ["bye", "no", "thanks", "thank you", "नहीं", "धन्यवाद", "stop", "exit", "band karo"]

# Critical keywords that trigger the immediate 108 emergency handoff, bypassing the AI
EMERGENCY_WORDS = ["unconscious", "chest pain", "heavy bleeding", "heart attack", "saans lene me dikkat", "सांस लेने में दिक्कत", "दम घुट रहा", "साँस लेने में कठिनाई"] 

# Supported languages for localization and language detection
SUPPORTED_LANGS = ["en", "hi", "mr", "bn"]

EMERGENCY_MESSAGE = {
    "hi": "⚠️ **तुरंत मदद!** यह एक आपातकालीन स्थिति हो सकती है। कृपया बिना देर किए एम्बुलेंस को कॉल करें: **108** या नजदीकी स्वास्थ्य केंद्र पर जाएं।",
    "en": "⚠️ **EMERGENCY!** This may be a life-threatening situation. Please call an ambulance immediately: **108** or go to the nearest health center.",
    "mr": "⚠️ **त्वरित मदत!** ही गंभीर समस्या असू शकते. कृपया त्वरित ॲम्बुलन्सला कॉल करा: **108** किंवा जवळच्या आरोग्य केंद्रात जा.",
    "bn": "⚠️ **জরুরী!** এটি একটি জীবন-হুমকির পরিস্থিতি হতে পারে। অবিলম্বে অ্যাম্বুলেন্সকে কল করুন: **108** অথবা নিকটস্থ স্বাস্থ্যকেন্দ্রে যান।"
}

# ----------------------------------------------------
# 🔧 CORE UTILITIES
# ----------------------------------------------------
def detect_language(text):
    """Determines the user's language for localization."""
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGS else "en"
    except Exception:
        return "en"

def generate_maps_link(lang="en"):
    """Creates a localized Google Maps link for nearby health centers."""
    localized_query = {
        "hi": "नजदीकी स्वास्थ्य केंद्र",
        "mr": "जवळचे आरोग्य केंद्र",
        "bn": "নিকটস্থ স্বাস্থ্যকেন্দ্র",
        "en": "health center near me"
    }.get(lang, "health center near me")
    return f"https://www.google.com/maps/search/?api=1&query={localized_query.replace(' ', '+')}"

def fallback_message(lang):
    """A safe, localized message when the AI or API fails."""
    return {
        "hi": "माफ़ कीजिए, मैं अभी जवाब नहीं दे पा रहा हूँ। कृपया बाद में प्रयास करें।",
        "mr": "माफ करा, मी सध्या उत्तर देऊ शकत नाही. कृपया नंतर प्रयत्न करा.",
        "bn": "দুঃখিত, আমি এখন উত্তর দিতে পারছি না। পরে আবার চেষ্টা করুন।",
        "en": "Sorry, I couldn't process that right now. Please try again later."
    }.get(lang, "Sorry, please try again later.")

def get_user_state(user_id):
    """Manages user session data (language, history) and handles timeouts."""
    state = user_sessions.get(user_id)
    if state and time.time() - state.get("last_seen", 0) <= SESSION_TIMEOUT:
        state["last_seen"] = time.time()
        return state
    
    # Initialize a fresh session state for new or timed-out users
    return {
        "lang": None, 
        "msg_count": 0,
        "last_seen": time.time(),
        "history": [] 
    }

# ----------------------------------------------------
# 🎤 VOICE & AI LOGIC (GEMINI INTEGRATION)
# ----------------------------------------------------

def download_media_as_bytes(media_url: str) -> bytes:
    """Downloads media from Twilio using Basic Auth."""
    if not twilio_client:
        raise Exception("Twilio client is not configured for media download.")

    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    download_url = media_url.replace('.json', '')
    
    response = requests.get(download_url, auth=auth)
    response.raise_for_status()
    
    return response.content

def transcribe_audio_gemini(media_url: str, from_number: str) -> str:
    """Uses Gemini's multimodal capability to transcribe WhatsApp audio."""
    if gemini_client is None:
        raise Exception("Gemini client not configured.")
        
    audio_bytes = download_media_as_bytes(media_url)
    
    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type='audio/ogg' # Common WhatsApp audio format
    )
    
    prompt_text = "Transcribe the following audio recording into the language being spoken. Provide only the text transcription."
    
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=[audio_part, prompt_text]
    )
    
    return response.text.strip()

def build_gemini_system_instruction(lang: str = "en") -> str:
    """Defines the strict persona, safety rules, and limitations for the AI Health Assistant."""
    base = (
        f"You are a highly compassionate, non-diagnostic AI Health Assistant operating in a rural context. Answer only in the user's language ({lang.upper()}).\n"
        "- **Your Role:** Provide empathetic, safe, and actionable triage advice (first aid, home care, prevention).\n"
        "- **Diagnosis:** **NEVER** provide a definitive diagnosis (e.g., 'You have Dengue'). Use non-committal language (e.g., 'Your symptoms may be consistent with a common viral fever...').\n"
        "- **Conciseness:** Keep your response brief—**maximum of three concise paragraphs**.\n"
        "- **Safety:** If any symptom is severe, persistent, or a clear emergency, your **MAIN** response must be to **seek professional medical help immediately**.\n"
        "- **Medication:** **NEVER** recommend prescription medication. Only suggest common, over-the-counter remedies like rest, fluids, and safe pain relievers (e.g., paracetamol).\n"
        "- **Non-Health Queries:** If the user asks a non-health question (e.g., politics, jokes), **politely decline to answer** and redirect them back to health topics. Keep this refusal very brief.\n"
        "- **Tone:** Use simple, non-medical, and culturally appropriate language, like talking to a family member in a village setting.\n"
    )
    return base

@backoff.on_exception(backoff.expo, (APIError, requests.exceptions.RequestException), max_tries=3, factor=1)
def ask_llm(user_id: str, question: str, lang="en") -> str:
    """Queries the Gemini model, managing conversation history for context."""
    if gemini_client is None:
        return fallback_message(lang)
    
    state = user_sessions[user_id]
    
    # Add the user's new question to the session history
    state["history"].append(types.Content(role="user", parts=[types.Part.from_text(question)]))
    
    system_instruction = build_gemini_system_instruction(lang)
    
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=state["history"], # The model processes the conversation history
            config=types.GenerateContentConfig(
                temperature=0.7,
                system_instruction=system_instruction, # Enforce safety rules
                max_output_tokens=500
            )
        )
        reply = response.text.strip()
        
        if not reply:
            raise Exception("LLM returned empty.")
            
        # Add the model's response to the history for the next turn
        state["history"].append(types.Content(role="model", parts=[types.Part.from_text(reply)]))
        
        return reply

    except APIError as e:
        logger.error("Gemini API Error: %s", e)
        # We re-raise the API error to trigger backoff/retry logic
        raise 
    except Exception as e:
        logger.error("Non-API exception in ask_llm: %s", e)
        return fallback_message(lang)


# ----------------------------------------------------
# 💬 CONVERSATION FLOW MANAGER
# ----------------------------------------------------
def build_conversation_response(user_id, incoming_msg_raw, is_audio=False):
    """Orchestrates the entire conversation flow: state, safety, AI, and response."""
    state = get_user_state(user_id)
    is_first_message = (state["msg_count"] == 0)
    state["msg_count"] += 1
    
    # Detect language if not set (crucial for first text/transcribed message)
    if state["lang"] is None:
        state["lang"] = detect_language(incoming_msg_raw)
    
    user_sessions[user_id] = state 

    incoming_msg_normalized = incoming_msg_raw.lower().strip()
    lang = state["lang"]
    final_response = ""
    
    # 1. Handle EXIT Keywords
    if any(word in incoming_msg_normalized for word in EXIT_WORDS):
        user_sessions.pop(user_id, None)
        return "Conversation ended. You can send a new message to start again."
        
    # 2. Handle CRITICAL EMERGENCY Handoff
    if any(word in incoming_msg_normalized for word in EMERGENCY_WORDS):
        logger.critical("Emergency keyword detected from %s", user_id)
        user_sessions.pop(user_id, None) 
        return EMERGENCY_MESSAGE.get(lang, EMERGENCY_MESSAGE["en"])

    # 3. Welcome Message (if first interaction and not audio)
    if is_first_message and not is_audio:
        welcome_text = {
            "hi": "नमस्ते! मैं आपका AI स्वास्थ्य सहायक हूँ। कृपया अपने स्वास्थ्य संबंधी सवाल पूछें।",
            "en": "Hello! I'm your AI Health Assistant. Please ask your health-related question.",
            "mr": "नमस्कार! मी तुमचा आरोग्य सहाय्यक आहे. कृपया तुमचा आरोग्य संबंधित प्रश्न विचारा.",
            "bn": "হ্যালো! আমি আপনার এআই স্বাস্থ্য সহকারী। আপনার স্বাস্থ্য সংক্রান্ত প্রশ্ন জিজ্ঞাসা করুন।"
        }.get(lang, "Hello! I'm your AI Health Assistant. Please ask your health-related question.")
        final_response += f"*{welcome_text}*\n\n---\n"

    # 4. Process Query with LLM
    try:
        llm_reply = ask_llm(user_id, incoming_msg_raw, lang=lang)
        final_response += llm_reply
            
        # 5. Append Safety and Referral Link
        map_link = generate_maps_link(lang)
        final_response += f"\n\n---\n🗺️ **नजदीकी स्वास्थ्य केंद्र / Nearby Health Center:** [नक्शा / Map Link]({map_link})"
        
        return final_response

    except Exception:
        # Final safety net if all LLM retries fail
        return fallback_message(lang)


# ----------------------------------------------------
# 🌐 FLASK ROUTES (TWILIO WEBHOOK)
# ----------------------------------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Twilio webhook to receive incoming messages and media."""
    from_number = request.form.get("From", "")
    incoming_msg_body = request.form.get("Body", "")
    media_url = request.form.get("MediaUrl0")
    num_media = int(request.form.get("NumMedia", 0))
    is_audio = False
    
    logger.info("Incoming message from %s: Body='%s', Media='%s'", from_number, incoming_msg_body, media_url)

    # Handle Voice Messages
    if num_media > 0 and media_url:
        is_audio = True
        user_state = get_user_state(from_number)
        user_lang = user_state.get("lang", "en") 

        try:
            incoming_msg_body = transcribe_audio_gemini(media_url, from_number)
            logger.info("Transcribed Text: %s", incoming_msg_body)
            # If this was the first message, set the session language based on transcription
            if user_state["lang"] is None:
                 user_state["lang"] = detect_language(incoming_msg_body)
                 user_sessions[from_number] = user_state
                 
        except Exception as e:
            logger.error("Failed to process media/transcribe audio for %s: %s", from_number, e)
            reply_text = fallback_message(user_lang)
            resp = MessagingResponse()
            resp.message(reply_text)
            return Response(str(resp), mimetype="application/xml")

    # Process Text (from body or successful transcription)
    if not incoming_msg_body.strip():
        reply_text = "Sorry, I received an empty message. Please try again or type your question."
    else:
        reply_text = build_conversation_response(from_number, incoming_msg_body, is_audio=is_audio)

    # Send Response
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply_text)
    return Response(str(resp), mimetype="application/xml")

@app.route("/", methods=["GET"])
def index():
    """Simple health check endpoint."""
    return "✅ WhatsApp AI Health Assistant (Gemini) is running."

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)