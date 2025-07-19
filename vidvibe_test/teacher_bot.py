import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def load_transcript(file_path="transcript.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

TEACHER_PROMPT_TEMPLATE = """
You are a friendly and patient teacher chatbot.

The following transcript is a detailed explanation of a topic extracted from a YouTube video:

--------------------TRANSCRIPT--------------------
{transcript}
--------------------------------------------------

Your job is to:
1. First explain the transcript content in simple, step-by-step way like you’re teaching a beginner.
2. If a question is asked, answer only based on the transcript, and make the answer very **clear, slow, beginner-friendly, and **beautifully explained.
3. If the answer is not in the transcript, politely say: "Sorry, that wasn't covered in the transcript."

Always assume the student knows nothing.

Now answer this question:
"{question}"
"""

def ask_teacher_bot(transcript, question, model="gpt-3.5-turbo"):
    prompt = TEACHER_PROMPT_TEMPLATE.format(transcript=transcript, question=question)

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"