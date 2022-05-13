import string
import random

def generate()->str:
    word_pool = string.ascii_letters+string.digits+string.punctuation
    random.shuffle(word_pool)
    weights = [random.randint(1, 30) for _ in range(len(word_pool))]
    return "".join(random.choices(word_pool, k=15, weights=weights))
