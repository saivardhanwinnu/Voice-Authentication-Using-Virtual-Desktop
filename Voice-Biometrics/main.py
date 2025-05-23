from interface import unauthorized
from model import speaker_identifier
if __name__ == "__main__":
    pred = speaker_identifier()
    if pred == 1:
        print("You are authorized!")
        exec(open("interface.py").read())
    else:
        print("Unauthorized !!")
        unauthorized()












