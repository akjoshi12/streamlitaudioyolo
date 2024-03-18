## Version 7

import streamlit as st
import speech_recognition as sr
from ultralytics import YOLO
import pyttsx3
from threading import Thread, Event
from queue import Queue

model = YOLO("yolov8n.pt")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Create a queue to communicate between threads
speech_queue = Queue()

# Create an event to signal the object detection thread
detect_event = Event()

# Global variable to store the mode
mode = "pedestrian"  # Initial mode

def speech_worker():
    """Function to run in a separate thread for text-to-speech"""
    while True:
        speech_text = speech_queue.get()
        if speech_text is None:
            break
        engine.say(speech_text)
        engine.runAndWait()
        speech_queue.task_done()

def object_detection_worker():
    """Function to run in a separate thread for object detection"""
    while True:
        detect_event.wait()
        detect_event.clear()

        results = model.predict(source="0", stream=False)

        # Collect all detected objects in a list
        detected_objects = []

        # Display detected objects in Streamlit and collect them in a list
        for result in results:
            result_boxes = result.boxes
            for box in result_boxes:
                object_name = box.cls.name
                st.write(f"Object detected: {object_name}")
                detected_objects.append(object_name)

        # Add speech text to the queue
        speech_text = "Objects detected: " + ", ".join(detected_objects)
        speech_queue.put(speech_text)

        # Handle mode-specific actions
        if mode == "pedestrian":
            print("This is pedestrian mode")  # Replace with your desired action
        elif mode == "alert":
            # Flag to track if any object is coming near
            object_near = False

            # Collect objects coming near in a list
            near_objects = []

            # Display alert for objects coming near and collect them in a list
            for result in results:
                result_boxes = result.boxes
                for box in result_boxes:
                    # Calculate the area of the bounding box
                    box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

                    # Set a threshold area to determine if an object is near
                    THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

                    if box_area > THRESHOLD_AREA:
                        object_name = box.cls.name
                        st.write(f"Alert! {object_name} is coming near.")
                        near_objects.append(object_name)
                        object_near = True

            # Add speech text to the queue
            if near_objects:
                speech_text = "Alert! " + ", ".join(near_objects) + " are coming near."
                speech_queue.put(speech_text)

            # If no object is coming near, don't display or speak anything
            if not object_near:
                pass

            print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

# Start the speech worker thread
speech_thread = Thread(target=speech_worker, daemon=True)
speech_thread.start()

# Start the object detection worker thread
detection_thread = Thread(target=object_detection_worker, daemon=True)
detection_thread.start()

