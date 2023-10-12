import cv2
import numpy as np

# Path to the input video file
inputvid = 'video.mp4'

# Create a VideoCapture object to read from the video file
vidcap = cv2.VideoCapture(inputvid)

# Create a background subtractor object
bgsub = cv2.createBackgroundSubtractorMOG2()

while True:
    # Read the video frame
    suc, vidframe = vidcap.read()

    # If there are no more frames to show, break the loop
    if not suc:
        break

    # Apply the background subtractor to the frame
    foremask = bgsub.apply(vidframe)

    # Convert the mask to 3 channels
    foremask = cv2.cvtColor(foremask, cv2.COLOR_GRAY2BGR)

    # Apply the mask to the original frame to extract the person
    result = cv2.bitwise_and(vidframe, foremask)

    # Resize the frame and result to a smaller size
    scale_percent = 50  # Adjust this value to control the scaling
    winwidth = int(vidframe.shape[1] * scale_percent / 100)
    winheight = int(vidframe.shape[0] * scale_percent / 100)
    small_vidframe = cv2.resize(vidframe, (winwidth, winheight))
    small_result = cv2.resize(result, (winwidth, winheight))

    # Stack the resized frame and result horizontally
    hstacked_frames = np.hstack((small_vidframe, small_result))
    cv2.imshow("Original and Person Only", hstacked_frames)

    # If the 'q' key is pressed, stop the loop
    if cv2.waitKey(30) == ord("q"):
        break

# Release the video capture object
vidcap.release()
cv2.destroyAllWindows()
