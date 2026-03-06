import whisper
import tempfile

# Load whisper model once
model = whisper.load_model("base")

def transcribe_audio(file):

    # Create a temporary file to store uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(file.read())
        temp_path = temp_audio.name

    # Run transcription
    result = model.transcribe(temp_path)

    return result["text"]
