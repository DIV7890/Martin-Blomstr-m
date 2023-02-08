from gtts import gTTS
import os

mytext = "one"
audio = gTTS(text=mytext, lang="en", slow=False)

audio.save("glosa.mp3")
os.system("glosa.mp3")
os.close("glosa.mp3")
mytext = "two"

audio.save("glosa.mp3")
os.system("glosa.mp3")