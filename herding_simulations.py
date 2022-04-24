import random
from auxilary import bernouli


def create_herding_sign_series(p, gamma, length):
    counter = 1.01
    weights = []
    sign_series = [bernouli(0.5)] #initialising the first sign
    for i in range(1, length):
        weights.append(1-(counter ** gamma))
        mother_sign = random.choices(sign_series, weights=weights)[0]
        new_sign = mother_sign * bernouli(p)
        sign_series.append(new_sign)
        counter += 1
    return sign_series