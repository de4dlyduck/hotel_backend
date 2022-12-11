import datetime
import threading
import time
import atexit
import hashlib
import smtplib
import secrets
import string
from models.database import DATABASE_NAME, engine
from flask import Flask, jsonify, request
import create_database as db_creator
from sqlalchemy.orm import sessionmaker
from models.hotels import Rooms, Profile, Penalties, Reviews, Date
from sqlalchemy import desc
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False



@app.route('/hotel/1', methods=['GET'])
def show_hotel():
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Rooms).order_by(Rooms.cost).filter(Rooms.occupied == False).all()
    session.close()
    return jsonify(request)


@app.route('/hotel/2', methods=['GET'])
def show_hotel_reverse():
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Rooms).order_by(desc(Rooms.cost)).filter(Rooms.occupied == False).all()
    session.close()
    return jsonify(request)


@app.route('/hotel/admin/1', methods=['GET'])
def show_hotelAd():
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Rooms).order_by(Rooms.cost).all()
    session.close()
    return jsonify(request)


@app.route('/hotel/admin/2', methods=['GET'])
def show_hotelAd_reverse():
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Rooms).order_by(desc(Rooms.cost)).all()
    session.close()
    return jsonify(request)


@app.route('/api/hotel/reg', methods=['POST'])
def add_profile():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    name = str(profile['name'])
    surname = profile['surname']
    patronymic = profile['patronymic']
    password = hashlib.sha512(profile['password'].encode())
    serial = profile['serial']
    nomber = profile['nomber']
    mail = profile['mail']
    telNumber = profile['telNumber']
    type = profile['type']

    if ((len(str(serial)) != 4) and (len(str(nomber)) != 6) and (len(str(telNumber)) != 11)):
        session.close()
        return 'Error'

    else:
        try:
            if (len('') == 0):
                prof = Profile(name=name, surname=surname, patronymic=patronymic, password=password.hexdigest(),
                               serial=serial, nomber=nomber, mail=mail, telNumber=telNumber, type=type)
                session.add(prof)
                session.commit()
                return 'Success'
            else:
                session.close()
                return 'Error'
        except BaseException:
            session.close()
            return 'Error'

    session.close()
    return 'Error'


@app.route('/api/hotel/log', methods=['POST'])
def login_profile():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    email = profile['email']
    password = hashlib.sha512(profile['password'].encode())
    try:
        for user in session.query(Profile).filter(Profile.mail == email):
            if (user.password == password.hexdigest()):
                session.close()
                return f'Success{user.id}'
            else:
                session.close()
                return 'Error'
    except BaseException:
        session.close()
        return 'Error'


@app.route(f'/api/hotel/name/<user>', methods=['GET'])
def get_name(user):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Profile).filter(Profile.id == user).all()
    session.close()
    return jsonify(request)


@app.route(f'/api/hotel/nameTel/<user>', methods=['GET'])
def get_nameTel(user):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Profile).filter(Profile.telNumber == user).all()
    session.close()
    return jsonify(request)


@app.route('/api/hotel/remember/<emall>', methods=['GET'])
def send_password(emall):
    Session = sessionmaker(bind=engine)
    session = Session()
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
    smtpObj.starttls()
    smtpObj.ehlo()

    try:
        session.query(Profile).filter(Profile.mail == emall).update(
            {Profile.password: str(hashlib.sha512(password.encode()).hexdigest())})
        session.commit()
        session.close()
        smtpObj.login("hotelkurs@yandex.ru", "pzkknecqufjlkqqz")
        smtpObj.sendmail("hotelkurs@yandex.ru", str(emall), str(password))
        return "Success"
    except BaseException:
        return "Error"


@app.route('/api/hotel/penalties/<id_user>', methods=['GET'])
def send_penalties(id_user):
    Session = sessionmaker(bind=engine)
    session = Session()
    request_penalties = session.query(Penalties).filter(Penalties.id_user == id_user).all()
    session.close()
    return jsonify(request_penalties)


