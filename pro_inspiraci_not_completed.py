from ollama import chat
import pyttsx3
from poslech import main as listen

# Inicializace TTS
engine = pyttsx3.init()

#kratkodoba pamet
conversation_history = []

#mody
STANDBY = "STANDBY"
ACTIVE = "ACTIVE"

conversation_state = STANDBY
# Funkce pro komunikaci s LLM

def ask_llm(question: str) -> str:

    # Ulozeni otazky do historie
    conversation_history.append({
        "role": "user",
        "content": question
    })

    # Predani cele historie LLM
    stream = chat(
        model="gemma4",
        messages=conversation_history,
        stream=True
    )

    odpoved = ""

    for chunk in stream:
        odpoved += chunk["message"]["content"]

    # Ulozeni odpovedi do historie
    conversation_history.append({
        "role": "assistant",
        "content": odpoved
    })

    # Omezeni kratkodobe pameti na 10 vymen
    if len(conversation_history) > 20:
        del conversation_history[:-20]


# Hlavní konverzační smyčka
for i in range(2):

    # Získání hlasového vstupu
    full_otazka = listen()
    print(f"Otazka {i+1}: {full_otazka}")

    # Zpracování otázky pomocí LLM
    full_odpoved = ask_llm(full_otazka)
    print(f"Odpoved {i+1}: {full_odpoved}")

    # Hlasová odpověď
    engine.say(full_odpoved)
    engine.runAndWait()

