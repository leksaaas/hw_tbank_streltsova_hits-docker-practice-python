from locust import HttpUser, task, between


class HospitalUser(HttpUser):
    wait_time = between(0.1, 0.5)

    # Самое стабильное — healthcheck (не зависит от шаблонов)
    @task(10)
    def health(self):
        self.client.get("/health")

    # Просмотр страниц
    @task(3)
    def browse(self):
        self.client.get("/")
        self.client.get("/hospital")
        self.client.get("/doctor")
        self.client.get("/patient")
        self.client.get("/diagnosis")
        self.client.get("/doctor-patient")

    # Создание записей (POST формы как в твоих HTML)
    @task(2)
    def create_hospital(self):
        self.client.post("/hospital", data={
            "name": "LoadHospital",
            "address": "LoadStreet",
            "beds_number": "10",
            "phone": "123"
        })

    @task(2)
    def create_patient(self):
        self.client.post("/patient", data={
            "surname": "LoadPatient",
            "born_date": "2001-01-01",
            "sex": "M",
            "mpn": "9999"
        })
