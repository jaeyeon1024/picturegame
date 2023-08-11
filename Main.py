import os
import cv2
import random
import numpy as np

row_size = 256 # 사각형 크기
col_size = 256
window_size = 2 # 블러 크기
error_range = 30 # 오차범위
save_path = r"C:\Labs\picture_game\static\css\img\saves.jpg"
__image_path = r"static\css\img\meercat.jpg"
__instance = None

#이미지 설정
def img_resize(img,background):
    img = cv2.resize(img, dsize=(row_size, col_size), interpolation=cv2.INTER_AREA)
    background = cv2.resize(background, dsize=(row_size, col_size), interpolation=cv2.INTER_AREA)
    return img,background

# 스머징 구현
def Smudge_Tool(img):
    for i in range(img.shape[0]):
        for j in range(1,img.shape[1]):
            random_num = random.randrange(2)
            img[i,j],img[i-random_num,j-random_num] = img[i-random_num,j-random_num],img[i,j]
    return img

# 블러 구현
def blurring_img(img): 
    np_arr = np.array(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
        # 작은 윈도우
            pixel_sum = np.array([0,0,0])
            for _i in range(i-window_size, i):
                for _j in range(j-window_size, j):
                    pixel_sum += np_arr[_i][_j]
            pixel_mean = pixel_sum // (window_size * window_size)
            img[i][j] = list(pixel_mean)
    return img

# 픽셀 체크
def check_pexels(img_data:list, rgb:list) -> bool:
    check = True
    if img_data[0]-error_range > rgb[0] or img_data[0]+error_range < rgb[0]:
        check = False
    elif img_data[1]-error_range > rgb[1] or img_data[1]+error_range < rgb[1]:
        check = False
    elif img_data[2]-error_range > rgb[2] or img_data[2]+error_range < rgb[2]:
        check = False
    return check

#픽셀 출력
def print_pexels(img,background,rgb,save_path=None):
    for i in range(img.shape[0]-1):
        for j in range(img.shape[1]-1):
            if check_pexels(list(img[i][j]),rgb):
                background[i][j] = list(img[i][j])
    cv2.imwrite(save_path, background)
    return 

#
def __create(image_path = None):
    if image_path is not None:
        update(image_path)
    
    img = cv2.imread(__image_path)
    background = cv2.imread(r"static\css\img\white_background.jpg")

    img, background = img_resize(img,background)
    img = Smudge_Tool(img)
    img = blurring_img(img)
    return [img, background]

def update(path: str):
    global __image_path
    if not os.path.exists(path):
        raise FileNotFoundError()
    if not os.path.isfile(path):
        raise RuntimeError(f"This is not file ({path})")
    __image_path = path
    

def create(image_path = None):
    __instance = __create(image_path)
    return __instance


def get():
    if __instance is None:
        raise RuntimeError()
    return __instance

def reset(background):
    cv2.imwrite(save_path, background)

# 케니 엣지


