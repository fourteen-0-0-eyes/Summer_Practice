def get_сoins_from_sum(sum: int, coinsWorth: list=None):
    if(coinsWorth == None):
        coinsWorth = [1, 5, 10, 25, 100]

    coinsWorth = list(set(coinsWorth))
    coinsWorth.sort(reverse=True)
    coins = []
    while (sum >= coinsWorth[-1]):
        for coin in coinsWorth:
            if(sum >= coin):
                sum -= coin
                coins.append(coin)
                break

    return coins


def main():
    print(get_сoins_from_sum(101))


if __name__ == "__main__":
    main()
