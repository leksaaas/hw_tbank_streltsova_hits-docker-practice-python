#!/usr/bin/env python3

import logging
import os

import redis
import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line

# Default port; можно переопределить через переменную окружения PORT
PORT = int(os.environ.get("PORT", "8888"))


def get_redis() -> redis.StrictRedis:
    """Создаёт Redis-клиент на основе переменных окружения."""
    return redis.StrictRedis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        db=0,
    )


def get_id_or_init(r: redis.StrictRedis, key: str) -> int:
    """
    Безопасно возвращает autoID.
    Если ключа нет (например Redis пустой) — создаём его со значением 1.
    """
    raw = r.get(key)
    if raw is None:
        r.set(key, 1)
        return 1
    return int(raw.decode())


def init_db(r: redis.StrictRedis) -> None:
    """Инициализация Redis ключей, если база ещё не проинициализирована."""
    db_initiated = r.get("db_initiated")
    if not db_initiated:
        r.set("hospital:autoID", 1)
        r.set("doctor:autoID", 1)
        r.set("patient:autoID", 1)
        r.set("diagnosis:autoID", 1)
        r.set("db_initiated", 1)


class BaseHandler(tornado.web.RequestHandler):
    """Базовый handler: даёт доступ к Redis через настройки приложения."""

    @property
    def r(self) -> redis.StrictRedis:
        return self.application.settings["redis"]


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("OK")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


class HospitalHandler(BaseHandler):
    def get(self):
        items = []
        try:
            last_id = get_id_or_init(self.r, "hospital:autoID")
            for i in range(1, last_id):
                result = self.r.hgetall(f"hospital:{i}")
                if result:
                    items.append(result)

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.render("templates/hospital.html", items=items)

    def post(self):
        name = self.get_argument("name")
        address = self.get_argument("address")
        beds_number = self.get_argument("beds_number", default="")
        phone = self.get_argument("phone", default="")

        if not name or not address:
            self.set_status(400)
            self.write("Hospital name and address required")
            return

        logging.debug("%s %s %s %s", name, address, beds_number, phone)

        try:
            new_id = get_id_or_init(self.r, "hospital:autoID")
            key = f"hospital:{new_id}"

            a = 0
            a += self.r.hset(key, "name", name)
            a += self.r.hset(key, "address", address)
            a += self.r.hset(key, "phone", phone)
            a += self.r.hset(key, "beds_number", beds_number)

            self.r.incr("hospital:autoID")
        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            if a != 4:
                self.set_status(500)
                self.write("Something went terribly wrong")
            else:
                self.write(f"OK: ID {new_id} for {name}")


class DoctorHandler(BaseHandler):
    def get(self):
        items = []
        try:
            last_id = get_id_or_init(self.r, "doctor:autoID")
            for i in range(1, last_id):
                result = self.r.hgetall(f"doctor:{i}")
                if result:
                    items.append(result)

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.render("templates/doctor.html", items=items)

    def post(self):
        surname = self.get_argument("surname")
        profession = self.get_argument("profession")
        hospital_ID = self.get_argument("hospital_ID", default="")

        if not surname or not profession:
            self.set_status(400)
            self.write("Surname and profession required")
            return

        logging.debug("%s %s", surname, profession)

        try:
            new_id = get_id_or_init(self.r, "doctor:autoID")

            if hospital_ID:
                hospital = self.r.hgetall("hospital:" + hospital_ID)
                if not hospital:
                    self.set_status(400)
                    self.write("No hospital with such ID")
                    return

            key = f"doctor:{new_id}"
            a = 0
            a += self.r.hset(key, "surname", surname)
            a += self.r.hset(key, "profession", profession)
            a += self.r.hset(key, "hospital_ID", hospital_ID)

            self.r.incr("doctor:autoID")
        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            if a != 3:
                self.set_status(500)
                self.write("Something went terribly wrong")
            else:
                self.write(f"OK: ID {new_id} for {surname}")


