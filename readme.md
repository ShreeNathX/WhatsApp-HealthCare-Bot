# 🩺 WhatsApp AI Health Assistant (Powered by OpenAI)

A highly accessible and secure conversational AI assistant for **rural healthcare triage** and first aid advice, delivered through **WhatsApp**.  
This project uses **OpenAI’s GPT and Whisper models** for intelligent reasoning, empathy, and accurate voice transcription, alongside **Twilio** for seamless messaging.

---

## ✅ Key Features

This AI is designed to act as a **safe, non-diagnostic** health assistant.

* 🤒 **Symptom Triage:** Analyzes symptoms and provides immediate, safe first aid and home care advice.
* 🧠 **OpenAI Integration:** Utilizes **OpenAI GPT models** for powerful, context-aware reasoning and memory-based conversation handling.
* 🎙️ **Voice Message Support (ASR):** Uses **OpenAI Whisper** to **transcribe voice notes** into text, ensuring accessibility for all users.
* 🗣 **Multilingual Support:** Auto-detects and converses in **English, Hindi, Marathi, and Bengali**.
* 🚨 **Emergency Handoff:** Instantly recognizes critical keywords (e.g., "chest pain," "saans lene me dikkat") and directs the user to call **108** (Ambulance/Emergency).
* 🏥 **Referral Link:** Provides a **localized Google Maps link** to find the nearest health center or hospital during emergencies.

---

## 🛠 Tools Used

| Tool | Purpose |
| :--- | :--- |
| **Flask** | Lightweight web server to run the Python application. |
| **Twilio** | WhatsApp messaging API to receive and send messages. |
| **Ngrok** | Creates a secure public link to expose your local Flask server to Twilio. |
| **OpenAI API** | The primary engine for **health triage**, **contextual conversation**, and **voice transcription** using GPT and Whisper. |
| **Langdetect** | Python library for automatic language detection. |
| **Google Maps Link** | Provides actionable hospital or clinic search links. |

---

## ⚙️ Setup Guide (Step-by-Step for Beginners)

Follow these steps to get your AI Health Assistant running locally and connected to WhatsApp.

### 1️⃣ Project Setup

1.  **Clone the Code:** Open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/ShreeNathX/WhatsApp-HealthCare-Bot
    cd whatsapp-healthcare-bot
    ```

2.  **Install Requirements:** Install all necessary Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create `.env` File:** Create a file named **`.env`** inside the `whatsapp-healthcare-bot` folder. This file holds your secret keys.

    Copy and paste the following template into your **`.env`** file. **You must replace the placeholder values with your actual keys.**

    ```env
# 🔑 OpenAI API Key for AI Reasoning and Voice Transcription
# Get yours from https://platform.openai.com
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-3.5-turbo

# 📞 Twilio Credentials (Required for WhatsApp Messaging)
TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN

# Flask Configuration (Keep these default)
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
    ```

### 2️⃣ Ngrok Setup (Create a Public Link)

Twilio needs a public internet address to send messages to your local Flask app. Ngrok handles this.

1.  **Download Ngrok:** Get the Ngrok executable from the [Ngrok Download Page](https://ngrok.com/download).
2.  **Authenticate:** Get your Auth Token from the [Ngrok Dashboard](https://dashboard.ngrok.com). In your terminal, run:
    ```bash
    ngrok config add-authtoken <YOUR_NGROK_AUTH_TOKEN>
    ```
3.  **Start Ngrok:** In a **new terminal window**, start Ngrok to tunnel port 5000.
    ```bash
    ngrok http 5000
    ```
    Keep this terminal window open! Ngrok will give you a **Forwarding URL** (e.g., `https://random-word.ngrok-free.app`). **Copy this HTTPS link.**

### 3️⃣ Run the Flask App

In your **original terminal window**, start the Python application:

```bash
python app.py
```
Keep this window open. It will show log messages when a user texts the bot.

### 4️⃣ Twilio WhatsApp Setup

