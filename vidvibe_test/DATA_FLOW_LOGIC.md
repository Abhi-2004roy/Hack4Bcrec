VidVibe - Data Flow Logic

TL;DR - Quick Overview

🚀 Application Startup
- Load environment variables and initialize Flask
- Set up global state (transcript_data, summary_data)
- Initialize frontend with theme preference
- Register event listeners and form handlers

📥 YouTube URL Processing
- User enters URL → Frontend validation (empty/invalid check)
- Valid URL → Backend processing → Extract video ID
- YouTube API call → Get transcript → Generate summary
- Save to file → Update global state → Display results

❓ Question & Answer Flow
- User asks question → Validate (transcript exists, question not empty)
- Load transcript → Create AI prompt → Call OpenAI API
- Process response → Check for errors → Display answer
- Auto-scroll to answer → Show success/error toast

🎨 Frontend Interactions
- Form submission → Show spinner → Validate → Submit
- Response received → Hide spinner → Display content
- Auto-scroll to relevant section → Show notifications
- Theme toggle → Update localStorage → Apply CSS changes

⚠ Error Handling
- Frontend validation → Prevent submission → Show error toast
- Backend exceptions → Catch errors → Set error messages
- API failures → Handle gracefully → User-friendly messages
- Network issues → Timeout handling → Retry mechanisms

💾 State Management
- Global variables (session-based transcript/summary)
- localStorage (theme preference persistence)
- File system (transcript.txt storage)
- DOM state (content visibility, form values)

🔄 User Journey
- Visit app → Load theme → Enter YouTube URL
- Generate transcript → View summary → Ask questions
- Get AI answers → Clear content → Start over
- Error recovery → Retry actions → Continue workflow

Overview
This document describes the complete data flow and logic patterns in the VidVibe application, from user input to AI-generated responses.

1. Application Initialization Flow

Startup Sequence
1. Flask app initialization (app.py)
   ├── Load environment variables (.env)
   ├── Initialize global variables
   │   ├── transcript_data = ""
   │   └── summary_data = ""
   └── Register routes

2. Frontend initialization (index.html)
   ├── Load CSS styles (static/style.css)
   ├── Initialize JavaScript modules
   ├── Set up event listeners
   ├── Load theme preference (localStorage)
   └── Display initial interface

Theme Management Flow
User Theme Selection
    ↓
localStorage.setItem('darkMode', boolean)
    ↓
document.body.classList.toggle('dark-mode')
    ↓
CSS variables update
    ↓
Visual theme change

2. YouTube URL Processing Flow

Input Validation Chain
User enters YouTube URL
    ↓
Frontend Validation (JavaScript)
    ├── Check if URL is empty
    │   ├── TRUE: Show error toast, prevent submission
    │   └── FALSE: Continue
    └── Validate URL format (Regex)
        ├── Valid: Continue to backend
        └── Invalid: Show error toast, prevent submission

Backend Processing Chain
Valid URL received
    ↓
extract_video_id(youtube_url)
    ├── Apply regex patterns
    ├── Extract 11-character video ID
    └── Return video_id or None
        ├── None: Raise ValueError
        └── Valid ID: Continue
    ↓
YouTubeTranscriptApi.get_transcript(video_id)
    ├── API call to YouTube
    ├── Handle exceptions:
    │   ├── TranscriptsDisabled
    │   ├── NoTranscriptFound
    │   ├── VideoUnavailable
    │   └── General exceptions
    └── Return transcript_list
    ↓
Process transcript_list
    ├── Join text entries
    ├── Save to transcript.txt
    └── Return processed transcript

Summary Generation Flow
Transcript received
    ↓
summarize_transcript(transcript)
    ├── Truncate transcript (first 2000 chars)
    ├── Create OpenAI prompt
    ├── Call OpenAI API (gpt-3.5-turbo)
    ├── Handle API exceptions
    └── Return summary or error message
    ↓
Update global state
    ├── transcript_data = transcript
    ├── summary_data = summary
    └── success_message = "Transcript and summary generated successfully"

3. Question & Answer Flow

Question Validation Chain
User enters question
    ↓
Frontend Validation (JavaScript)
    ├── Check if transcript exists
    │   ├── FALSE: Show error toast, prevent submission
    │   └── TRUE: Continue
    ├── Check if question is empty
    │   ├── TRUE: Show error toast, prevent submission
    │   └── FALSE: Continue
    └── Submit to backend

AI Processing Chain
Valid question received
    ↓
