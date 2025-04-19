import cv2  # OpenCV for video and image processing
import os  # File/directory handling
from pytube import YouTube  # Library to download videos from YouTube
from skimage.metrics import structural_similarity as ssim  # For comparing image similarity
import numpy as np  # Numerical operations

def download_video(youtube_url, save_as='video.mp4'):
    try:
        yt = YouTube(youtube_url) # Create YouTube object using the URL
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()  # Get best video quality
        stream.download(filename=save_as) # Download and save the video as video.mp4
        return save_as  # Return path of the downloaded file
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def extract_slides(video_path, output_folder='frames', interval=2, threshold=0.8):
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn’t exist
    cap = cv2.VideoCapture(video_path)  # Open the video file
    fps = int(cap.get(cv2.CAP_PROP_FPS)) # Get frames per second ,video is 30 fps, that means it shows 30 frames in one second.
    
    count = 0  # Frame counter
    slide_count = 0  # Number of slides saved
    prev_frame = None  # Holds the previous frame for comparison
    interval=1 #Save 1 frame every "1" second

    while True:
        ret, frame = cap.read() #cap.read() tries to read the next frame from the video->ret is boolean,next frame?
        if not ret:   # If no frame is read, break (end of video
            break
        
         # Every X seconds, check if this frame is different enough
        if count % (fps * interval) == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale

            if prev_frame is None:  # First frame? Always save it
                save_path = f"{output_folder}/slide_{slide_count}.jpg"
                cv2.imwrite(save_path, frame)  # Save image to disk
                slide_count += 1
            else:
                # Compare current frame with previous using SSIM
                score, _ = ssim(prev_frame, gray, full=True)
                if score < threshold:  # If difference is big enough (score low), save
                    save_path = f"{output_folder}/slide_{slide_count}.jpg"
                    cv2.imwrite(save_path, frame)
                    slide_count += 1

            prev_frame = gray  # Set current frame as previous for next loop
        
        count += 1
    
    cap.release()
