import sys
import json


# [{'basicName': 'תפוח', 'quantity': 2, 'realName': 'item_id_2112537', 'link': None, 'cost': '8'}
class Vegetable:
    def __init__(self, siteName, basicName, quantity, realName, link, cost):
        self.siteName = siteName
        self.basicName = basicName
        self.quantity = quantity
        self.realName = realName
        self.link = link
        self.cost = cost

    # {'basicName': 'תפוח', 'quantity': 2, 'realName': 'item_id_2112537', 'link': None, 'cost': '8'}
    def getVegDic(self):
        return {
            'supplierName': self.siteName,
            'basicName': self.basicName,
            'quantity': self.quantity,
            'realName': self.realName,
            'link': self.link,
        }

    def getVegDetails(self):
        return f'Site: {self.siteName}\n' \
               f'Basic Name: {self.basicName}\n' \
               f'Quantity: {self.quantity}\n' \
               f'Cost: {self.cost}\n' \
               f'Real Name: {self.realName}\n' \
               f'Link: {self.link}\n' \
               f'\n'


def createVegList(data=sys.argv[1]):  # =sys.argv[1]):
    try:
        jsonList = json.loads(data)
        # Debug
        # jsonList = data
        kishuritDic = jsonList["purchaseList"]["prodsKishurit"]
        sultanDic = jsonList["purchaseList"]["prodsSultan"]
        dovDic = jsonList["purchaseList"]["prodsDov"]
        kishuritVegs = []
        sultanVegs = []
        dovVegs = []
        for prod in kishuritDic:
            kishuritVegs.append(
                Vegetable("Kishurit", prod["basicName"], prod["quantity"], prod["realName"], prod["link"],
                          prod["cost"]))
        for prod in sultanDic:
            sultanVegs.append(
                Vegetable("Sultan", prod["basicName"], prod["quantity"], prod["realName"], prod["link"], prod["cost"]))
        for prod in dovDic:
            dovVegs.append(
                Vegetable("Dov", prod["basicName"], prod["quantity"], prod["realName"], prod["link"], prod["cost"]))
        with open("Stam1.txt", "w") as file:
            for item in kishuritVegs:
                file.write(item.getVegDetails())
            for item in sultanVegs:
                file.write(item.getVegDetails())
            for item in dovVegs:
                file.write(item.getVegDetails())
            file.write("----------------------------------")
        return kishuritVegs, sultanVegs, dovVegs
    except Exception as e:
        print("createVegList" + str(e))
        exit(0)


def compareLists(List1, List2):
    try:
        resultList = []
        totalListPrice = 0
        for veg1 in List1:
            tempVeg = None
            for veg2 in List2:
                if veg1.basicName == veg2.basicName:
                    if float(veg1.cost) <= float(veg2.cost):
                        tempVeg = veg1
                    else:
                        tempVeg = veg2
                    break
            if tempVeg:
                totalListPrice = totalListPrice + float(tempVeg.cost) * float(tempVeg.quantity)
                resultList.append(tempVeg)
            else:
                totalListPrice = totalListPrice + float(veg1.cost) * float(veg1.quantity)
                resultList.append(veg1)

        for veg2 in List2:
            tempVeg = 0
            for resVeg in resultList:
                if veg2.basicName == resVeg.basicName:
                    tempVeg = 1
                    break
            if tempVeg == 0:
                totalListPrice = totalListPrice + float(veg2.cost) * float(veg2.quantity)
                resultList.append(veg2)

        return resultList, totalListPrice
    except Exception as e:
        print("compareLists" + str(e))
        exit(0)


