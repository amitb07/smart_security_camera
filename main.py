import cv2
import winsound

# capture the video
cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    # taking difference of frame1 & frame2, if there is any movement in video there will be some difference
    diff = cv2.absdiff(frame1,frame2)
    # converting the difference in grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    # blur the image
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    # the threshold will remove noise and show sharper difference
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    # using dilation to increase or scale the size of threshold images
    dilated = cv2.dilate(thresh, None, iterations=3)
    # to highlight the moving objects we use contours and they are highlighted in rectangle
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # to check only larger objects we add following condition, this can vary based on the position of camera
        if cv2.contourArea(c) < 5000:
            continue
        # construct a rectangle around the moving object
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # beep the sound when a large disturbance is observed Beep(freq, time), higher the freq higher the volume.
        winsound.Beep(300, 200)

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Camera Output', frame1)