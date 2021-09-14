from sys import int_info
import pyaudio 
import speech_recognition as sr 
from google.cloud import texttospeech
import librosa 
from pathlib import Path

class Elisa:
    def __init__(self):
        self.r = sr.Recognizer()
        #self.client = texttospeech.TextToSpeechClient()
        self.mp3_path = Path.cwd() / 'voice/voice.mp3'

        while 'to keep Elisa alive':
            with sr.Microphone(device_index=2) as source:
                self.audio = self.r.listen(source)    
                self.text = self.speech_to_text()
    
    def listen(self):
        return self.audio

    def speech_to_text(self):
        try:
          result = self.r.recognize_google(self.listen(), language='fr-FR')
          words = result.lower()
          print('>', words)
          #self.speak()
          return words
        except LookupError:
          print("Please, speak more clearly")
        except sr.UnknownValueError:
          pass
          
    def create_mp3(self):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=self.text)
        # Build the voice request, select the language code ("fr-FR") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
    
    def speak(self):
        y, sample_rate = librosa.load(self.mp3_path)
        #Erase last message
        self.mp3_path.unlink()
        
if __name__ == '__main__':
    honey = Elisa()
    
