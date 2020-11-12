def compareData(dataBaseCon):
    """
       compareData - extract the data from each file (including the data base) and compares between the sites.
       """
    resemblance = []

    kishuritProducts = []
    select_qurey_Kishutrit = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Kishurit'"
    dataBaseCon.execute(select_qurey_Kishutrit)
    for row in dataBaseCon:
        kishuritProducts.append(row.Prod_Name)

    select_query_Sultan = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Sultan'"
    sultanProducts = []
    dataBaseCon.execute(select_query_Sultan)
    for row in dataBaseCon:
        sultanProducts.append(row.Prod_Name)

    AllVegNames_query = "SELECT * FROM [BraudeProject].[dbo].[AllVegNames]"
    allVegNames = []
    dataBaseCon.execute(AllVegNames_query)
    for row in dataBaseCon:
        allVegNames.append(row.Veg_Name)

    pairs = []
    for product1 in sultanProducts:
        resemblance.append(product1)
        try:
            index = allVegNames.index(product1.split(' ')[0])
            for product2 in kishuritProducts:
                if product2.find(allVegNames[index]) != -1:
                    percent = copmareByPerecent(product1, product2)
                    if percent >= 0.2:
                        pairs.append(product2)
            resemblance.append(pairs)
            pairs = []
        except ValueError:
            continue
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
