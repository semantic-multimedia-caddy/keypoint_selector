import argparse
import cv2
import os
from functools import partial
from selector import KeypointSelector


def mouse_callback(event, 
                   x, y, 
                   flags, 
                   param, 
                   keypoint_buffer, 
                   keypoint_label_buffer):

    if event == cv2.EVENT_LBUTTONDOWN and len(keypoint_label_buffer) > 0:
        label = int("".join(keypoint_label_buffer))
        keypoint = (label, (x, y))
        filtered = list(filter(lambda kpt: kpt[0] == label, keypoint_buffer))

        if len(filtered) > 0:
            keypoint_buffer.remove(filtered[0])

        keypoint_buffer.append(keypoint)
        print(f"Keypoint of labeled {label} was set to x: {keypoint[1][0]}, y: {keypoint[1][1]}")

        keypoint_label_buffer.clear()


def main(args):
    video_filename = args.video.replace("\\", "/").split("/")[-1]
    keypoint_selector = KeypointSelector(args.video)

    running = True
    window_name = f"{video_filename} frame"
    cv2.namedWindow(window_name)

    while running:
        frame = keypoint_selector.get_frame(args.interval)
        keypoint_buffer = []
        keypoint_label_buffer = []
        
        cv2.setMouseCallback(window_name, partial(
            mouse_callback,
            keypoint_buffer=keypoint_buffer,
            keypoint_label_buffer=keypoint_label_buffer,
        ))

        cv2.imshow(window_name, frame)

        while True:
            key = cv2.waitKey()

            if key >= 48 and key < 58: # number input
                keypoint_label_buffer.append(chr(key))
                print("".join(keypoint_label_buffer))
            else:
                keypoint_label_buffer.clear()

                if key == ord("e") or key == ord("E"): # exit
                    running = False
                    break
                elif key == ord("z") or key == ord("Z"): # undo
                    if len(keypoint_buffer) > 0:
                        keypoint_buffer.pop(-1)
                elif key == ord("n") or key == ord("N"): # next frame
                    keypoint_selector.apply_keypoints(frame, keypoint_buffer)
                    break

    cv2.destroyAllWindows()

    output_path = os.path.join(args.savedir, "output", video_filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    keypoint_selector.save(output_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=str, help="path to video")
    parser.add_argument("--interval", required=False, default=1, type=int, help="path to video")
    parser.add_argument("--savedir", required=False, default=".", type=str, help="keypoint save directory")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