@app.route('/api/hotel/add/room', methods=['POST'])
def add_room():
    description: str
    cost: float
    personScore: int
    vans: int
    bedScore: int
    occupied: bool
    photo: str
    Session = sessionmaker(bind=engine)
    session = Session()
    room = request.json
    description = room['description']
    cost = room['cost']
    personScore = room['personScore']
    vans = room['vans']
    bedScore = room['vans']
    occupied = room['occupied']
    photo = room['photo']
    room = Rooms(description=description, cost=cost, personScore=personScore, vans=vans, bedScore=bedScore,
                 occupied=occupied, photo=photo)
    session.add(room)
    session.commit()
    session.close()
    return 'acces'


@app.route('/api/hotel/ref/room/<id_room>', methods=['POST'])
def ref_room(id_room):
    description: str
    cost: float
    personScore: int
    vans: int
    bedScore: int
    occupied: bool
    photo: str
    Session = sessionmaker(bind=engine)
    session = Session()
    room = request.json
    smt = session.query(Rooms).filter(Rooms.id==id_room).first()
    smt.description = room['description']
    smt.cost = room['cost']
    smt.personScore = room['personScore']
    smt.vans = room['vans']
    smt.occupied = room['occupied']
    smt.photo = room['photo']
    smt.bedScore = room['bedScore']
    session.commit()
    session.close()
    return 'acces'


@app.route('/api/hotel/add/penalties', methods=['POST'])
def add_penalties():
    description: str
    cost: float
    id_user: int
    Session = sessionmaker(bind=engine)
    session = Session()
    penalties = request.json
    description = penalties['description']
    cost = penalties['cost']
    id_user = penalties['id_user']
    penalties = Penalties(description=description, cost=cost, id_user=id_user)
    session.add(penalties)
    session.commit()
    session.close()
    return 'acces'


@app.route('/api/hotel/add/rew', methods=['POST'])
def add_rew():
    description: str
    id_user: int
    rating: int
    id_room: int
    Session = sessionmaker(bind=engine)
    session = Session()
    rew = request.json
    description = rew['description']
    rating = rew['rating']
    id_user = rew['id_profile']
    id_room = rew['id_rooms']
    prov = session.query(Reviews).filter(Reviews.id_profile==id_user).filter(Reviews.id_rooms==id_room).all()
    if(len(prov)!=0):
        print (str(prov))
        return 'error'
    rews = Reviews(description=description, rating=rating, id_profile=id_user, id_rooms=id_room);
    session.add(rews)
    session.commit()
    session.close()
    return 'acces'


@app.route('/api/hotel/reg/admin', methods=['POST'])
def add_profile_admin():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    name = str(profile['name'])
    surname = profile['surname']
    patronymic = profile['patronymic']
    password = hashlib.sha512(profile['password'].encode())
    serial = profile['serial']
    nomber = profile['nomber']
    mail = profile['mail']
    telNumber = profile['telNumber']
    type = profile['type']

    if (len(str(telNumber)) != 11):
        session.close()
        return 'Error'

    else:
        try:
            if (len('') == 0):
                prof = Profile(name=name, surname=surname, patronymic=patronymic, password=password.hexdigest(),
                               serial=serial, nomber=nomber, mail=mail, telNumber=telNumber, type=type)
                session.add(prof)
                session.commit()
                return 'Success'
            else:
                session.close()
                return 'Error'
        except BaseException:
            session.close()
            return 'Error'

    session.close()
    return 'Error'


@app.route('/api/hotel/rating/<id_room>', methods=['POST'])
def return_rat(id_room):
    rating = 0.0
    Session = sessionmaker(bind=engine)
    session = Session()
    request_rating = session.query(Reviews).filter(Reviews.id_rooms == id_room).all()
    for rat in request_rating:
        rating += rat.rating

    if(rating==0.0):
        session.close()
        return '0'
    session.close()
    return str(rating / len(request_rating))