def listen_for_input():
    """Continuously listens for user input and calls corresponding functions"""
    global mode  # Declare the mode variable as global
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("You can speak now.")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                text = text.lower()  # Convert input to lowercase for case-insensitive matching
                if "pedestrian" in text:
                    mode = "pedestrian"  # No need for global here
                    st.write("Switched to pedestrian mode")
                    detect_event.set()
                elif "alert" in text:
                    mode = "alert"  # No need for global here
                    st.write("Switched to alert mode")
                    detect_event.set()
                elif "exit" in text:
                    break  # Exit the listening loop
                else:
                    st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
            except sr.UnknownValueError:
                st.write("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    st.write("Welcome to ThirdEye")
    listen_for_input()

    # Stop the speech worker thread
    speech_queue.put(None)
    speech_thread.join()

    # Stop the object detection worker thread
    detect_event.set()


## Version 6 

# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO
# import pyttsx3
# from threading import Thread
# from queue import Queue

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Create a queue to communicate between threads
# speech_queue = Queue()

# def speech_worker():
#     """Function to run in a separate thread for text-to-speech"""
#     while True:
#         speech_text = speech_queue.get()
#         if speech_text is None:
#             break
#         engine.say(speech_text)
#         engine.runAndWait()
#         speech_queue.task_done()

# # Start the speech worker thread
# speech_thread = Thread(target=speech_worker, daemon=True)
# speech_thread.start()

# def detect_objects(mode):
#     """Function to detect objects and handle mode-specific actions"""
#     results = model.predict(source="0", stream=False)

#     # Collect all detected objects in a list
#     detected_objects = []

#     # Display detected objects in Streamlit and collect them in a list
#     for result in results:
#         result_boxes = result.boxes
#         for box in result_boxes:
#             object_name = box.cls.name
#             st.write(f"Object detected: {object_name}")
#             detected_objects.append(object_name)

#     # Add speech text to the queue
#     speech_text = "Objects detected: " + ", ".join(detected_objects)
#     speech_queue.put(speech_text)

#     # Handle mode-specific actions
#     if mode == "pedestrian":
#         print("This is pedestrian mode")  # Replace with your desired action
#     elif mode == "alert":
#         # Flag to track if any object is coming near
#         object_near = False

#         # Collect objects coming near in a list
#         near_objects = []

#         # Display alert for objects coming near and collect them in a list
#         for result in results:
#             result_boxes = result.boxes
#             for box in result_boxes:
#                 # Calculate the area of the bounding box
#                 box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

#                 # Set a threshold area to determine if an object is near
#                 THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

#                 if box_area > THRESHOLD_AREA:
#                     object_name = box.cls.name
#                     st.write(f"Alert! {object_name} is coming near.")
#                     near_objects.append(object_name)
#                     object_near = True

#         # Add speech text to the queue
#         if near_objects:
#             speech_text = "Alert! " + ", ".join(near_objects) + " are coming near."
#             speech_queue.put(speech_text)

#         # If no object is coming near, don't display or speak anything
#         if not object_near:
#             pass

#         print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("You can speak now.")
#         while True:
#             audio = recognizer.listen(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()  # Convert input to lowercase for case-insensitive matching
#                 if "pedestrian" in text:
#                     detect_objects("pedestrian")
#                 elif "alert" in text:
#                     detect_objects("alert")
#                 elif "exit" in text:
#                     break  # Exit the listening loop
#                 else:
#                     st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#             except sr.UnknownValueError:
#                 st.write("Could not understand audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()

#     # Stop the speech worker thread
#     speech_queue.put(None)
#     speech_thread.join()




# #Version 5

# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO
# import pyttsx3
# from threading import Thread
# from queue import Queue

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Create a queue to communicate between threads
# speech_queue = Queue()

# def speech_worker():
#     """Function to run in a separate thread for text-to-speech"""
#     while True:
#         speech_text = speech_queue.get()
#         if speech_text is None:
#             break
#         engine.say(speech_text)
#         engine.runAndWait()
#         speech_queue.task_done()

# # Start the speech worker thread
# speech_thread = Thread(target=speech_worker, daemon=True)
# speech_thread.start()

# def pedestrian():
#     """Function to handle pedestrian input"""
#     print("This is pedestrian mode")  # Replace with your desired action

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=False)  # Change stream=True to stream=False

#     # Collect all detected objects in a list
#     detected_objects = []

#     # Display detected objects in Streamlit and collect them in a list
#     for result in results:
#         result_boxes = result.boxes
#         for box in result_boxes:
#             object_name = box.cls.name
#             st.write(f"Object detected: {object_name}")
#             detected_objects.append(object_name)

#     # Add speech text to the queue
#     speech_text = "Objects detected: " + ", ".join(detected_objects)
#     speech_queue.put(speech_text)

#     listen_for_input()  # Continue listening after pedestrian mode

# def alert():
#     """Function to handle alert input"""
#     print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=False)  # Change stream=True to stream=False

#     # Flag to track if any object is coming near
#     object_near = False

#     # Collect objects coming near in a list
#     near_objects = []

#     # Display alert for objects coming near and collect them in a list
#     for result in results:
#         result_boxes = result.boxes
#         for box in result_boxes:
#             # Calculate the area of the bounding box
#             box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

#             # Set a threshold area to determine if an object is near
#             THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

#             if box_area > THRESHOLD_AREA:
#                 object_name = box.cls.name
#                 st.write(f"Alert! {object_name} is coming near.")
#                 near_objects.append(object_name)
#                 object_near = True

