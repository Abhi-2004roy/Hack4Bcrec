from flask import Flask, request, render_template, send_file
import yt_transcribe
import teacher_bot
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

transcript_data = ""
summary_data = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global transcript_data, summary_data
    answer = None
    selected_model = request.form.get("model", "gpt-3.5-turbo")

    if request.method == "POST":
        if "youtube_url" in request.form:
            youtube_url = request.form["youtube_url"]
            transcript = yt_transcribe.transcribe_from_url(youtube_url)
            summary = yt_transcribe.summarize_transcript(transcript)
            transcript_data = transcript
            summary_data = summary
            answer = "Transcript and summary generated successfully. You can now ask questions."

        elif "question" in request.form:
            question = request.form["question"]
            answer = teacher_bot.ask_teacher_bot(transcript_data, question, selected_model)

         


    return render_template("index.html", answer=answer, transcript=transcript_data, summary=summary_data)

@app.route("/download")
def download_transcript():
    return send_file("transcript.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)