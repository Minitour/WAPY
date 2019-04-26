import cv2
import dlib
import numpy as np
from imutils import face_utils
import json
import math
import datetime

DEBUG = True
POSSIBLE_CAMERAS = 1

DISTANCE = 1

path_for_pictures = "./pictures_for_analysis/"
face_landmark_path = './shape_predictor_68_face_landmarks.dat'

K = [6.5308391993466671e+002, 0.0, 3.1950000000000000e+002,
     0.0, 6.5308391993466671e+002, 2.3950000000000000e+002,
     0.0, 0.0, 1.0]
D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e+000]

cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                         [1.330353, 7.122144, 6.903745],
                         [-1.330353, 7.122144, 6.903745],
                         [-6.825897, 6.760612, 4.402142],
                         [5.311432, 5.485328, 3.987654],
                         [1.789930, 5.393625, 4.413414],
                         [-1.789930, 5.393625, 4.413414],
                         [-5.311432, 5.485328, 3.987654],
                         [2.005628, 1.409845, 6.165652],
                         [-2.005628, 1.409845, 6.165652],
                         [2.774015, -2.080775, 5.048531],
                         [-2.774015, -2.080775, 5.048531],
                         [0.000000, -3.116408, 6.097667],
                         [0.000000, -7.415691, 4.070434]])

reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]


def get_head_pose(shape):
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])

    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix,
                                        dist_coeffs)

    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # calc euler angle
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle


def get_available_cameras():

    cameras = []

    for index_for_camera in range(0, POSSIBLE_CAMERAS):

        try:
            # trying to connect to camera with specific index
            camera = cv2.VideoCapture(index_for_camera)

            # append to available cameras
            if camera:
                print("got camera: " + str(camera))
                cameras.append(camera)

        except Exception as error:
            if DEBUG:
                print(error)

    # returning the available cameras
    return cameras


# default cameras:
    # index == 0 -> the computer camera
    # index == 1 -> external camera
    # index > 1 -> other cameras -> we will not implement more than one camera BUT SUPPORTED
def get_default_camera(cameras, index_for_camera=0, external=False):

    if len(cameras) == 0:
        return None

    if len(cameras) == 1 and not external:
        return cameras[index_for_camera]

    if len(cameras) == 1 and external:
        return None

    if len(cameras) > 1 and not external:
        return cameras[index_for_camera]

    if external:
        return cameras[index_for_camera]


def save_frame_as_picture(frame):

    raw_timestamp = datetime.datetime.now()

    # example: raw_timestamp -> 2019-03-12 08:14:47.501562
    timestamp = str(raw_timestamp).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")

    cv2.imwrite(path_for_pictures + timestamp + ".jpg", frame)

    if DEBUG:
        print("saved photo with timestamp:" + str(timestamp) + ".jpg")


def main():
    # return

    external = False

    # getting all available cameras that are connected to the compute stick
    cameras = get_available_cameras()

    # getting the camera we want to use -> default => the computer camera
    # to get the external camera you can add True parameter to this function and also select the number of the camera
    # if you do not specific any index/external parameter -> will get the default one (computer)
    # example: cap = get_default_camera(cameras, 1, True)
    cap = get_default_camera(cameras, external)

    # if the external param is True -> cap might be equal to [] if the function cant find a connected camera
    if (cap is None) or (not cap.isOpened()):
        print(cap)
        print("Unable to find camera.")
        return ["NO_CAMERAS"]

    # init the detector
    detector = dlib.get_frontal_face_detector()

    # init the predictor
    predictor = dlib.shape_predictor(face_landmark_path)

    # init an array for the points we will find
    points = [] # tuples (x,y)

    # index when we will take the frame and get the emotions from the picture
    index = 1
    while cap.isOpened():

        index += 1

        ret, frame = cap.read()

        # after 1000 frames we are saving one photo
        if index % 5 == 0:
            save_frame_as_picture(frame)

        # getting the width and height from the video
        width = cap.get(3)
        height = cap.get(4)

        if DEBUG:
            print(width)
            print(height)

        # we are still getting video from the camera
        if ret:

            # getting the face rectangle from the frame
            face_rects = detector(frame, 0)

            # if we found some face/s in the frame
            if len(face_rects) > 0:

                # start to analyse the face/s in the frame
                for face in face_rects:
                    shape = predictor(frame, face)
                    shape = face_utils.shape_to_np(shape)

                    # estimate the head pose of the specific face
                    reprojectdst, euler_angle = get_head_pose(shape)
                    #print(reprojectdst)

                    # draw points for the face
                    for (x, y) in shape:
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                    x = width/2 - int((euler_angle[1, 0]/30)*(width/2)*(DISTANCE)) # the 30 parameter should be the angel up and down of the camera
                    y = height/2 + int((euler_angle[0, 0]/30)*(height/2)*(DISTANCE))
                    print(euler_angle)
                    cv2.circle(frame, (int(x), int(y)), 3, (10, 20, 20), 2)
                    points.append((x,y))

                    if DEBUG:
                        print("x: " + str(x) + ", y: " + str(y))

                    with open("./points.json", "r") as json_file:
                        values = json.load(json_file)
                        results = values['results']
                        new_results = insert_x_y(x,y, results)
                        to_json_results = {"results": new_results}
                        with open("./points.json", "w") as json_file:
                            json.dump(to_json_results, json_file)

                            if DEBUG:
                                print("updated json file")

            cv2.imshow("demo", frame)
            array_list = []
            if cv2.waitKey(1) & 0xFF == ord('q'):
                for (x, y) in points:
                    array_list = insert_x_y(x,y, array_list)

                array_list = finilize_to_send(array_list)
                break


def insert_x_y(x,y, array_list):
    entered = False
    for i in range(0, len(array_list)):
        if array_list[i]['x'] == x and array_list[i]['y'] == y:
            entered = True
            array_list[i]['value'] += 1
            break

    if not entered:
        array_list = check_close_pixel([x,y,1], array_list)
    return array_list


def check_close_pixel(pxl, array_list):
    dist_to_pixel = 10
    found = False
    for i in range(0,len(array_list)):
        if pxl[0] + dist_to_pixel <= array_list[i]['x'] or pxl[0] - dist_to_pixel >= array_list[i]['x']:
            if pxl[1] + dist_to_pixel <= array_list[i]['y'] or pxl[1] - dist_to_pixel >= array_list[i]['y']:
                array_list[i]['value'] += pxl[2]
                found = True
                break
    if not found:
        array_list.append({"x": pxl[0], "y": pxl[1], "value": pxl[2], "radius": 40})
    return array_list



def finilize_to_send(list_to_order):

    return list_to_order.sort(key=get_value)


def get_value(object):

    if (not object) or (object is None):
        return 0
    return object['value']




if __name__ == '__main__':
    main()