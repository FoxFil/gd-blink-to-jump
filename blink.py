import cv2  # video rendering
import dlib  # detection
import imutils  # calculating
from scipy.spatial import distance as dist
from imutils import face_utils
import keyboard  # for pressing buttons

cam = cv2.VideoCapture(0)


def calculate_EAR(eye):
    # calculate the vertical distances
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])

    # calculate the horizontal distance
    x1 = dist.euclidean(eye[0], eye[3])

    # calculate the EAR
    EAR = (y1 + y2) / x1
    return EAR


blink_thresh = 0.4

# eyes landmarks
# (L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# face detection model initialazing
detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

x = 1

while 1:
    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT):
        cam.set(cv2.CAP_PROP_POS_FRAMES, 0)

    else:
        _, frame = cam.read()
        frame = imutils.resize(frame, width=640)

        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(img_gray)
        for face in faces:
            # landmark detection
            shape = landmark_predict(img_gray, face)

            shape = face_utils.shape_to_np(shape)

            # lefteye = shape[L_start:L_end]
            righteye = shape[R_start:R_end]

            # left_EAR = calculate_EAR(lefteye)
            right_EAR = calculate_EAR(righteye)

            # avg = (left_EAR + right_EAR) / 2

            if right_EAR < blink_thresh:
                keyboard.press("w")
            else:
                keyboard.release("w")
            # cv2.putText(
            #     frame,
            #     str(right_EAR),
            #     (50, 50),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     1,ww
            #     (0, 255, 255),
            #     2,
            #     cv2.LINE_4,
            # )

        cv2.imshow("Video", frame)
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()
