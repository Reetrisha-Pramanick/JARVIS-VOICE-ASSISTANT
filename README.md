# 🤖 Jarvis — Python Voice Assistant

A Python-based desktop voice assistant that combines speech recognition, text-to-speech, web search, desktop automation, and optional AI-powered responses to make everyday computer tasks easier.

## ✨ Features

- **Voice Recognition:** Accepts voice commands using speech recognition.
- **Text-to-Speech:** Responds verbally using `pyttsx3`.
- **Web Search:** Searches the web for relevant information using DuckDuckGo.
- **Website Navigation:** Opens websites such as Google and YouTube.
- **Desktop Automation:** Launches supported desktop applications, such as Notepad and Calculator.
- **Time Assistance:** Provides the current time.
- **AI Integration:** Supports OpenAI-powered responses when a valid API key and available API quota are configured.
- **Search Fallback:** Uses web search for supported queries when AI responses are unavailable.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| SpeechRecognition | Voice input and speech recognition |
| PyAudio | Microphone audio capture |
| pyttsx3 | Text-to-speech output |
| OpenAI API | Optional AI-powered responses |
| DDGS | DuckDuckGo web search |
| Git & GitHub | Version control and project hosting |

## 📁 Project Structure

```text
JARVIS/
├── main.py
├── openaitest.py
├── config.py
├── config_example.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** `config.py` contains your local API configuration and should never be committed to GitHub. The file is excluded using `.gitignore`.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version supported by the installed dependencies
- Git
- A working microphone
- Internet connection for web search and optional OpenAI integration

### 1. Clone the repository

```bash
git clone https://github.com/Reetrisha-Pramanick/JARVIS-VOICE-ASSISTANT.git
cd JARVIS-VOICE-ASSISTANT
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, open a terminal where script activation is permitted or use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PyAudio installation fails, install a compatible wheel for your Python version and system architecture, or follow the PyAudio installation documentation.

### 4. Configure the API key (optional)

If you want to use OpenAI-powered responses, create a local file named `config.py` in the project root:

```python
apikey = "YOUR_OPENAI_API_KEY_HERE"
```

Replace the placeholder with your own API key.

**Security:** Never share or commit your API key. OpenAI API usage may require available billing credits or quota. Web-search functionality can still be used for supported queries without an active AI API response.

### 5. Run Jarvis

```bash
python main.py
```

Make sure your microphone is connected and allow microphone access when prompted.

## 🎙️ Example Commands

Depending on the implemented command handlers, you can try commands such as:

- "Open Google"
- "Open YouTube"
- "What time is it?"
- "Open Notepad"
- "Open Calculator"
- "Search for Python tutorials"

## 🔐 Security

- API credentials are kept in a local configuration file.
- `.gitignore` excludes sensitive configuration and generated files.
- Never publish API keys, passwords, or other secrets in source code or commit history.

## 🚀 Future Improvements

- Add a customizable wake word.
- Improve handling of speech recognition errors.
- Add more desktop automation commands.
- Introduce a graphical user interface.
- Expand conversational AI capabilities.
- Add command logging and configurable settings.

## 👩‍💻 Author

**Reetrisha Pramanick**

Electronics and Communication Engineering Student | Python Developer

[GitHub Profile](https://github.com/Reetrisha-Pramanick)

---

*Built as a hands-on project to explore Python, speech recognition, automation, and AI integration.*
