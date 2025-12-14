import fakeredis
from tornado.testing import AsyncHTTPTestCase
import main


class TestHandlers(AsyncHTTPTestCase):
    def get_app(self):
        self.redis = fakeredis.FakeStrictRedis()
        main.init_db(self.redis)
        return main.make_app(self.redis)

    def test_health_ok(self):
        r = self.fetch("/health")
        assert r.code == 200
        assert r.body == b"OK"

    def test_root_ok(self):
        r = self.fetch("/")
        assert r.code == 200
        assert b"Welcome to the hospital" in r.body

    def test_hospital_validation(self):
        r = self.fetch("/hospital", method="POST", body="name=&address=")
        assert r.code == 400
        assert b"Hospital name and address required" in r.body

    def test_hospital_create_ok(self):
        body = "name=City&address=Main&beds_number=10&phone=123"
        r = self.fetch("/hospital", method="POST", body=body)
        assert r.code == 200
        assert b"OK: ID" in r.body

    def test_doctor_rejects_unknown_hospital_id(self):
        body = "surname=Ivanov&profession=Surgeon&hospital_ID=999"
        r = self.fetch("/doctor", method="POST", body=body)
        assert r.code == 400
        assert b"No hospital with such ID" in r.body

    def test_patient_sex_validation(self):
        body = "surname=Petrov&born_date=2000-01-01&sex=X&mpn=111"
        r = self.fetch("/patient", method="POST", body=body)
        assert r.code == 400
        assert b"Sex must be 'M' or 'F'" in r.body

    def test_diagnosis_requires_existing_patient(self):
        body = "patient_ID=999&type=flu&information=test"
        r = self.fetch("/diagnosis", method="POST", body=body)
        assert r.code == 400
        assert b"No patient with such ID" in r.body
