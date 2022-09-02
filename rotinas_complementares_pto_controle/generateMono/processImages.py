import cv2

def processImages(path):
    stack_path = list(path.rglob('*.jpg')) + list(path.rglob('*.png'))
    imgs = [x for x in stack_path if x.parts[-2]=='3_Foto_Rastreio']
    for i in imgs:
        padImages(i)

def padImages(path):
    proportion = 2 # width/height
    img = cv2.imread(str(path))
    size = img.shape[:2]
    if size[1] < proportion*size[0]:
        lateral_pad = int((proportion*size[0]-size[1])/2)
        img = cv2.copyMakeBorder(img, 0,0,lateral_pad,lateral_pad,borderType=cv2.BORDER_CONSTANT, value=(255,255,255))
        cv2.imwrite(str(path),img)
