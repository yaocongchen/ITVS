import os
import cv2

array_of_img = [] # this if for store all of the image data
# this function is for read image,the input is directory name
def read_directory(directory_name):
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    n=0
    for filename in os.listdir(r"./"+directory_name):
        #print(filename) #just for test
        #img is used to store the image data 
        img = cv2.imread(directory_name + "/" + filename)

        # 裁切區域的 x 與 y 座標（左上角）
        x = 504
        y = 0

        # 裁切區域的長度與寬度
        w = 1942
        h = 1942

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]
        image = cv2.resize(crop_img, (256, 256), interpolation=cv2.INTER_AREA)
        '''
        # 顯示圖片
        cv2.imshow("cropped", image)
        cv2.waitKey(0)
        '''
        # 寫入圖檔
        cv2.imwrite("./20201209/"+str(n+1)+'.jpg', image)
        n=n+1 #當有不止一個檔案的時候，依次對每一個檔案進行上面的流程

        array_of_img.append(img)
        #print(img)
        print(array_of_img)

# 讀取圖檔
#img = cv2.imread("1.jpg")
#read file
read_directory("20201023")
