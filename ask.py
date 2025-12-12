from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
from pydub import AudioSegment
from pathlib import Path

load_dotenv()

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

current_file = Path(__file__).resolve()
current_dir = current_file.parent

script_dir = current_dir / "script"
script_dir.mkdir(exist_ok=True)

voices_dir = current_dir / "voices"
voices_dir.mkdir(exist_ok=True)

VOICES = {
    "Hobbes": "alloy",
    "Locke": "verse",
    "Rousseau": "sage"
}

def tts_to_file(text, voice, filename):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    )

    with open(filename, "wb") as f:
        f.write(response.read())

def parse_dialogue(full_text):
    parsed = []
    for line in full_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip()
            text = text.strip()
            parsed.append({"speaker": speaker, "text": text})
    return parsed

def make_audio_from_text(full_text):
    dialogues = parse_dialogue(full_text)
    output_files = []

    # 개별 TTS 생성
    for i, d in enumerate(dialogues):
        spk = d["speaker"]
        text = d["text"]
        voice = VOICES.get(spk, "alloy")

        filename = os.path.join(voices_dir, f"{i:03d}_{spk}.mp3")
        print(f"Generating audio: {filename}")
        tts_to_file(text, voice, filename)
        output_files.append(filename)

    # 오디오 합치기
    combined = AudioSegment.empty()
    for path in output_files:
        seg = AudioSegment.from_file(path)
        combined += seg + AudioSegment.silent(300)

    final_audio_path = os.path.join(
        voices_dir,
        f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    )

    combined.export(final_audio_path, format="mp3")
    print(f"\n🎧 Final audio created: {final_audio_path}\n")

def ask(ques):

    request_params = {
        "model": "gpt-4.1-mini",
        "input": f"""
            The user has asked the following question: "{ques}"

            Write a script in which Thomas Hobbes, John Locke, and Jean-Jacques Rousseau
            debate this question. Each philosopher should respond in his own distinctive
            voice and historical perspective.

            Format the output as a dialogue script, like:

            Hobbes: ...

            Locke: ...

            Rousseau: ...

            The philosophers should respond sequentially, challenge each other, and build
            on one another’s ideas, just like in a real debate.

            Requirements:

            Keep each philosopher’s voice consistent with his actual writings.
            Hobbes: mechanistic psychology, self-preservation, fear, power, sovereignty, the state of nature as war; sharp, cold, logical tone.
            Locke: natural rights, reason, consent, limited government, property, equality; calm, rational, optimistic tone.
            Rousseau: natural goodness of man, corruption by society, authenticity, sentiment, compassion (pitié); passionate, moralizing tone.

            Have them directly challenge each other using their own frameworks.
            (e.g., Hobbes attacks Rousseau’s optimism; Rousseau accuses Hobbes of cynicism; Locke mediates but also critiques both.)

            Ensure that each argument reflects historically accurate claims
            drawn from Leviathan, Second Treatise, and Discourse on Inequality.

            Avoid anachronisms and keep the reasoning grounded in themes they actually discussed.

            Make conversation in 1000 letters.
            """,
        "max_output_tokens": 1000,
        "stream": True
    }
    
    response = client.responses.create(**request_params)

    full_text = ""
    for event in response:
        if event.type == "response.output_text.delta":
            text = event.delta
            print(text, end="", flush=True)
            full_text += text

    print("\n\n--- End of Debate ---\n")
    filename = os.path.join(
        script_dir,
        f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_text)

    make_audio_from_text(full_text)

if __name__ == '__main__':
    while True:
        user_ques = input("Pose your question to Hobbes, Rousseau, and Locke: ")
        ask(user_ques)

    