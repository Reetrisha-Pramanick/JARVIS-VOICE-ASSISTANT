
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
from pathlib import Path
from urllib.parse import quote_plus

import pyttsx3
from openai import OpenAI
from config import apikey
from ddgs import DDGS


# OpenAI client
client = OpenAI(api_key=apikey)

# Store recent AI conversation messages
chat_history = []

# Folder for saving AI-generated responses
OUTPUT_DIR = Path(__file__).parent / "Openai"
OUTPUT_DIR.mkdir(exist_ok=True)

# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty("rate", 175)


def say(text):
    """Speak text aloud and display it in the terminal."""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def web_search(query):
    """Search the web, read out results, and open Google results."""
    try:
        print(f"\nSearching the web for: {query}")

        results = DDGS().text(query, max_results=3)

        if not results:
            say("Sorry, I couldn't find any search results.")
        else:
            say("I found some information on the web.")

            for index, result in enumerate(results, start=1):
                title = result.get("title", "Untitled result")
                summary = result.get("body", "No summary available")
                url = result.get("href", "")

                print(f"\nResult {index}: {title}")
                print(summary)
                print(url)

                say(f"Result {index}. {title}. {summary}")

        # Open Google with the requested search
        google_url = (
            "https://www.google.com/search?q=" + quote_plus(query)
        )
        webbrowser.open(google_url)

    except Exception as e:
        print(f"Web search error: {e}")
        say("Sorry, web search is unavailable right now.")

        # Still try opening the Google search page
        google_url = (
            "https://www.google.com/search?q=" + quote_plus(query)
        )
        webbrowser.open(google_url)


def chat(query):
    """Send a message to OpenAI and maintain conversation history."""
    global chat_history

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a helpful and concise voice assistant. "
                    "Respond naturally and clearly."
                )
            }
        ]

        messages.extend(chat_history[-10:])
        messages.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "Sorry, I couldn't generate a response."

        chat_history.extend([
            {"role": "user", "content": query},
            {"role": "assistant", "content": answer}
        ])

        say(answer)
        return answer

    except Exception as e:
        print(f"OpenAI error: {e}")
        say(
            "AI conversation is unavailable. "
            "I'll try searching the web instead."
        )
        web_search(query)
        return None


def ai(prompt):
    """Generate an AI response and save it to a text file."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        answer = response.choices[0].message.content or ""

        filename = f"response_{random.randint(100000, 999999)}.txt"
        output_file = OUTPUT_DIR / filename

        output_file.write_text(
            f"Prompt: {prompt}\n\nResponse:\n{answer}",
            encoding="utf-8"
        )

        print(f"Response saved to: {output_file}")
        say("I have saved the AI response to a text file.")

    except Exception as e:
        print(f"AI error: {e}")
        say("Sorry, I couldn't generate or save that response.")


def takeCommand():
    """Listen through the microphone and convert speech to text."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening... Speak now.")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=12
            )

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You: {query}")
        return query.strip()

    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")

    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")

    except Exception as e:
        print(f"Microphone error: {e}")

    return ""


def handleCommand(query):
    """Recognize commands and perform the appropriate action."""
    global chat_history

    if not query:
        return True

    command = query.lower().strip()

    # Open websites
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "google": "https://www.google.com"
    }

    for site, url in sites.items():
        if f"open {site}" in command:
            say(f"Opening {site}.")
            webbrowser.open(url)
            return True

    # Tell the current time
    if (
        "the time" in command
        or "what time" in command
        or command == "time"
    ):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        say(f"The time is {current_time}.")
        return True

    # Play a local music file
    if "open music" in command:
        music_path = Path.home() / "Music" / "downfall-21371.mp3"

        if music_path.exists():
            os.startfile(str(music_path))
            say("Playing music.")
        else:
            say(
                "I couldn't find the music file. "
                "Please check your Music folder."
            )

        return True

    # Open Notepad
    if "open notepad" in command:
        os.startfile("notepad.exe")
        say("Opening Notepad.")
        return True

    # Open Calculator
    if "open calculator" in command:
        os.startfile("calc.exe")
        say("Opening Calculator.")
        return True

    # Generate an AI response and save it
    if "using artificial intelligence" in command:
        ai(query)
        return True

    # Clear conversation history
    if "reset chat" in command:
        chat_history = []
        say("Conversation history cleared.")
        return True

    # Exit Jarvis
    if any(
        phrase in command
        for phrase in [
            "jarvis quit",
            "exit jarvis",
            "stop jarvis"
        ]
    ):
        say("Goodbye!")
        return False

    # Search the web directly
    if command.startswith("search for"):
        search_query = command[len("search for"):].strip()

        if search_query:
            web_search(search_query)
        else:
            say("Please tell me what you want to search for.")

        return True

    # Default: AI conversation
    chat(query)
    return True


if __name__ == "__main__":
    print("Welcome to Jarvis A.I.")
    say("Welcome to Jarvis A.I. How can I help you?")

    running = True

    while running:
        query = takeCommand()

        if query:
            running = handleCommand(query)
