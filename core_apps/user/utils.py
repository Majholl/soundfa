import random, string



def generate_code():
    return ''.join(random.choice(string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase) for _ in range(8))