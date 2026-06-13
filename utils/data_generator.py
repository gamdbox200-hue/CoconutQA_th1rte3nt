import random
import string
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        SPECIAL_CHARS = "?@#$%^&*_-+()[]{}><\\/|\"'.,:"
        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(SPECIAL_CHARS)

        all_allowed = string.ascii_letters + string.digits + SPECIAL_CHARS

        remaining_length = random.randint(8 - 4, 20 - 4)
        remaining_chars = "".join(random.choices(all_allowed, k=remaining_length))

        password_list = list(upper + lower + digit + special + remaining_chars)
        random.shuffle(password_list)

        return "".join(password_list)

    @staticmethod
    def generate_random_int(length: int) -> str:
        return "".join(random.choices(string.digits, k=length))