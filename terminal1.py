import speech_recognition as sr

def pedestrian():
    """Function to handle pedestrian input"""
    print("Pedestrian detected. Take caution!")  # Replace with your desired action
    listen_for_input()  # Continue listening after pedestrian mode

def alert():
    """Function to handle alert input"""
    print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic
    listen_for_input()  # Continue listening after alert mode

def listen_for_input():
    """Continuously listens for user input and calls corresponding functions"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
      print("You can speak now.")
      while True:
        audio = recognizer.listen(source)
        try:
          text = recognizer.recognize_google(audio)
          text = text.lower()  # Convert input to lowercase for case-insensitive matching
          if "pedestrian" in text:
            pedestrian()
          elif "alert" in text:
            alert()
          elif "exit" in text:
            break  # Exit the listening loop
          else:
            print("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
        except sr.UnknownValueError:
          print("Could not understand audio")
        except sr.RequestError as e:
          print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    print("Welcome to ThirdEye")
    listen_for_input()
