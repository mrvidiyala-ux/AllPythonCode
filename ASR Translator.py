import whisper
model=whisper.load_model("medium")
import whisper 
model=whisper.load_model("base")
audio=whisper.load_audio(r"C:\Users\Maniram.LAPTOP-2J12BJKB\Downloads\Recording.m4a")
audio=whisper.pad_or_trim(audio)
mel=whisper.log_mel_spectrogram(audio).to(model.device)
_,probs=model.detect_language(mel)
print(f"Detected language: {max(probs,key=probs.get)}")
options=whisper.DecodingOptions(task="translate", fp16=False)