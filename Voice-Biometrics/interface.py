import pyttsx3
import datetime
import speech_recognition as sr
from random import choice
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from AppOpener import open, close
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 180)
bot_name = "jarvis"
User_name = "Akash"
positive_response = ["Cool, I am on it sir!", " Okay sir, I'm working on it!", "Just a second sir!"]
negative_response = ["I think its invalid Command ", "I could not understand properly please speak again!","Sorry!, i don't know how to do this" ]
gratitude = ["I am happy to help!", "My pleasure sir!", "No problem!"]
email_id = "mandaakash6@gmail.com"
password = "eaea gcls nege aahs"
def speak(text):
    engine.say(text)
    engine.runAndWait()
def unauthorized():
    speak("You are unauthorized")
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 10)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
    except:
        return "I cannot recognize please speak again"
    query = str(query).lower()
    return query
def validate_command(query):
    if "open text file" in query:
        speak(choice(positive_response))
        new_text_file()
    elif "close " in query.lower():
        app_name = query.replace("close ", "").strip()
        close(app_name, match_closest=True,output=False)  # App will be close be it matches little bit too (Without printing conquery (like CLOSING <app_name>))
    elif "open " in query.lower():
        app_name = query.replace("open ", "")
        open(app_name, match_closest=True)
    elif "exit" in query:
        exit()
    elif "send whatsapp message" in query:
        speak(choice(positive_response))
        send_whatsapp_message()
    elif "search on wikipedia" in query:
        speak(choice(positive_response))
        search_on_wikipedia()
    elif "thank you" in query:
        speak(choice(gratitude)) #choice function selects random element from the array
    elif "send an email" in query:
        send_email()
    else:
        speak(choice(negative_response))
def send_email():
    try:
        speak("Whom do you want to mail?")
        receiver_address = ((take_user_input()+"@gmail.com").replace(" ","")).lower()
        print(receiver_address)
        speak("What should be the subject?")
        subject = take_user_input()  # take_user_input method is defined below
        speak("What should i write?")
        message = take_user_input()
        draft = EmailMessage()
        draft["To"] = receiver_address
        draft["subject"] = subject
        draft["From"] = email_id
        draft.set_content(message)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(email_id, password)
        s.send_message(draft)
        s.close()
        speak("Email sent successfully")
    except Exception as e:
        speak("There was an error!")
        print(e)
def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        audio = r.listen(source)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
        except Exception:
            speak('Sorry, I could not understand. Could you please say that again?')
            query = 'None'
        return query
def search_on_wikipedia():
    speak("What do you want to search?")
    query = take_user_input()
    results = wikipedia.summary(query, sentences=2)
    print(results)
    speak(results)
def new_text_file():
    speak("What will be the name of the file? ")
    file_name = take_user_input()
    file = "D:\Miniproject\\"+file_name + ".txt"
    f = open(file, "w+")
    speak("What do you want to write into the file"
          
          )
    content = take_user_input()
    f.write(content)
    speak("New text file made with name " + file_name)
    f.close()
def send_whatsapp_message():
    speak("whom do you want to send?")
    number = take_user_input().replace(" ","")
    print(number)
    speak("what do you want to send")
    message = take_user_input()
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def greet():
    current_time = datetime.datetime.now().hour
    if 4 < current_time <= 12:
        speak("Good morning and welcome to virtual assistant ")
    elif 12 < current_time <= 16:
        speak("Good afternoon and welcome to virtual assistant")
    elif 16 < current_time <= 21:
        speak("Good evening and welcome to virtual assistant ")
    elif 21 < current_time < 23 or 0 <= current_time <= 4:
        speak("Its a late night and welcome to virtual assistant ")
    speak("What would you like to do ?")
if __name__ == "__main__":
    greet()
    while True:
        query = take_command()
        print("You said \" " + query + " \"")
        validate_command(query)


