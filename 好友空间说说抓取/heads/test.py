import cv2
import  numpy as np

def corderange(img):
    focus = np.where(img > 14)
    return (focus[1][0],focus[0][0],focus[1][-1],focus[0][-1])

if __name__ == '__main__':
    img = cv2.imread('screenshot.png',0)
    cv2.imshow('test',img)
    focus = np.where(img>14)
    print(focus[0][0],focus[1][0])
    print(focus)
    print(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()