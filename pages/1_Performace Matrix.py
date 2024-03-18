import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have your pre-trained model loaded as 'model'

# Performance data (replace with your actual YOLOv8n performance metrics)
data_size = 12345  # Replace with actual data size
accuracy = 0.87  # Replace with actual accuracy
confusion_matrix = [[100, 20, 10],  # Replace with actual confusion matrix values
                    [15, 80, 5],
                    [5, 10, 85]]
precision = [0.9, 0.8, 0.85]  # Replace with actual precision values
recall = [0.92, 0.78, 0.82]  # Replace with actual recall values
fps = 30  # Replace with actual FPS

# Function to display confusion matrix as a table
def display_confusion_matrix(matrix):
  df = pd.DataFrame(matrix, index=['Predicted A', 'Predicted B', 'Predicted C'], columns=['Actual A', 'Actual B', 'Actual C'])
  st.write(df)

# Title and Introduction
st.title("YOLOv8n Model Performance")
st.write("This page presents key performance metrics for the pre-trained YOLOv8n model.")

# Data Size
st.header("Data Size")
st.write(f"{data_size:,} images used for training.")

# Accuracy
st.header("Accuracy")
st.write(f"The model achieved an accuracy of {accuracy:.2f}.")

# Confusion Matrix
st.header("Confusion Matrix")
display_confusion_matrix(confusion_matrix)

# Precision-Recall Curve (using matplotlib)
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='o', label='Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve for YOLOv8n')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# FPS
st.header("Frames Per Second (FPS)")
st.write(f"The model achieves an estimated real-time inference speed of approximately {fps} FPS.")

# Conclusion
st.write("This performance analysis provides insights into the capabilities of the YOLOv8n model. It's crucial to consider these metrics when evaluating the model's suitability for your specific use case.")