@app.route('/api/hotel/rating/all/1/<id_room>', methods=['GET'])
def return_all_rat(id_room):
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Reviews.rating, Reviews.description, Profile.name, Profile.surname).join(Profile).filter(Reviews.id_rooms==id_room).filter(Profile.id==Reviews.id_profile).order_by(desc(Reviews.rating)).all()
    session.close()
    return jsonify([dict(r) for r in res])



@app.route('/api/hotel/rating/all/2/<id_room>', methods=['GET'])
def return_all_rat2(id_room):
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Reviews.rating, Reviews.description, Profile.name, Profile.surname).join(Profile).filter(Reviews.id_rooms==id_room).filter(Profile.id==Reviews.id_profile).order_by(Reviews.rating).all()
    session.close()
    return jsonify([dict(r) for r in res])

@app.route('/api/hotel/update/1', methods=['POST'])
def update1():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.name=data
    session.commit()
    session.close()
    return 'sucsess'


@app.route('/api/hotel/update/2', methods=['POST'])
def update2():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.surname=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/3', methods=['POST'])
def update3():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.patronymic=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/4', methods=['POST'])
def update4():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.serial=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/5', methods=['POST'])
def update5():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.nomber=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/6', methods=['POST'])
def update6():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.mail=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/7', methods=['POST'])
def update7():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.telNumber=data
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/update/8', methods=['POST'])
def update8():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    data = profile['data']
    id = profile['id']
    user = session.query(Profile).filter(Profile.id==id).first()
    user.password=hashlib.sha512(data.encode()).hexdigest()
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/deletPen', methods=['POST'])
def delPen():
    Session = sessionmaker(bind=engine)
    session = Session()
    profile = request.json
    id = profile['id']
    smt = session.query(Penalties).filter(Penalties.id==id).first()
    session.delete(smt)
    session.commit()
    session.close()
    return 'sucsess'

@app.route('/api/hotel/payRoom', methods=['POST'])
def payRoom():
    Session = sessionmaker(bind=engine)
    session = Session()
    day = request.json
    id=day['id']
    id_room= day['id_room']
    first_day = day['first_day']
    last_day = day['last_day']
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(8))
    try:
        day = Date(id_user=id, id_room=id_room, first_day=first_day, last_day=last_day, code=code)
        session.add(day)
        session.commit()
        session.close()
        return 'sucsess'
    except BaseException:
        session.close()
        return 'error'

@app.route('/api/hotel/UserRoom/<id>',methods=['GET'])
def getInfoByRoom(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Date).filter(Date.id_user==id).all()
    session.close()

    return jsonify(res)


@app.route('/api/hotel/UserAllRoom/<tel>',methods=['GET'])
def getInfoRooms(tel):
    Session = sessionmaker(bind=engine)
    session = Session()
    resbuf = session.query(Profile).filter(Profile.telNumber==tel).first()
    res = session.query(Date).join(Profile).filter(Date.id_user==resbuf.id).all()
    session.close()
    print(res)
    session.close()
    return jsonify(res)

@app.route('/api/hotel/delete/<id>',methods=['POST'])
def delRoom(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
       res = session.query(Rooms).filter(Rooms.id==id).first()
       res2 = session.query(Reviews).filter(Reviews.id_rooms==id).all()
       session.delete(res)
       session.commit()
       session.close()
       return 'success'
    except:
        return 'error'


@app.route('/api/hotel/ignore/<id>', methods=['POST'])
def ignoreRoom(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        res = session.query(Rooms).filter(Rooms.id == id).first()
        res.occupied=True
        session.commit()
        session.close()
        return 'success'
    except:
        return 'error'


@app.route('/api/hotel/deignore/<id>', methods=['POST'])
def deignoreRoom(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        res = session.query(Rooms).filter(Rooms.id == id).first()
        res.occupied=False
        session.commit()
        session.close()
        return 'success'
    except:
        return 'error'

def chek():
    now = datetime.datetime.now().date()
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Date).filter(Date.last_day == str(now)).all()
    session.delete(res)
    session.commit()
    session.close()
    return 'sucsess'



t=threading.Timer(86400,chek())
t.start()

if __name__ == '__main__':
    td=threading.Thread(app.run())
    td.start()