#     # Add speech text to the queue
#     if near_objects:
#         speech_text = "Alert! " + ", ".join(near_objects) + " are coming near."
#         speech_queue.put(speech_text)

#     # If no object is coming near, don't display or speak anything
#     if not object_near:
#         pass

#     listen_for_input()  # Continue listening after alert mode

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("You can speak now.")
#         while True:
#             audio = recognizer.listen(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()  # Convert input to lowercase for case-insensitive matching
#                 if "pedestrian" in text:
#                     pedestrian()
#                 elif "alert" in text:
#                     alert()
#                 elif "exit" in text:
#                     break  # Exit the listening loop
#                 else:
#                     st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#             except sr.UnknownValueError:
#                 st.write("Could not understand audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()

#     # Stop the speech worker thread
#     speech_queue.put(None)
#     speech_thread.join()



# # Version 4 

# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO
# import pyttsx3
# from threading import Thread
# from queue import Queue

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Create a queue to communicate between threads
# speech_queue = Queue()

# def speech_worker():
#     """Function to run in a separate thread for text-to-speech"""
#     while True:
#         speech_text = speech_queue.get()
#         if speech_text is None:
#             break
#         engine.say(speech_text)
#         engine.runAndWait()
#         speech_queue.task_done()

# # Start the speech worker thread
# speech_thread = Thread(target=speech_worker, daemon=True)
# speech_thread.start()

# def pedestrian():
#     """Function to handle pedestrian input"""
#     print("This is pedestrian mode")  # Replace with your desired action

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Collect all detected objects in a list
#     detected_objects = []

#     # Display detected objects in Streamlit and collect them in a list
#     for result in results:
#         for box in result.boxes:
#             object_name = box.cls.name
#             st.write(f"Object detected: {object_name}")
#             detected_objects.append(object_name)

#     # Add speech text to the queue
#     speech_text = "Objects detected: " + ", ".join(detected_objects)
#     speech_queue.put(speech_text)

#     listen_for_input()  # Continue listening after pedestrian mode

# def alert():
#     """Function to handle alert input"""
#     print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Flag to track if any object is coming near
#     object_near = False

#     # Collect objects coming near in a list
#     near_objects = []

#     # Display alert for objects coming near and collect them in a list
#     for result in results:
#         for box in result.boxes:
#             # Calculate the area of the bounding box
#             box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

#             # Set a threshold area to determine if an object is near
#             THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

#             if box_area > THRESHOLD_AREA:
#                 object_name = box.cls.name
#                 st.write(f"Alert! {object_name} is coming near.")
#                 near_objects.append(object_name)
#                 object_near = True

#     # Add speech text to the queue
#     if near_objects:
#         speech_text = "Alert! " + ", ".join(near_objects) + " are coming near."
#         speech_queue.put(speech_text)

#     # If no object is coming near, don't display or speak anything
#     if not object_near:
#         pass

#     listen_for_input()  # Continue listening after alert mode

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("You can speak now.")
#         while True:
#             audio = recognizer.listen(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()  # Convert input to lowercase for case-insensitive matching
#                 if "pedestrian" in text:
#                     pedestrian()
#                 elif "alert" in text:
#                     alert()
#                 elif "exit" in text:
#                     break  # Exit the listening loop
#                 else:
#                     st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#             except sr.UnknownValueError:
#                 st.write("Could not understand audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()

#     # Stop the speech worker thread
#     speech_queue.put(None)
#     speech_thread.join()




# #Version 3

# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO
# import pyttsx3

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# def pedestrian():
#     """Function to handle pedestrian input"""
#     print("This is pedestrian mode")  # Replace with your desired action

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Display detected objects in Streamlit and speak them out
#     for result in results:
#         for box in result.boxes:
#             object_name = box.cls.name
#             st.write(f"Object detected: {object_name}")
#             engine.say(f"Object detected: {object_name}")
#             engine.runAndWait()

#     listen_for_input()  # Continue listening after pedestrian mode

# def alert():
#     """Function to handle alert input"""
#     print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Flag to track if any object is coming near
#     object_near = False

