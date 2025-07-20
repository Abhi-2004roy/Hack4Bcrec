from gtts import gTTS
import os
import re

def clean_text_for_speech(text):
    """
    Clean text for natural speech synthesis by removing problematic newlines
    and formatting issues that cause unnatural pauses.
    
    Args:
        text (str): Raw text that may contain newlines and formatting issues
    
    Returns:
        str: Cleaned text optimized for speech synthesis
    """
    if not text:
        return ""
    
    # Step 1: Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Step 2: Split into lines and process each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Step 3: Check if this line ends with sentence-ending punctuation
        ends_with_punctuation = bool(re.search(r'[.!?]\s*$', line))
        
        # Step 4: Check if next line starts with a capital letter (new sentence)
        next_line_starts_sentence = False
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and re.match(r'^[A-Z]', next_line):
                next_line_starts_sentence = True
        
        # Step 5: Determine if we should add a pause (period) or just a space
        if ends_with_punctuation or next_line_starts_sentence:
            # This is a proper sentence break, keep it as is
            cleaned_lines.append(line)
        else:
            # This line doesn't end a sentence, add a space instead of newline
            if cleaned_lines:
                # Append to the previous line with a space
                cleaned_lines[-1] = cleaned_lines[-1] + " " + line
            else:
                # First line, just add it
                cleaned_lines.append(line)
    
    # Step 6: Join all lines with proper spacing
    cleaned_text = " ".join(cleaned_lines)
    
    # Step 7: Clean up multiple spaces and other formatting issues
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with single space
    cleaned_text = re.sub(r'\s+([.!?])', r'\1', cleaned_text)  # Remove spaces before punctuation
    cleaned_text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', cleaned_text)  # Ensure space after punctuation before capital
    
    # Step 8: Final cleanup
    cleaned_text = cleaned_text.strip()
    
    print(f"Text cleaned for speech: {len(text)} chars → {len(cleaned_text)} chars")
    return cleaned_text

def generate_audio_from_text(text, filename="summary.mp3", language="en"):
    """
    Convert text to speech and save as MP3 file
    
    Args:
        text (str): The text to convert to speech
        filename (str): Output filename (default: summary.mp3)
        language (str): Language code (default: en for English)
    
    Returns:
        str: Path to the generated audio file
    """
    try:
        # Clean the text for natural speech synthesis
        cleaned_text = clean_text_for_speech(text)
        
        if not cleaned_text:
            print("Error: No text content after cleaning")
            return None
        
        # Create gTTS object with cleaned text
        tts = gTTS(text=cleaned_text, lang=language, slow=False)
        
        # Save the audio file
        tts.save(filename)
        
        print(f"Audio file generated successfully: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None

def generate_summary_audio(summary_text):
    """
    Generate audio from summary text
    
    Args:
        summary_text (str): The summary text to convert to audio
    
    Returns:
        str: Path to the generated audio file or None if failed
    """
    if not summary_text or summary_text.strip() == "":
        print("Error: Summary text is empty")
        return None
    
    return generate_audio_from_text(summary_text, "summary.mp3")

if __name__ == "__main__":
    # Example usage with text containing newlines
    sample_text = """This is a sample summary text
that contains multiple lines with newlines.
Some lines end with proper punctuation.
While others don't have any punctuation
at the end of the line. This should be
converted to speech without unnatural pauses."""
    
    print("Original text:")
    print(repr(sample_text))
    print("\nCleaned text:")
    cleaned = clean_text_for_speech(sample_text)
    print(repr(cleaned))
    
    result = generate_summary_audio(sample_text)
    
    if result:
        print(f"\nAudio file created at: {os.path.abspath(result)}")
    else:
        print("\nFailed to create audio file") 