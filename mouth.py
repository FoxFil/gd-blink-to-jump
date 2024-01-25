import cv2  # video rendering
import dlib  # detection
import imutils  # calculating
from scipy.spatial import distance as dist
from imutils import face_utils
import keyboard  # for pressing buttons

cam = cv2.VideoCapture(0)


def mouth_aspect_ratio(mouth):

    A = dist.euclidean(mouth[2], mouth[9])
    B = dist.euclidean(mouth[4], mouth[7])

    C = dist.euclidean(mouth[0], mouth[6]) 

    mar = (A + B) / (2.0 * C)

    return mar


blink_thresh = 0.45
MOUTH_AR_THRESH = 0.6
(mStart, mEnd) = (49, 68)

# eyes landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
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

            # extract the mouth coordinates, then use the
            # coordinates to compute the mouth aspect ratio
            mouth = shape[mStart:mEnd]
            mar = mouth_aspect_ratio(mouth)

            # compute the convex hull for the mouth, then
            # visualize the mouth
            mouthHull = cv2.convexHull(mouth)

            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
            cv2.putText(
                frame,
                "mouth: {:.2f}".format(mar),
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

            # Draw text if mouth is open
            if mar > MOUTH_AR_THRESH:
                keyboard.press("w")
            else:
                keyboard.release("w")

        cv2.imshow("Video", frame)
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()
