@@ .. @@
 from flask import Flask, request, render_template, send_file
 import yt_transcribe
 import teacher_bot
 import os
 from dotenv import load_dotenv
 load_dotenv()


 app = Flask(__name__)

 transcript_data = ""
 summary_data = ""
+qa_history = []

 @app.route("/", methods=["GET", "POST"])
 def index():
-    global transcript_data, summary_data
+    global transcript_data, summary_data, qa_history
     answer = None
     error_message = None
+    success_message = None
     selected_model = request.form.get("model", "gpt-3.5-turbo")

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
-                            answer = "Transcript and summary generated successfully. You can now ask questions."
+                            success_message = "Transcript and summary generated successfully!"
+                            # Clear previous Q&A history when new transcript is generated
+                            qa_history = []
                             
                 except Exception as e:
                     error_message = f"Error processing video: {str(e)}"
                     # Reset data on error
                     transcript_data = ""
                     summary_data = ""
+                    qa_history = []

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
+                    else:
+                        # Add to Q&A history
+                        qa_history.append({
+                            'question': question,
+                            'answer': answer
+                        })
+                        success_message = "Question answered successfully!"
                 except Exception as e:
                     error_message = f"Error processing question: {str(e)}"
                     answer = None

     return render_template("index.html", 
                          answer=answer, 
                          transcript=transcript_data, 
                          summary=summary_data, 
-                         error_message=error_message)
+                         error_message=error_message,
+                         success_message=success_message,
+                         qa_history=qa_history,
+                         selected_model=selected_model)