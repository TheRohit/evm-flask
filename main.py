# Import necessary modules at the top
import cv2
import sys
from video_processing import pyramids, heartrate, preprocessing, eulerian



def process_video(video_path):
    freq_min = 1
    freq_max = 1.8

    print("Reading + preprocessing video...")
    video_frames, frame_ct, fps = preprocessing.read_video(video_path)

    print("Building Laplacian video pyramid...")
    lap_video = pyramids.build_video_pyramid(video_frames)

    heart_rate = None  # Initialize heart rate variable

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            continue

        print("Running FFT and Eulerian magnification...")
        result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        print("Calculating heart rate...")
        heart_rate = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)

    print("Rebuilding final video...")
    amplified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, frame_ct)

    print("Heart rate: ", heart_rate)
    return heart_rate
