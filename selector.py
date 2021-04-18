import cv2
import os


class KeypointSelector():

    def __init__(self, filename):
        if os.path.exists(filename):
            self.cap = cv2.VideoCapture(filename)
        else:
            raise ValueError(f"'{filename}' does not exists!")

        self.frames = []
        self.keypoints = []

    def get_frame(self, interval):
        for _ in range(interval):
            self.cap.read()

        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    def apply_keypoints(self, frame, keypoints):
        self.frames.append(frame)
        self.keypoints.append(keypoints)

    def save(self, dirpath):
        index = 0

        with open(os.path.join(dirpath, "keypoints.txt"), "w") as f:
            for frame, keypoints in zip(self.frames, self.keypoints):
                imgpath = os.path.join(dirpath, f"{index:08f}.jpg")
                cv2.imwrite(imgpath, frame)

                for keypoint in keypoints:
                    label = keypoint[0]
                    coord = keypoint[1]

                    f.write(f"{index}.jpg {label} {' '.join(map(str, coord))}\n")

                index += 1

        
