 import pytesseract
import sys
from PIL import Image
def import_py():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def passImage(path):
    value = Image.open(path)
    return value
def convertTotext(img):
    text = pytesseract.image_to_string(img)
    return text
def main():
    import_py()
    image_path = input("enter the image path.....By default it is download.jpg") or "download.jpg"
    value = passImage(image_path)
    value = convertTotext(value)
    return value
value = main()
print("text on the image is : \n")
print(value + "\n")
s = input("do you want to write it on the file\n")
s.lower()
if s == "yes":
    path = input("enter the name of the file\n")
    f = open("notepad/" + path + ".txt" , "a")
    f.write(value)
    f.close()
    print("write successful\n")
else:
    s = input("Do you want to convert more images..")
    s.lower()
    if s == "yes":
        main()
    else:
        print("bye\n")
        sys.exit()