1.  **Twilio Console:** Log in to your [Twilio Console](https://console.twilio.com/).
2.  **WhatsApp Sandbox:** Navigate to **Messaging** -> **Try it out** -> **Send a WhatsApp Message**.
3.  **Join Sandbox:** Follow the instructions to send the "join" code (e.g., `join <your-code>`) to the Twilio Sandbox number (`+1 415 523 8886`) from your personal WhatsApp to activate testing.
4.  **Set Webhook:** Scroll down to the **Sandbox Configuration** settings. Under "When a message comes in," paste your Ngrok URL from Step 2, adding `/whatsapp` to the end.

    *Example Webhook URL:* `https://random-word.ngrok-free.app/whatsapp`

5.  **Save** the configuration. Your bot is now live!

---

## 📱 How to Use Your Assistant

Send a message, an emergency word, or even a **voice note** to the Twilio Sandbox number: `+1 415 523 8886`.

### Example Queries:

* **Text Query (English):** `I have a fever, cough, and feel very tired.`
* **Text Query (Hindi):** `मुझे बुखार है और सिर दर्द हो रहा है।`
* **Voice Note:** Record yourself saying, "My child is vomiting and has a high temperature."
* **Emergency Test:** `chest pain` (The bot will immediately reply with the 108 emergency message).

---

## 📎 Important Notes

* **Security:** Always keep your **`.env`** file private and ensure it is listed in your **`.gitignore`** file.
* **Non-Diagnostic:** This tool is an assistant for **triage and safety**; it is **not a substitute for a doctor**.
---

# 🚀 Future Enhancements — WhatsApp AI Health Assistant (Powered by OpenAI)

This document outlines planned improvements and advanced features for future versions of the **AI Health Assistant**.  
The goal is to make the system more intelligent, scalable, and medically reliable while maintaining accessibility through **WhatsApp**.

---

## 🧠 1. Advanced AI Intelligence

- **Context Memory:**  
  Implement long-term conversation memory for personalized health interactions.  
  Example — The assistant remembers previous symptoms and follow-ups across multiple sessions.

- **Symptom Severity Scoring:**  
  Introduce a health risk scoring model using probabilistic AI or small neural networks to detect mild, moderate, and severe symptom patterns.

- **Medical Ontology Integration:**  
  Leverage standardized health datasets (like **SNOMED CT** or **ICD-10**) for structured and accurate symptom classification.

---

## 🗺️ 2. Smart Location & Hospital Integration

- **Google Maps / Places API:**  
  Automatically detect the user’s city or location (from chat metadata or user input) and show the **nearest verified hospitals or clinics**.

- **Real-time Emergency Routing:**  
  Display route maps to emergency centers based on GPS coordinates shared by the user.

- **Doctor Specialization Recommendation:**  
  Suggest specific **doctors or specialists** (Cardiologist, Neurologist, etc.) based on detected symptoms.

---

## 🩺 3. Data-Driven Health Insights

- **Symptom Trend Dashboard:**  
  Build a backend dashboard that shows trending diseases, common symptoms, and seasonal health patterns in specific regions.

- **Anonymous Data Collection:**  
  (With user consent) aggregate anonymized symptom data to improve healthcare resource planning and analytics.

---

## 💬 4. Enhanced Communication & UX

- **Voice-to-Voice Conversations:**  
  Integrate **OpenAI’s TTS (Text-to-Speech)** for natural two-way voice-based interactions.

- **Multimedia Health Education:**  
  Send visual infographics or short videos explaining first-aid steps and preventive care in regional languages.

- **Emotionally Aware Responses:**  
  Use sentiment analysis to adapt tone — calm during emergencies, friendly during routine health checks.

---

## 🧩 5. Architecture & Performance

- **Cloud Deployment:**  
  Migrate to **AWS / GCP / Azure** for scalability and 24×7 uptime.

- **Database Integration:**  
  Add **MongoDB** or **PostgreSQL** to store chat history, analytics, and health queries for research.

- **Caching System:**  
  Implement **Redis** or **Memcached** to handle high-volume message traffic efficiently.

---

## 🔒 6. Security and Compliance

- **End-to-End Encryption:**  
  Ensure secure transmission of sensitive chat data between users and servers.

- **HIPAA / GDPR Compliance:**  
  Follow privacy laws for health-related data, ensuring all user data is processed securely and ethically.

- **User Consent Management:**  
  Add consent-based data storage and retrieval mechanisms for full transparency.

---

## 🌍 7. Community and Expansion

- **Multilingual Expansion:**  
  Extend support to 15+ Indian and global languages with cultural and linguistic adaptation.

- **Partnership with Local Health Authorities:**  
  Collaborate with rural hospitals and NGOs to deliver verified medical information through WhatsApp.

- **Offline Mode (Future Research):**  
  Investigate low-bandwidth or SMS-based fallback systems for areas with limited internet access.

---

## 💡 Vision Statement

The **WhatsApp AI Health Assistant (Powered by OpenAI)** aims to become a trusted, scalable, and multilingual digital companion that bridges healthcare accessibility gaps worldwide.  
Through future AI advancements, real-time health insights, and verified medical integration, it will evolve into a **personalized, safe, and reliable digital triage partner** for every user.

---


## 👨‍💻 Author and Team
**Shree Nath Mahato (Leader)**  
📧 Contact: [shreenath.ventures17@gmail.com](mailto:shreenath.ventures17@gmail.com)

### Team Members
* **Arjun Chaudhary** - [GitHub Profile](https://github.com/Arzunchy).
* **Aditya Singh Baghel** – [GitHub Profile](https://github.com/ArBaghel).

* **Suraj Kumar** – [GitHub Profile](https://github.com/Suraj110905).




