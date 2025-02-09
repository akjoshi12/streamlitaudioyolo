import cv2
import torch
from ultralytics import YOLO
import easyocr
import numpy as np
from collections import Counter 
import re
import streamlit as st

# Replace the relative path to your weight file
model_path = "/Users/atrijoshi/Downloads/AI&DS/Machine Learning/Code/Third_Eye_Modular/best_Model_Roboflow 1.pt"
source_path = "/Users/atrijoshi/Downloads/AI&DS/Machine Learning/Code/Third_Eye_Modular/st_4.jpeg"

# Initialize a Counter object to store text occurrences
text_occurrences_global = Counter()
# Set the number of frames you want to process
n_frames_to_process = 20

# Initialize a counter for processed frames
processed_frames_count = 0

# Assuming the YOLO model is loaded correctly with the correct import
model = YOLO(model_path)

# Open video capture
cap = cv2.VideoCapture(source_path)



def preprocess_for_ocr(im):
    # Set confidence threshold for OCR
    conf = 0.4
    
    # Resize the image to zoom in
    zoom_factor = 4  # Adjust this factor as needed
    resized_width = int(im.shape[1] * zoom_factor)
    resized_height = int(im.shape[0] * zoom_factor)
    zoomed_image = cv2.resize(im, (resized_width, resized_height), interpolation=cv2.INTER_NEAREST)

    # Apply noise reduction techniques for better OCR results
    blurred_image = cv2.GaussianBlur(zoomed_image, (5, 5), 0)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
    
    # # Adaptive thresholding
    # thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                cv2.THRESH_BINARY, 11, 2)
    return gray_image


# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Function to perform OCR on a region of interest (ROI) in an image
def getOCR(im, coors):
    # Extract coordinates of the region of interest (ROI)
    x, y, w, h = int(coors[0]), int(coors[1]), int(coors[2]), int(coors[3])
    # Crop the ROI from the image
    im = im[y:h, x:w]
    
    # Preprocess image for OCR
    preprocessed_im = preprocess_for_ocr(im)
    
    # Perform OCR on the preprocessed image
    results = reader.readtext(preprocessed_im)
    
    # Store occurrences of each recognized text
    text_occurrences = Counter()

    # Loop through OCR results
    for result in results:
        bbox, text, score = result
        if len(text) > 2:  # Ensure text is meaningful
            # Use regex to filter only alphabetic characters
            filtered_text = " ".join(re.findall("[A-Za-z]+", text))
            if filtered_text:  # Ensure filtered text is not empty
                # Convert to uppercase and remove spaces for better counting
                cleaned_text = filtered_text.upper()
                text_occurrences[cleaned_text] += 1

    # Return the most occurred text
    if text_occurrences:
        most_common_text = text_occurrences.most_common(1)[0][0]
        return most_common_text
    else:
        # If no common text found, return any single text if available
        if results:
            # Apply regex filter to the first recognized text before returning
            return " ".join(re.findall("[A-Za-z]+", results[0][1]))  # Return the first filtered text recognized
        else:
            return ""  # Return empty string if no text is found

# Replace 'model' and 'cap' variables with your actual YOLO model and video capture
# Assuming 'model' and 'cap' are already initialized in your code

# Initialize global counter for text occurrences across all frames
text_occurrences_global = Counter()

# Loop through video frames
while cap.isOpened() and processed_frames_count < n_frames_to_process:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection on the current frame
    results = model(frame)

    # Iterate over detected objects
    # Assuming 'results' is obtained from your YOLO detection
    street_plates = results[0]  # Assuming results[0] is the desired detection results for the current frame
    for street_plate in street_plates.boxes.data.tolist():
        x1, y1, x2, y2, _, _ = street_plate

        # Extract text from the detected region
        text = getOCR(frame, [x1, y1, x2, y2])
        print("Detected Text:", text)  # Printing the detected text

        # Add the detected text to the global counter
        if text:  # Ensure the text is not empty
            cleaned_text = text.upper()
            text_occurrences_global[cleaned_text] += 1
    
    # Increment the processed frames counter
    processed_frames_count += 1

    # # Display the frame with detections
    # cv2.imshow('YOLO Object Detection', frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# After processing all frames
if text_occurrences_global:
    most_common_text, occurrence = text_occurrences_global.most_common(1)[0]
    print("Most Occurred Text:", most_common_text, "with", occurrence, "occurrences")
else:
    print("No text detected.")

# Release video capture
cap.release()
cv2.destroyAllWindows()
