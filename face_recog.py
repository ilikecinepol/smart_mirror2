import requests
import settings

class FindCloneAPI:
    def __init__(self):
        self.phone = settings.phone
        self.pasw = settings.pasw

        self.session = requests.Session()
        self.headers = {
            "Connection": "keep-alive", "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        }
        self.session.headers.update(self.headers)
        self.data = None
        self.session_key = None
        self.user_id = None
        self.userid = None #id site
        self.quantity = 0
        self.total = 0
        self.photo = ''

    def login(self):
        try:
            url = 'https://findclone.ru/login'
            data = {'phone': self.phone, 'password': self.pasw}
            logging = self.session.post(url, data=data).json()
            print(logging)
            self.session_key = logging['session_key']
            self.headers.update({'session-key': self.session_key, 'user-id': str(logging['userid'])})
            self.quantity = logging['Quantity']
            self.userid = str(logging['userid'])
            self.session.headers.clear()
            self.session.headers.update(self.headers)
            print("Авторизация завершена")
        except Exception as e:
            print("Error: ", e)

    def upload(self, file):
        try:
            url = 'https://findclone.ru/upload2'
            files = {'uploaded_photo': ('photo.png', open(file, 'rb'), 'image/png')}
            self.session.headers.clear()
            self.session.headers.update(self.headers)
            upload = self.session.post(url, files=files).json()
            self.data = upload['data']
            self.quantity = upload['Quantity']
            self.total = upload['Total']
            print("Поиск завершен")
        except Exception as e:
            print("Error: ", e)

    def out_info(self):
        print("Осталось поисков: " + str(self.quantity))
        print("Найдено: " + str(self.total))
        self.data.reverse()
        person = self.data[-1]
        #self.name = name
        try:
            age = person['age']
        except:
            age = 'Не указан'
        try:
            city = person['city']
        except:
            city = 'Не указан'
        try:
            name = person['firstname']
        except:
            name = 'Не указан'
        try:
            score = person['score']
        except:
            score = 'Не указан'
        try:
            userid = person['userid']
        except:
            userid = 'Не указан'
        out_text = f"""
        ===========================
        Возраст: {age}
        Город: {city}
        Имя: {name}
        Уверенность: {int(score*100)}%
        Ссылка: https://vk.com/id{userid}
        """.format(age=age, city=city, name=name, score=score, userid=userid)
        print(out_text)
        return out_text, name

if __name__ == '__main__':

    human1 = FindCloneAPI()
    human1.photo = 'humans_photo/current.png'
    human1.login()
    human1.upload(human1.photo)
    human1.out_info()
