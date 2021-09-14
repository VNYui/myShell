import os
import sys
import pyaudio 
import speech_recognition as sr 
from google.cloud import texttospeech
import librosa 
from pathlib import Path
from pprint import pprint
import toml
class Elisa:
    def __init__(self):
        self.r = sr.Recognizer()
        #self.r.energy_threshold = 500
        
        #self.client = texttospeech.TextToSpeechClient()
        self.setup_path = Path.cwd() / 'Elisa/config.toml'
        self.conf = toml.load(self.setup_path) 
        self.device_index = int(self.conf.get('mic_devices'))
        self.mp3_path = Path.cwd() / 'voice/voice.mp3'

        while 'to keep Elisa alive':
            with sr.Microphone(device_index=self.device_index) as source:
                self.r.adjust_for_ambient_noise(source)
                self.audio = self.r.listen(source)    
                self.text = self.speech_to_text()

    def listen(self):
        return self.audio

    def speech_to_text(self):
        try:
          result = self.r.recognize_google(self.audio, language='fr-FR')
          words = result.lower()
          print(words)
          if words == 'ouvre un terminal':
              os.system('start cmd.exe')
          #self.speak()
          return words
        except LookupError:
          print("Please, speak more clearly")
        except sr.UnknownValueError:
          pass
          
    def create_mp3(self):
        synthesis_input = texttospeech.SynthesisInput(text=self.text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # The response's audio_content is binary
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
    
