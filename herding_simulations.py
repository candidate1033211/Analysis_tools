import random
from auxilary import bernouli


def create_herding_sign_series(p, decay, length):
    counter = 1.01
    weights = []
    sign_series = [bernouli(0.5)] #initialising the first sign
    for i in range(1, length):
        weights.append(1-(counter ** decay))
        mother_sign = random.choices(sign_series, weights=weights)[0]
        new_sign = mother_sign * bernouli(p)
        sign_series.append(new_sign)
        counter += 1
    return sign_series
