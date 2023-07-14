import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import os

def draw_face_data(img, face, detector, f):
    point_left = face[145]
    point_right = face[374]

    # Draw line and circles
    cv2.line(img, point_left, point_right, (0, 200, 0), 3)
    cv2.circle(img, point_left, 5, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, point_right, 5, (255, 0, 255), cv2.FILLED)

    # Calculate face width and distance from camera
    face_width, _ = detector.findDistance(point_left, point_right)
    face_distance = (6.3 * f) / face_width

    # Print depth on the image
    cvzone.putTextRect(img, f'Depth: {int(face_distance)}cm', (face[10][0] - 100, face[10][1] - 50), scale=2)

    return img

def main():
    # Create a Streamlit sidebar
    st.sidebar.title('Face Distance Estimation')
    input_option = st.sidebar.selectbox('Input option', ['Select a video file', 'Use webcam'])
    focal_length = st.sidebar.number_input("Focal length", min_value=100, max_value=1000, value=840)

    # Create a Streamlit main area
    st.title('Face Detection Video')
    frame_slot = st.empty()

    # Initialize face detector
    detector = FaceMeshDetector(maxFaces=1)

    if input_option == 'Select a video file':
        video_file = st.sidebar.file_uploader("Upload video", type=['mp4', 'mov', 'avi'])

        # If video is uploaded, read from the file.
        if video_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(video_file.read())
        
            cap = cv2.VideoCapture(tfile.name)

            # Read video frames and process them
            while True:
                success, img = cap.read()
                if not success:
                    break

                img, faces = detector.findFaceMesh(img, draw=False)

                if faces:
                    img = draw_face_data(img, faces[0], detector, focal_length)

                # Display processed frame in Streamlit main area
                frame_slot.image(img, channels="BGR")

            os.unlink(tfile.name) # remove temporary file

    elif input_option == 'Use webcam':
        start_webcam = st.sidebar.button('Start webcam')

        if start_webcam:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.text("Cannot open webcam")
                return

            # Read video frames and process them
            while True:
                success, img = cap.read()
                if not success:
                    st.text("Failed to read frame")
                    break

                img, faces = detector.findFaceMesh(img, draw=False)

                if faces:
                    img = draw_face_data(img, faces[0], detector, focal_length)

                # Display processed frame in Streamlit main area
                frame_slot.image(img, channels="BGR")

            if cap is not None:
                cap.release()

if __name__ == "__main__":
    main()
