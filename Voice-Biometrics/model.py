import sounddevice as sd
from scipy.io.wavfile import write
from creatingData import extract_mfcc
import pandas as pd
from sklearn.neural_network import MLPClassifier
import time
import warnings
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)
def speaker_identifier():

    fs = 44100
    duration = 3
    print("speak team9 when the recording starts")
    engine.say("Speak team9 when the recording starts!")
    engine.runAndWait()

    time.sleep(0.1)
    print("recording started")

    rec = sd.rec(int((duration * fs)), samplerate=fs, channels=1)

    sd.wait()

    print("recording stopped")

    file = "data\\Temp_Data\\last_try.wav"
    write(filename=file, rate=fs, data=rec)
    mfcc = extract_mfcc(file, n_mfcc=40) 
    input = pd.DataFrame(columns=range(0, 40))
    lst = list(mfcc)
    input.loc[len(input)] = lst
    df = pd.read_csv("data\\Temp_Data\\complete_data.csv")
    X = df.drop(columns=["speaker", "Unnamed: 0"])
    Y = df["speaker"]
    classifier = MLPClassifier(solver='adam', alpha=0.001,random_state=1, max_iter=500,hidden_layer_sizes=100, activation="logistic")
    warnings.simplefilter("ignore")
    classifier.fit(X, Y)
    pred_mlp = classifier.predict(input)
    return pred_mlp[0]