class PatientHandler(BaseHandler):
    def get(self):
        items = []
        try:
            last_id = get_id_or_init(self.r, "patient:autoID")
            for i in range(1, last_id):
                result = self.r.hgetall(f"patient:{i}")
                if result:
                    items.append(result)

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.render("templates/patient.html", items=items)

    def post(self):
        surname = self.get_argument("surname")
        born_date = self.get_argument("born_date")
        sex = self.get_argument("sex")
        mpn = self.get_argument("mpn")

        if not surname or not born_date or not sex or not mpn:
            self.set_status(400)
            self.write("All fields required")
            return

        if sex not in ["M", "F"]:
            self.set_status(400)
            self.write("Sex must be 'M' or 'F'")
            return

        logging.debug("%s %s %s %s", surname, born_date, sex, mpn)

        try:
            new_id = get_id_or_init(self.r, "patient:autoID")
            key = f"patient:{new_id}"

            a = 0
            a += self.r.hset(key, "surname", surname)
            a += self.r.hset(key, "born_date", born_date)
            a += self.r.hset(key, "sex", sex)
            a += self.r.hset(key, "mpn", mpn)

            self.r.incr("patient:autoID")
        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            if a != 4:
                self.set_status(500)
                self.write("Something went terribly wrong")
            else:
                self.write(f"OK: ID {new_id} for {surname}")


class DiagnosisHandler(BaseHandler):
    def get(self):
        items = []
        try:
            last_id = get_id_or_init(self.r, "diagnosis:autoID")
            for i in range(1, last_id):
                result = self.r.hgetall(f"diagnosis:{i}")
                if result:
                    items.append(result)

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.render("templates/diagnosis.html", items=items)

    def post(self):
        patient_ID = self.get_argument("patient_ID")
        diagnosis_type = self.get_argument("type")
        information = self.get_argument("information", default="")

        if not patient_ID or not diagnosis_type:
            self.set_status(400)
            self.write("Patient ID and diagnosis type required")
            return

        logging.debug("%s %s %s", patient_ID, diagnosis_type, information)

        try:
            patient = self.r.hgetall("patient:" + patient_ID)
            if not patient:
                self.set_status(400)
                self.write("No patient with such ID")
                return

            new_id = get_id_or_init(self.r, "diagnosis:autoID")
            key = f"diagnosis:{new_id}"

            a = 0
            a += self.r.hset(key, "patient_ID", patient_ID)
            a += self.r.hset(key, "type", diagnosis_type)
            a += self.r.hset(key, "information", information)

            self.r.incr("diagnosis:autoID")
        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            if a != 3:
                self.set_status(500)
                self.write("Something went terribly wrong")
            else:
                surname = patient.get(b"surname", b"unknown").decode()
                self.write(f"OK: ID {new_id} for patient {surname}")


class DoctorPatientHandler(BaseHandler):
    def get(self):
        items = {}
        try:
            last_id = get_id_or_init(self.r, "doctor:autoID")
            for i in range(1, last_id):
                result = self.r.smembers(f"doctor-patient:{i}")
                if result:
                    items[i] = result

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.render("templates/doctor-patient.html", items=items)

    def post(self):
        doctor_ID = self.get_argument("doctor_ID")
        patient_ID = self.get_argument("patient_ID")

        if not doctor_ID or not patient_ID:
            self.set_status(400)
            self.write("ID required")
            return

        logging.debug("%s %s", doctor_ID, patient_ID)

        try:
            patient = self.r.hgetall("patient:" + patient_ID)
            doctor = self.r.hgetall("doctor:" + doctor_ID)

            if not patient or not doctor:
                self.set_status(400)
                self.write("No such ID for doctor or patient")
                return

            self.r.sadd("doctor-patient:" + doctor_ID, patient_ID)

        except redis.exceptions.ConnectionError:
            self.set_status(503)
            self.write("Redis connection refused")
        else:
            self.write(f"OK: doctor ID: {doctor_ID}, patient ID: {patient_ID}")


def make_app(r=None):
    r = r or get_redis()
    debug = os.environ.get("DEBUG", "1") == "1"

    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/health", HealthHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"}),
            (r"/hospital", HospitalHandler),
            (r"/doctor", DoctorHandler),
            (r"/patient", PatientHandler),
            (r"/diagnosis", DiagnosisHandler),
            (r"/doctor-patient", DoctorPatientHandler),
        ],
        redis=r,
        autoreload=debug,
        debug=debug,
        compiled_template_cache=not debug,
        serve_traceback=debug,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parse_command_line()

    r = get_redis()
    init_db(r)

    app = make_app(r)
    app.listen(PORT)

    logging.info("Listening on %s", PORT)
    tornado.ioloop.IOLoop.current().start()