#     # Display alert for objects coming near and speak the alert
#     for result in results:
#         for box in result.boxes:
#             # Calculate the area of the bounding box
#             box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

#             # Set a threshold area to determine if an object is near
#             THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

#             if box_area > THRESHOLD_AREA:
#                 object_name = box.cls.name
#                 st.write(f"Alert! {object_name} is coming near.")
#                 engine.say(f"Alert! {object_name} is coming near.")
#                 engine.runAndWait()
#                 object_near = True

#     # If no object is coming near, don't display or speak anything
#     if not object_near:
#         pass

#     listen_for_input()  # Continue listening after alert mode

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("You can speak now.")
#         while True:
#             audio = recognizer.listen(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()  # Convert input to lowercase for case-insensitive matching
#                 if "pedestrian" in text:
#                     pedestrian()
#                 elif "alert" in text:
#                     alert()
#                 elif "exit" in text:
#                     break  # Exit the listening loop
#                 else:
#                     st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#             except sr.UnknownValueError:
#                 st.write("Could not understand audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()



#Version 2

# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine

# def pedestrian():
#     """Function to handle pedestrian input"""
#     print("This is pedestrian mode")  # Replace with your desired action

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Display detected objects in Streamlit
#     for result in results:
#         for box in result.boxes:
#             st.write(f"Object detected: {box.cls.name}")

#     listen_for_input()  # Continue listening after pedestrian mode

# def alert():
#     """Function to handle alert input"""
#     print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic

#     # Use YOLO model for object detection
#     results = model.predict(source="0", stream=True)  # Replace "0" with your camera source

#     # Flag to track if any object is coming near
#     object_near = False

#     # Display alert for objects coming near
#     for result in results:
#         for box in result.boxes:
#             # Calculate the area of the bounding box
#             box_area = (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])

#             # Set a threshold area to determine if an object is near
#             THRESHOLD_AREA = 10000  # Adjust this value based on your requirements

#             if box_area > THRESHOLD_AREA:
#                 st.write(f"Alert! {box.cls.name} is coming near.")
#                 object_near = True

#     # If no object is coming near, don't display anything
#     if not object_near:
#         pass

#     listen_for_input()  # Continue listening after alert mode

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("You can speak now.")
#         while True:
#             audio = recognizer.listen(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()  # Convert input to lowercase for case-insensitive matching
#                 if "pedestrian" in text:
#                     pedestrian()
#                 elif "alert" in text:
#                     alert()
#                 elif "exit" in text:
#                     break  # Exit the listening loop
#                 else:
#                     st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#             except sr.UnknownValueError:
#                 st.write("Could not understand audio")
#             except sr.RequestError as e:
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()



# import streamlit as st
# import speech_recognition as sr
# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")

# # Initialize text-to-speech engine

# def pedestrian():
#     """Function to handle pedestrian input"""
#     print("This is pedestrian mode")  # Replace with your desired action

#     # Display message in Streamlit (optional)
#     st.write("Pedestrian detected!")    
#     listen_for_input()  # Continue listening after pedestrian mode

# def alert():
#     """Function to handle alert input"""
#     print("Alert triggered! Sending emergency notification.")  # Replace with your notification logic
#     listen_for_input()  # Continue listening after alert mode

# def listen_for_input():
#     """Continuously listens for user input and calls corresponding functions"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#       st.write("You can speak now.")
#       while True:
#         audio = recognizer.listen(source)
#         try:
#           text = recognizer.recognize_google(audio)
#           text = text.lower()  # Convert input to lowercase for case-insensitive matching
#           if "pedestrian" in text:
#             pedestrian()
#           elif "alert" in text:
#             alert()
#           elif "exit" in text:
#             break  # Exit the listening loop
#           else:
#             st.write("Did not recognize input. Please say 'pedestrian', 'alert', or 'exit'.")
#         except sr.UnknownValueError:
#           st.write("Could not understand audio")
#         except sr.RequestError as e:
#           print("Could not request results from Google Speech Recognition service; {0}".format(e))

# if __name__ == "__main__":
#     st.write("Welcome to ThirdEye")
#     listen_for_input()


