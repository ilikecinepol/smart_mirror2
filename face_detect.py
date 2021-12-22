import cv2
from face_recog import *
from PIL import Image, ImageDraw, ImageFont
import settings
import face_recog

face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#cap = cv2.VideoCapture(settings.stream)
cap = cv2.VideoCapture(0)
photo = False


def save_face():
    # Делаем снимок
    ret, frame = cap.read()

    # Записываем в файл
    # name = input('Как Вас зовут?')
    cv2.imwrite(f'humans_photo/current.png', frame)

    photo = True


def get_face():
    success, img = cap.read()
    # img = cv2.imread("IMG_20191012_145410_3.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    for (x, y, w, h) in faces:
        # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        crop_img = img[y:y + h, x:x + w]
        #cv2.imshow("cropped", crop_img)
        cv2.waitKey(0)
        cv2.imwrite(f'humans_photo/current.png', crop_img)
        cv2.destroyAllWindows()


def streaming():
    success, img = cap.read()
    # img = cv2.imread("IMG_20191012_145410_3.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    #text = (human1.out_info())
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if len(human1.out_info()[1])> 0:
            #cv2.putText(img, , ((x + w) // 2, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            pass

    cv2.imshow('rez', img)
    # cv2.waitKey()


def get_out_image(text, name):

    im = Image.open('humans_photo/bg.jpg')
    avatar = Image.open('humans_photo/current.png')
    # im.convert('RGB')
    # avatar.convert('RGB')
    font = ImageFont.truetype('Submarine Beach.ttf', size=30)
    draw_text = ImageDraw.Draw(im)
    im.paste(avatar, (0, 0))
    draw_text.text(
        (250, 0),
        ''.join(text.ljust(0)),
        # Добавляем шрифт к изображению
        font=font,
        fill='#000000')
    im.show()
    im.save(f"{name}.jpg")
    global photo
    photo = False


if __name__ == '__main__':

    print(photo)

    while True:
        #print(photo)
        if photo == False:
            get_face()
            human1 = FindCloneAPI()
            human1.photo = 'humans_photo/current.png'
            human1.login()
            human1.upload(human1.photo)
            text = (human1.out_info())
            # print(text)
            get_out_image(text[0], text[1])
            photo = True
        streaming()
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
