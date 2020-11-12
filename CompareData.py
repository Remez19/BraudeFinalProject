import pandas as pd


def compareData():
    """
       compareData - extract the data from each file (including the data base) and compares between the sites.
       """
    dataBase = []
    resemblance = []
    with open("DataBase_Products.txt", encoding='utf8') as products:
        dataBase = products.read().splitlines()
    df = pd.read_excel('סולטן.xlsx')
    sultanProducts = df['שם'].tolist()
    df = pd.read_excel('משק כישורית.xlsx')
    kishuritProducts = df['שם'].tolist()
    for product1 in sultanProducts:
        resemblance.append(product1)
        try:
            index = dataBase.index(product1.split(' ')[0])
            pairs = []
            for product2 in kishuritProducts:
                # if product2.find(dataBase[index]) != -1:
                percent = copmareByPerecent(product1, product2)
                if percent >= 0.1:
                    pairs.append(product2)
            resemblance.append(pairs)
        except ValueError:
            continue
    print(resemblance)
    return resemblance


def copmareByPerecent(product1, product2):
    """
    :param product1: the first product.
    :param product2: the second product.
    :return percentage: the percentage of the two products resemblance.
    """
    matchPercent = 0
    count = 0
    for A, B in zip(product1, product2):
        if A == B:
            count += 1
        else:
            count -= 1
            break
    matchPercent = float(count / min(len(product1), len(product2)))
    return matchPercent
