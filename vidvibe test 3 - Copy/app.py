from flask import Flask, request, render_template, send_file
from flask import session
import yt_transcribe
import teacher_bot
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

transcript_data = ""
summary_data = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global transcript_data, summary_data
    answer = None
    error_message = None
    selected_model = request.form.get("model", "gpt-3.5-turbo")
    if request.method == "GET":
        session['qa_history'] = []
        qa_history = []
    else:
        qa_history = session.get('qa_history')
        if qa_history is None:
            qa_history = []

    if request.method == "POST":
        if "youtube_url" in request.form:
            youtube_url = request.form["youtube_url"]
            
            # Validate YouTube URL
            if not youtube_url or not youtube_url.strip():
                error_message = "Please enter a valid YouTube URL."
            else:
                try:
                    # Generate transcript
                    transcript = yt_transcribe.transcribe_from_url(youtube_url)
                    
                    # Validate transcript
                    if not transcript or not transcript.strip():
                        error_message = "Failed to generate transcript. The video might not have captions or they might be disabled."
                    else:
                        # Generate summary only if transcript is valid
                        summary = yt_transcribe.summarize_transcript(transcript)
                        
                        # Check if summary generation failed
                        if summary.startswith("❌"):
                            error_message = f"Failed to generate summary: {summary}"
                            transcript_data = transcript  # Keep transcript even if summary fails
                            summary_data = ""
                        else:
                            transcript_data = transcript
                            summary_data = summary
                            answer = "Transcript and summary generated successfully. You can now ask questions."
                            
                except Exception as e:
                    error_message = f"Error processing video: {str(e)}"
                    # Reset data on error
                    transcript_data = ""
                    summary_data = ""

        elif "question" in request.form:
            question = request.form["question"]
            
            # Validate that we have a transcript before asking questions
            if not transcript_data or not transcript_data.strip():
                error_message = "No transcript available. Please generate a transcript first by submitting a YouTube URL."
            elif not question or not question.strip():
                error_message = "Please enter a question."
            else:
                try:
                    answer = teacher_bot.ask_teacher_bot(transcript_data, question, selected_model)
                    
                    # Check if the answer indicates an error
                    if answer.startswith("❌"):
                        error_message = f"Error generating answer: {answer}"
                        answer = None
                    else:
                        # Append new Q&A to history
                        qa_history.append({'question': question, 'answer': answer})
                        session['qa_history'] = qa_history
                except Exception as e:
                    error_message = f"Error processing question: {str(e)}"
                    answer = None

    return render_template("index.html", 
                         answer=answer, 
                         transcript=transcript_data, 
                         summary=summary_data, 
                         error_message=error_message,
                         qa_history=qa_history)

@app.route("/download")
def download_transcript():
    """Download the transcript.txt file as an attachment"""
    try:
        transcript_path = os.path.abspath("transcript.txt")
        print(f"Attempting to serve transcript from: {transcript_path}")
        
        if os.path.exists(transcript_path):
            file_size = os.path.getsize(transcript_path)
            print(f"Transcript file found. File size: {file_size} bytes")
            return send_file(transcript_path, as_attachment=True, download_name="transcript.txt")
        else:
            print(f"Transcript file not found at: {transcript_path}")
            return "Transcript file not found. Please generate a transcript first.", 404
    except Exception as e:
        print(f"Error serving transcript file: {str(e)}")
        return f"Error serving transcript file: {str(e)}", 500

@app.route("/audio")
def serve_audio():
    """Serve the summary.mp3 file for download or in-browser playback"""
    try:
        if os.path.exists("summary.mp3"):
            return send_file("summary.mp3", mimetype="audio/mpeg")
        else:
            return "Audio file not found. Please generate a summary first.", 404
    except Exception as e:
        return f"Error serving audio file: {str(e)}", 500

@app.route("/download-audio")
def download_audio():
    """Download the summary.mp3 file as an attachment"""
    try:
        if os.path.exists("summary.mp3"):
            return send_file("summary.mp3", as_attachment=True, download_name="summary.mp3")
        else:
            return "Audio file not found. Please generate a summary first.", 404
    except Exception as e:
        return f"Error downloading audio file: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)