ask_teacher_bot(transcript, question, model)
    ├── Load transcript from file
    ├── Create TEACHER_PROMPT_TEMPLATE
    │   ├── Include transcript context
    │   ├── Include user question
    │   └── Set teaching instructions
    ├── Call OpenAI API (selected model)
    ├── Handle API exceptions
    └── Return response or error message
    ↓
Response processing
    ├── Check if response starts with "❌ Error"
    │   ├── TRUE: Set error_message
    │   └── FALSE: Set success_message = "Question answered"
    └── Set answer = response

4. Frontend Interaction Flow

Form Submission Handling
Form submit event
    ↓
Prevent default behavior
    ↓
Show loading spinner
    ├── transcript-spinner (for YouTube URL)
    └── question-spinner (for questions)
    ↓
Submit form data
    ↓
Wait for response
    ↓
Hide spinner
    ↓
Handle response
    ├── Success: Show content, scroll to relevant section
    └── Error: Show error toast

Content Display Logic
Response received
    ↓
Template rendering (Jinja2)
    ├── {% if summary %} → Display summary box
    ├── {% if transcript %} → Display transcript box
    ├── {% if answer %} → Display answer box
    └── {% if error_message %} → Show error toast
    ↓
DOM mutation detected
    ↓
Auto-scroll logic
    ├── Summary generated: Scroll to summary
    ├── Answer generated: Scroll to answer
    └── No content: No scroll

Toast Notification Flow
Event triggers toast
    ↓
showToast(message, type)
    ├── Create toast element
    ├── Add close button
    ├── Set auto-dismiss timer (3.4s)
    ├── Add click handler for close button
    └── Append to toast container
    ↓
Toast display
    ├── Fade in animation
    ├── User can close manually
    └── Auto-fade out after timer

5. Error Handling Flow

Frontend Error Handling
Error condition detected
    ↓
Determine error type
    ├── Empty input
    ├── Invalid URL
    ├── No transcript loaded
    └── Empty question
    ↓
Show appropriate error toast
    ↓
Prevent form submission
    ↓
Hide loading spinner

Backend Error Handling
Exception occurs
    ↓
Try-catch block
    ├── YouTube API errors
    ├── OpenAI API errors
    ├── File I/O errors
    └── General exceptions
    ↓
Set error_message
    ↓
Return to template
    ↓
Display error toast

6. State Management Flow

Global State Variables
app.py global variables
    ├── transcript_data: Current transcript
    ├── summary_data: Current summary
    ├── error_message: Error notifications
    └── success_message: Success notifications

Local Storage State
Browser localStorage
    ├── darkMode: Theme preference
    └── Persistent across sessions

File System State
transcript.txt
    ├── Current transcript content
    ├── Overwritten on new video
    └── Available for download

7. User Interaction Patterns

Complete User Journey
1. User visits application
   ├── Load theme preference
   ├── Display empty interface
   └── Show dark mode toggle

2. User enters YouTube URL
   ├── Validate URL format
   ├── Show loading spinner
   ├── Generate transcript & summary
   ├── Display results
   ├── Auto-scroll to summary
   └── Show success toast

3. User asks question
   ├── Validate question & transcript
   ├── Show loading spinner
   ├── Generate AI response
   ├── Display answer
   ├── Auto-scroll to answer
   └── Show success toast

4. User clears content
   ├── Clear all form fields
   ├── Hide content sections
   └── Reset interface state

Error Recovery Patterns
Error occurs
    ↓
Show error toast
    ↓
Hide loading spinner
    ↓
Maintain form state
    ↓
Allow user to retry
    ↓
Clear error on next action

8. Performance Optimization Flow

Frontend Optimizations
DOM manipulation
    ├── Efficient selectors
    ├── Minimal reflows
    ├── Debounced events
    └── Optimized animations

Memory management
    ├── Event listener cleanup
    ├── Timer cleanup
    └── DOM element removal

Backend Optimizations
API calls
    ├── Error handling
    ├── Timeout management
    └── Response caching

File operations
    ├── Efficient I/O
    ├── Memory management
    └── Error recovery

9. Security Flow

Input Sanitization
User input received
    ↓
Template escaping (Jinja2)
    ├── HTML entities
    ├── XSS prevention
    └── Safe rendering

API Security
API calls
    ├── Environment variables
    ├── No hardcoded secrets
    └── Secure transmission

10. Data Persistence Flow

Session Data
Request cycle
    ├── Global variables (per session)
    ├── Template context
    └── Response rendering

Persistent Data
File storage
    ├── transcript.txt (current session)
    └── .env (configuration)

Browser storage
    ├── localStorage (theme preference)
    └── Session persistence