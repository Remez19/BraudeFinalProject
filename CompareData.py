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

    select_query_Michaeli = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Michaeli'"
    michaeliProducts = []
    dataBaseCon.execute(select_query_Michaeli)
    for row in dataBaseCon:
        michaeliProducts.append(row.Prod_Name)

    AllVegNames_query = "SELECT * FROM [BraudeProject].[dbo].[AllVegNames]"
    allVegNames = []
    dataBaseCon.execute(AllVegNames_query)
    for row in dataBaseCon:
        allVegNames.append(row.Veg_Name)

    delete_query = "DELETE FROM [BraudeProject].[dbo].[UserProdInfo] "
    dataBaseCon.execute(delete_query)
    dataBaseCon.commit()

    maxResemblance = 0
    maxProdKishurit = ""
    maxProdSultan = ""
    maxProdMichaeli = ""

    insert_query_userInfo = 'INSERT INTO UserProdInfo (baseProd,userProdList,siteName)' \
                            'VALUES (?,?,?);'
    for baseProd in allVegNames:
        for prodKishurit in kishuritProducts:
            if baseProd in prodKishurit:
                tempMax = copmareByPerecent(baseProd, prodKishurit)
                if tempMax > maxResemblance:
                    maxResemblance = tempMax
                    maxProdKishurit = prodKishurit
        if maxProdKishurit == "":
            row = (baseProd, "", "Kishurit")
            dataBaseCon.execute(insert_query_userInfo, row)
            dataBaseCon.commit()
        maxResemblance = 0
        tempMax = 0
        for prodSultan in sultanProducts:
            if baseProd in prodSultan:
                tempMax = copmareByPerecent(baseProd, prodSultan)
                if tempMax > maxResemblance:
                    maxResemblance = tempMax
                    maxProdSultan = prodSultan
        if maxProdSultan == "":
            row = (baseProd, "", "Sultan")
            dataBaseCon.execute(insert_query_userInfo, row)
            dataBaseCon.commit()
        maxResemblance = 0
        tempMax = 0
        for prodMichaeli in michaeliProducts:
            if baseProd in prodMichaeli:
                tempMax = copmareByPerecent(baseProd, prodMichaeli)
                if tempMax > maxResemblance:
                    maxResemblance = tempMax
                    maxProdMichaeli = prodMichaeli
        if maxProdMichaeli == "":
            row = (baseProd, "", "Michaeli")
            dataBaseCon.execute(insert_query_userInfo, row)
            dataBaseCon.commit()
        if maxProdKishurit == "" and maxProdSultan == "" and maxProdMichaeli == "":
            continue
        else:
            resemblance.append([maxProdKishurit, maxProdSultan, maxProdMichaeli])
        maxProdKishurit = ""
        maxProdSultan = ""
        maxProdMichaeli = ""
        tempMax = 0
        maxResemblance = 0
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
            break
    matchPercent = float(count / min(len(product1), len(product2)))
    return matchPercent
