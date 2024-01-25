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


def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[9])  # 51, 59
    B = dist.euclidean(mouth[4], mouth[7])  # 53, 57

    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    C = dist.euclidean(mouth[0], mouth[6])  # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)

    # return the mouth aspect ratio
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

            lefteye = shape[L_start:L_end]
            righteye = shape[R_start:R_end]

            lefteyeHull = cv2.convexHull(lefteye)
            righteyeHull = cv2.convexHull(righteye)

            cv2.drawContours(frame, [lefteyeHull], -1, (255, 0, 0), 1)
            cv2.drawContours(frame, [righteyeHull], -1, (0, 0, 255), 1)

            left_EAR = calculate_EAR(lefteye)
            right_EAR = calculate_EAR(righteye)

            avg = (left_EAR + right_EAR) / 2

            if left_EAR < blink_thresh:
                keyboard.press("d")
            elif right_EAR < blink_thresh:
                keyboard.press("a")
            if right_EAR >= blink_thresh:
                keyboard.release("a")
            if avg >= blink_thresh:
                keyboard.release("d")
            cv2.putText(
                frame,
                "right eye: " + str(round(right_EAR, 2)),
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_4,
            )
            cv2.putText(
                frame,
                "left eye: " + str(round(left_EAR, 2)),
                (50, 250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_4,
            )

        cv2.imshow("Video", frame)
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()
