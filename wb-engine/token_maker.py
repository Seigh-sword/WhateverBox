import random
import datetime
import string

class TokenMaker:
    @staticmethod
    def generate_private():
        rand_digits = random.randint(10, 99)
        current_time = datetime.datetime.now().strftime("%H%M%S")
        return f"wb-{rand_digits}-{current_time}.0tg7="

    @staticmethod
    def generate_public():
        chars = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(chars) for _ in range(32))
        return random_str
