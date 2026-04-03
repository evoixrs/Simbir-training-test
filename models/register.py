from faker import Faker
fake = Faker()

class RegisterModel:
    def random(self):
        username = fake.user_name()
        return {"name": fake.first_name(), "password": fake.password(), "email": f"{username}@example.com"}