import cv2
import dlib
import numpy as np
from imutils import face_utils
import json
import math

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


def main():
    # return
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to connect to camera.")
        return
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    points = [] # tuples (x,y)
    index = 1000
    while cap.isOpened():
        index += 1
        if index%1000 != 0:
            continue
        ret, frame = cap.read()
        width = cap.get(3)
        height = cap.get(4)
        print(width)
        print(height)
        if ret:
            face_rects = detector(frame, 0)

            if len(face_rects) > 0:
                for face in face_rects:
                    shape = predictor(frame, face)
                    shape = face_utils.shape_to_np(shape)

                    reprojectdst, euler_angle = get_head_pose(shape)
                    #print(reprojectdst)

                    for (x, y) in shape:
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                    looking_x_end = 0
                    looking_y_start = 0
                    looking_y_end = 0
                    looking_x_start = 0
                    # for start, end in line_pairs:
                    #     if start == 1 and end == 2:
                    #         looking_y_start = reprojectdst[start][1] + (reprojectdst[end][1] - reprojectdst[start][1])/2
                    #         cv2.line(frame, reprojectdst[start], reprojectdst[end], (255, 255, 0))
                    #     if start == 2 and end == 6:
                    #         looking_x_start = reprojectdst[start][0] + (reprojectdst[end][0] - reprojectdst[start][0]) / 2
                    #         cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))
                    #     if start == 3 and end == 0:
                    #         looking_y_end = reprojectdst[start][1] + (reprojectdst[end][1] - reprojectdst[start][1])/2
                    #         cv2.line(frame, reprojectdst[start], reprojectdst[end], (255, 255, 0))
                    #     if start == 3 and end == 7:
                    #         looking_x_end = reprojectdst[start][0] + (reprojectdst[end][0] - reprojectdst[start][0])/2
                    #         cv2.line(frame, reprojectdst[start], reprojectdst[end], (255, 255, 0))
                    #     else:
                    #         cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))
                        # if looking_y_start!=0 and looking_x_start!=0 and looking_y_end!=0 and looking_x_end!=0:
                        #     cv2.line(frame, (int(looking_x_start), int(looking_y_start)), (int(looking_x_end), int(looking_y_end)), (255, 255, 0))
                            #cv2.circle(frame, (int(looking_x_start), int(looking_y_start)), 3,(255, 255, 0),2)
                            #cv2.circle(frame, (int(looking_x_end), int(looking_y_end)), 3, (255, 255, 0), 2)

                    #math.sin()
                    dist = 1
                    x = width/2 - int((euler_angle[1, 0]/30)*(width/2)*(dist)) # the 30 parameter should be the angel up and down of the camera
                    y = height/2 + int((euler_angle[0, 0]/30)*(height/2)*(dist))
                    print(euler_angle)
                    cv2.circle(frame, (int(x), int(y)), 3, (10, 20, 20), 2)
                    points.append((x,y))
                    print("x: " + str(x) + ", y: " + str(y))
                    with open("./points.json", "r") as json_file:
                        values = json.load(json_file)
                        results = values['results']
                        new_results = insert_x_y(x,y, results)
                        to_json_results = {"results": new_results}
                        with open("./points.json", "w") as json_file:
                            json.dump(to_json_results, json_file)
                            print("updated json file")

            cv2.imshow("demo", frame)
            array_list = []
            if cv2.waitKey(1) & 0xFF == ord('q'):
                for (x, y) in points:
                    array_list = insert_x_y(x,y, array_list)
                print(array_list)
                # for l in array_list:
                #     print("x: " + str(l[0]) + ", y: " + str(l[1]) + ", value: " + str(l[2]) + "\n")

                # painting the picture
                # import paint_points
                # img = paint_points.start_painting(array_list)

                #json_values = {temp_values}
                # writing the points into the json file
                # with open("./points.json", "w") as json_file:
                #     to_json = {"results": array_list}
                #     json.dump(to_json, json_file)

                # showing the image with points
                # cv2.imshow("image", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
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


if __name__ == '__main__':
    main()