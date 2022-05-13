import string
import random

def generate()->str:
    word_pool = [x for x in string.ascii_letters+string.digits+string.punctuation]
    for _ in range(10):
        random.shuffle(word_pool)
    weights = [random.randint(1, 30) for _ in range(len(word_pool))]
    return "".join(random.choices(word_pool, k=15, weights=weights))
if __name__=='__main__':
    print(generate())