def findSeperation(kishurit, sultan, dov):
    try:
        kishuritSultan = []
        kishuritDov = []
        sultanDov = []
        resultList = []

        # Kishurit - Sultan
        kishuritSultan, kishuritSultanTotal = compareLists(kishurit, sultan)
        # Kishurit - Sultan

        # Kishurit - Dov
        kishuritDov, kishuritDovTotal = compareLists(kishurit, dov)
        # Kishurit - Dov

        # Sultan - Dov
        sultanDov, sultanDovTotal = compareLists(sultan, dov)
        # Sultan - Dov
        # maxLengthList = max(len(kishuritSultan), len(kishuritDov), len(sultanDov))
        if kishuritSultanTotal <= kishuritDovTotal and kishuritSultanTotal <= sultanDovTotal and len(kishuritSultan):
            resultList = kishuritSultan
            return resultList, kishuritSultanTotal, "K-S"
        if kishuritDovTotal <= kishuritSultanTotal and kishuritDovTotal <= sultanDovTotal and len(kishuritDov):
            resultList = kishuritDov
            return resultList, kishuritDovTotal, "K-D"
        if sultanDovTotal <= kishuritSultanTotal and sultanDovTotal <= kishuritDovTotal and len(sultanDov):
            resultList = sultanDov
            return resultList, sultanDovTotal, "S-D"
    except Exception as e:
        print("findSeperation" + str(e))
        exit(0)


def checkMiss(resList, checkList):
    for veg in checkList:
        flag = 0
        for resVeg in resList:
            if veg.basicName == resVeg.basicName:
                flag = 1
        if flag == 0:
            return 0
    return 1


if __name__ == '__main__':
    try:
        # with open("temp.txt", "w") as file:
        #     file.write(str(json.loads(sys.argv[1])))
        # data = {'purchaseList': {'userId': 0, 'products': [{'basicName': 'שמיר', 'quantity': 1}, {'basicName': 'תפוח', 'quantity': 1}, {'basicName': 'קייל', 'quantity': 1}, {'basicName': 'קולורבי', 'quantity': 1}], 'prodsKishurit': [{'basicName': 'תפוח', 'quantity': 1, 'realName': 'item_id_2112537', 'link': None, 'cost': '8'}, {'basicName': 'קולורבי', 'quantity': 1, 'realName': 'item_id_837044', 'link': None, 'cost': '6'}], 'missKishurit': [{'basicName': 'שמיר', 'quantity': 1}, {'basicName': 'קייל', 'quantity': 1}], 'prodsSultan': [{'basicName': 'שמיר', 'quantity': 1, 'realName': '54', 'link': None, 'cost': '4'}, {'basicName': 'תפוח', 'quantity': 1, 'realName': '76', 'link': None, 'cost': '5'}, {'basicName': 'קייל', 'quantity': 1, 'realName': '338', 'link': None, 'cost': '8'}], 'missSultan': [{'basicName': 'קולורבי', 'quantity': 1}], 'prodsDov': [{'basicName': 'שמיר', 'quantity': 1, 'realName': 'edit-submit--29', 'link': 'https://dovdov.co.il/products/category/yrq-wsby-tybwl-71', 'cost': '5.9'}, {'basicName': 'תפוח', 'quantity': 1, 'realName': 'edit-submit--41', 'link': 'https://dovdov.co.il/products/category/yrqwt-32', 'cost': '4.9'}, {'basicName': 'קייל', 'quantity': 1, 'realName': 'edit-submit--27', 'link': 'https://dovdov.co.il/products/category/yrq-wsby-tybwl-71', 'cost': '12.9'}, {'basicName': 'קולורבי', 'quantity': 1, 'realName': 'edit-submit--36', 'link': 'https://dovdov.co.il/products/category/yrqwt-32', 'cost': '8.9'}], 'missDov': []}}
        kishuritVegs, sultanVegs, dovVegs = createVegList()
        resList, totalSum, supplierName = findSeperation(kishuritVegs, sultanVegs, dovVegs)
        if supplierName == 'K-S':
            res = checkMiss(resList, dovVegs)
        if supplierName == 'K-D':
            res = checkMiss(resList, sultanVegs)
        if supplierName == "S-D":
            res = checkMiss(resList, kishuritVegs)
        if res:
            finalList = []
            for veg in resList:
                finalList.append(veg.getVegDic())
            print(finalList)
        else:
            print(0)
    except Exception as e:
        print(e)
    sys.stdout.flush()
