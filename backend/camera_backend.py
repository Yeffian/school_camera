import cv2 as cv
import yaml as yml
import time
import os
from datetime import datetime

config = yml.safe_load(open('../config.yml', 'r').read())
cap = cv.VideoCapture(0)


def load_cascade(name):
    return cv.CascadeClassifier(cv.data.haarcascades + f'haarcascade_{name}.xml')


face_cascade = load_cascade('frontalface_default')
body_cascade = load_cascade('fullbody')

recording = False
recording_stopped = None
timer_started = False

frame_size = (int(cap.get(3)), int(cap.get(4)))
writer = cv.VideoWriter_fourcc(*config['files']['codec'])

while True:
    _, frame = cap.read()

    output_buff = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(output_buff, config['cascades']['scaleFactor'], config['cascades']['minNeighbours'])
    bodies = face_cascade.detectMultiScale(output_buff, config['cascades']['scaleFactor'], config['cascades']['minNeighbours'])

    if len(faces) + len(bodies) > 0:
        if recording:
            timer_started = False
        else:
            recording = True
            current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            output = cv.VideoWriter(f"{config['files']['savePath']}{current_time}.mp4", writer, 20, frame_size)
            print("Started Recording!")
    elif recording:
        if timer_started:
            if time.time() - recording_stopped >= config['recordingDelay']:
                recording = False
                timer_started = False
                output.release()
                print('Stop Recording!')
        else:
            timer_started = True
            recording_stopped = time.time()

    if recording:
        output.write(frame)

    for (x, y, width, height) in faces:
        cv.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

    cv.imshow("Camera", frame)

    if cv.waitKey(1) == ord('q'):
        break

output.release()
cap.release()
cv.destroyAllWindows()