# 🩺 WhatsApp AI Health Assistant (Powered by Gemini)

A highly accessible and secure conversational AI assistant for **rural healthcare triage** and first aid advice, delivered through **WhatsApp**. This project uses **Google's Gemini AI** for powerful reasoning and voice transcription, and Twilio for messaging.

---

## ✅ Key Features

This AI is designed to act as a **safe, non-diagnostic** health assistant.

* 🤒 **Symptom Triage:** Analyzes complex symptoms and provides immediate, safe first aid and home care advice.
* 🧠 **Gemini Integration:** Utilizes **Gemini 2.5 Flash** for highly contextual, safe reasoning and to maintain conversation memory.
* 🎙️ **Voice Message Support (ASR):** Uses Gemini's multimodal power to **transcribe voice notes** into text, ensuring accessibility for all users.
* 🗣 **Multilingual Support:** Auto-detects and converses in **English, Hindi, Marathi, and Bengali**.
* 🚨 **Emergency Handoff:** Instantly recognizes critical keywords (e.g., "chest pain," "saans lene me dikkat") and directs the user to call **108** (Ambulance/Emergency).
* 🏥 **Referral Link:** Every response includes a **localized Google Maps link** to find the nearest health center immediately.

---

## 🛠 Tools Used

| Tool | Purpose |
| :--- | :--- |
| **Flask** | Lightweight web server to run the Python application. |
| **Twilio** | WhatsApp messaging API to receive and send messages. |
| **Ngrok** | Creates a secure public link to expose your local Flask server to Twilio. |
| **Gemini API** | The primary engine for **LLM Triage**, **Context Memory**, and **Voice Transcription (ASR)**. |
| **Langdetect** | Python library for automatic language detection. |
| **Google Maps Link** | Provides an actionable referral to nearby clinics. |

---

## ⚙️ Setup Guide (Step-by-Step for Beginners)

Follow these steps to get your AI Health Assistant running locally and connected to WhatsApp.

### 1️⃣ Project Setup

1.  **Clone the Code:** Open your terminal or command prompt and run:
    ```bash
    git clone [https://github.com/ShreeNath67/WhatsApp-HealthCare-Bot.git](https://github.com/ShreeNath67/WhatsApp-HealthCare-Bot.git)
    cd whatsapp-healthcare-bot
    ```

2.  **Install Requirements:** Install all necessary Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create `.env` File:** Create a file named **`.env`** inside the `whatsapp-healthcare-bot` folder. This file holds your secret keys.

    Copy and paste the following template into your **`.env`** file. **You must replace the placeholder values with your actual keys.**

    ```env
    # 🔑 Gemini API Key for AI Reasoning and Voice Transcription
    # Get yours from Google AI Studio.
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    GEMINI_MODEL=gemini-2.5-flash

    # 📞 Twilio Credentials (Required for WhatsApp Messaging)
    # Get these from your Twilio Console.
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

## 👨‍💻 Author and Team
**Shree Nath Mahato (Leader)**
📧 Contact: shreenath.ventures17@gmail.com

### Team Members
* **Arjun Chaudhary** - [GitHub Profile](https://github.com/Arzunchy).
* **Aditya Singh Baghel** – [GitHub Profile](https://github.com/ArBaghel).
* **Suraj Kumar** – [GitHub Profile](https://github.com/Suraj110905).