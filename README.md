Philosophical Debate Generator
Hobbes · Rousseau · Locke

This program generates a philosophical conversation between
Thomas Hobbes, Jean-Jacques Rousseau, and John Locke based on a user’s question.

Each philosopher responds in a distinct rhetorical style, and
audio (voice) files are generated alongside the text debate.

REQUIREMENTS

Python (Python 3 recommended)

Install required Python packages:
pip install openai
pip install pydub

Install ffmpeg (required for audio generation):
brew install ffmpeg


HOW TO USE (Terminal)

Open your terminal.

Navigate to the directory containing ask.py.

Run the program:
python ask.py

When prompted, pose your question to Hobbes, Rousseau, and Locke.

The program will:

Generate a conversation between the three philosophers

Save the debate as text files

Generate voice (audio) files for the responses

ENVIRONMENT SETUP (.env FILE)

You must create a file named ".env" in the SAME directory as ask.py.

Inside the .env file, add your OpenAI API key in the following format:

API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx

IMPORTANT:

Do NOT share your API key publicly.

Make sure the file name is exactly ".env" (no extra extension).
