import cv2
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
input = sys.stdin.readline

row_size = 512 # 사각형 크기
col_size = 512
window_size = 4 # 블러 크기
error_range = 30 # 오차범위

#이미지 설정
def img_resize(img,background):
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=(row_size, col_size), interpolation=cv2.INTER_AREA)
    background = cv2.resize(background, dsize=(row_size, col_size), interpolation=cv2.INTER_AREA)
    return img,background

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
# 스머징 구현
def Smudge_Tool(img):
    for i in range(img.shape[0]):
        for j in range(1,img.shape[1]):
            random_num = random.randrange(3)
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

#픽셀 출력
def print_pexels(img,background,rgb):
    for i in range(img.shape[0]-1):
        for j in range(img.shape[1]-1):
            if check_pexels(list(img[i][j]),rgb):
                background[i][j] = list(img[i][j])
    return background

if __name__ == '__main__':

    img = cv2.imread(r"img\train.png")
    background = cv2.imread(r"img\white_background.png")

    img, background = img_resize(img,background)
    img = Smudge_Tool(img)
    img = blurring_img(img)

    plt.imshow(img)
    plt.show()
    cv2.waitKey()
    cv2.destroyAllWindows()
    while(True):
        rgb = list(map(int, input().split()))
        background = print_pexels(img,background,rgb)
        plt.imshow(background)
        plt.show()
        cv2.waitKey()
        cv2.destroyAllWindows()



# print("back : ",background.shape)
# print("Size info : ",img.shape)
# print("Heght :" ,img.shape[0])
# print("colum :" ,img.shape[1])
# print("info type : ",type(img.shape[0]))

# print(type(img))
# print(img)

#cv2.waitKey()

#cv2.destroyAllWindows()


# 케니 엣지


