import cv2

file_name = "D:\\PW_mgr\\Sem2\\[CV3D] Computer Vision and 3D data processing\\proj\\data\\G5_tower.mp4"
cap = cv2.VideoCapture(file_name)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
high = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
no_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(no_frames)
for i in range(no_frames):
    ret, frame = cap.read()
    if i % 100 == 0:
        cv2.imwrite('frames/Frame_cap_%05d.jpg' % str(i), frame)
    if i % 500 == 0:
        print(i)
