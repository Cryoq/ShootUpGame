img = "3hearts.png"
number = int(img[0])
imgList = list(img)
imgList[0] = str(number-1)
img = ''.join(imgList)
print(img)