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
        # Разрешённые спецсимволы согласно спецификации API
        SPECIAL_CHARS = "~!?@#$%^&*_-+()[]{}><\\/|\"'.,:"

        # Гарантированные символы (по одному каждого типа)
        upper = random.choice(string.ascii_uppercase)   # заглавная латиница
        lower = random.choice(string.ascii_lowercase)   # строчная латиница
        digit = random.choice(string.digits)            # цифра
        special = random.choice(SPECIAL_CHARS)          # спецсимвол

        # Все допустимые символы для остальной части пароля
        all_allowed = string.ascii_letters + string.digits + SPECIAL_CHARS

        # Длина пароля от 8 до 32 символов (после добавления гарантированных)
        remaining_length = random.randint(8 - 4, 32 - 4)  # минимум 4 уже есть
        remaining_chars = "".join(random.choices(all_allowed, k=remaining_length))

        # Собираем и перемешиваем
        password_list = list(upper + lower + digit + special + remaining_chars)
        random.shuffle(password_list)

        return "".join(password_list)