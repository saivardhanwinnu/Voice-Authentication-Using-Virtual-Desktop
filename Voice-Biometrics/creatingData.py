import sounddevice as sd
import librosa
import numpy as np
from scipy.io.wavfile import write
import pandas as pd
import os

# Record your voice n times, where n is input by the user
def record_audio():
    fs = 44100
    duration = 3

    print("How many recordings?")
    try:
        n = int(input())
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    for i in range(0, n + 1):
        try:
            print("Recording started")
            rec = sd.rec(int((duration * fs)), samplerate=fs, channels=1)
            sd.wait()
            print("Recording stopped")

            fileName = f"data\\akash{i}.wav"
            os.makedirs(os.path.dirname(fileName), exist_ok=True)  # Ensure the directory exists
            write(filename=fileName, rate=fs, data=rec)
            print(f"Saved recording as {fileName}")

        except Exception as e:
            print(f"An error occurred while recording: {e}")
            continue  # Skip to the next iteration

        print("Record again? (1 for Yes, 0 for No)")
        try:
            choice = int(input())
            if choice == 0:
                break
        except ValueError:
            print("Invalid input. Exiting recording.")
            break

# Used in model.py / used to return 40 MFCCs of a particular audio file
def extract_mfcc(file, n_mfcc=40):
    try:
        audio, sr = librosa.load(file, sr=None)  # Load audio with fallback sampling rate
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T, axis=0)
        return mfccs
    except Exception as e:
        print(f"Error extracting MFCC from {file}: {e}")
        return np.zeros(n_mfcc)  # Fallback: Return an array of zeros

# Extract MFCCs and save to CSV
def createMfccCsv():
    try:
        df = pd.DataFrame(columns=range(0, 40))
        for i in range(0, 20):
            fileName = f"data\\akash{i}.wav"
            if not os.path.exists(fileName):
                print(f"File {fileName} not found. Skipping.")
                continue  # Skip missing files

            mfccs = extract_mfcc(fileName, 40)
            lst = list(mfccs)
            df.loc[len(df)] = lst

        output_path = "data\\Temp_Data\\team9.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the directory exists
        df.to_csv(output_path, index=False)
        print(f"MFCC data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred while creating the MFCC CSV: {e}")

# Append individual data to complete data
def appendIndividualToCompleteCSV():
    try:
        complete_data_path = "data\\Temp_Data\\complete_data.csv"
        individual_data_path = "data\\Temp_Data\\team9.csv"

        if not os.path.exists(individual_data_path):
            print(f"File {individual_data_path} not found. Aborting.")
            return

        df1 = pd.read_csv(complete_data_path) if os.path.exists(complete_data_path) else pd.DataFrame()
        df2 = pd.read_csv(individual_data_path)
        df1 = pd.concat([df1, df2], ignore_index=True)

        os.makedirs(os.path.dirname(complete_data_path), exist_ok=True)  # Ensure the directory exists
        df1.to_csv(complete_data_path, index=False)
        print(f"Data successfully appended to {complete_data_path}")

    except Exception as e:
        print(f"An error occurred while appending data: {e}")

# Main Program Flow
if __name__ == "__main__":
    try:
        print("1. Record Audio\n2. Create MFCC CSV\n3. Append Individual Data to Complete CSV")
        choice = int(input("Choose an option: "))
        
        if choice == 1:
            record_audio()
        elif choice == 2:
            createMfccCsv()
        elif choice == 3:
            appendIndividualToCompleteCSV()
        else:
            print("Invalid choice. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
