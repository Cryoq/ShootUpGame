img = "3hearts.png"
imgList = list(img)
number = int(img[0])
imgList[0] = str(number-1)
img = ''.join(imgList)
print(img)