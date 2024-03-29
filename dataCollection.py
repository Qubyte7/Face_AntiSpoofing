from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone
##############################
offsetPercentforH = 50
offsetPercentforw = 10
confidence = 0.85
##############################
# Initialize the webcam
# '2' means the third camera connected to the computer, usually 0 refers to the built-in webcam
cap = cv2.VideoCapture(0)

# Initialize the FaceDetector object
# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    # success: Boolean, whether the frame was successfully grabbed
    # img: the captured frame
    success, img = cap.read()

    # Detect faces in the image
    # img: Updated image
    # bboxs: List of bounding boxes around detected faces
    img, bboxs = detector.findFaces(img, draw=False)

    # Check if any face is detected
    if bboxs:
        # Loop through each bounding box
        for bbox in bboxs:
            center = bbox["center"]
            x, y, w, h = bbox['bbox']
            #SCORE
            score = bbox["score"][0]
        if score > confidence:
            #OFFSET ADDING
            offsetPixelsforw = int((offsetPercentforw / 100) * w)
            # Adjust the x coordinate and width
            x -= offsetPixelsforw
            w += 2 * offsetPixelsforw
            # Ensure width is not negative
            w = max(0, w)
            # Calculate offset in pixels for height
            offsetPixelsforh = int((offsetPercentforH / 100) * h)
            # Adjust the y coordinate and height
            y -= offsetPixelsforh
            h += offsetPixelsforh + 30
            # Ensure height is not negative
            h = max(0, h)
            # Calculate pt2
            pt2 = (x + w, y + h)
            blurValue = int (cv2.Laplacian(img,cv2.CV_64F).var())
            score = int(bbox['score'][0] * 100)
            cvzone.putTextRect(img, f'{score}%', (x, y - 10))
            cvzone.cornerRect(img, (x, y, w, h))
            cvzone.putTextRect(img,f'blur:{blurValue}',(x-120,y+20),2,2)

    # Display the image in a window named 'Image'
    cv2.imshow("Image", img)
    # Wait for 1 millisecond, and keep the window open
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()