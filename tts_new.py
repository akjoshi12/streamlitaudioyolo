from ultralytics import YOLO
import pyttsx3
import cv2
import speech_recognition as sr
#initiate YOLO model
model = YOLO(r'yolov8n.pt')

#initiate tts engine and define properties
engine=pyttsx3.init()
engine.setProperty('rate',100)
engine.setProperty('volume',0.7)

r = sr.Recognizer()

#read video into cv2 and extract each frame to feed into YOLO prediction
video_path = r'/Users/atrijoshi/Downloads/AI&DS/Machine Learning/ThirdEye/walkstop.mp4'
cap = cv2.VideoCapture(video_path)
pred=''
while True:
    success, frame = cap.read()
    if not success:
        break  # If no frame is read, break the loop
    #predict
    results = model(frame,show=True)
    
    #get class id of prediction as a tensor from r.boxes inside results, convert into int and get class name from class id
    for r in results:
        for b in r.boxes:
            class_tensor=b.cls
            class_id=int(class_tensor.item())
            class_name=r.names[class_id]
            class_name=str(class_name)
            if pred==class_name:
                pass
            else:
                engine.say(class_name)
                engine.runAndWait()
                pred=class_name
        
# Release resources
cap.release()
cv2.destroyAllWindows()