from ScrapePage import scrapePageSultan, scrapePageMichaeli, scrapePageKishurit



# Link to 'משק כישורית' site.
def importData(dataBaseCon):
    # Delete all the data from tables in order to update them
    delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Sultan'"
    dataBaseCon.execute(delete_query)
    dataBaseCon.commit()
    delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Kishurit'"
    dataBaseCon.execute(delete_query)
    dataBaseCon.commit()
    delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Michaeli'"
    dataBaseCon.execute(delete_query)
    dataBaseCon.commit()
    delete_query = "DELETE FROM [BraudeProject].[dbo].[AllVeg] WHERE Prod_Web = 'Michaeli'"


    # Define insert query
    insert_query = 'INSERT INTO AllProds (Prod_Name,Prod_Unit,Prod_Price,Prod_Web)' \
                   'VALUES (?,?,?,?);'

    KishuritLink = 'http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page='
    SultanLink = 'http://sultan.pricecall.co.il/'
    MichaeliLink = 'https://michaelio.co.il/c/%D7%99%D7%A8%D7%A7%D7%95%D7%AA'
    pageCount = 3  # The number of pages in "משק כישורית" webpage.

    Vegetables = []  # All the vegetables from "משק כישורית" webpage and "סולטן" webpage.
    Data = []  # One list of all the vegetables
    for pageIndex in range(1, pageCount + 1):
        Vegetables.append(scrapePageKishurit(pageIndex, KishuritLink))

    # falttern the data to single list
    Data = [item for sublist in Vegetables for item in sublist]
    row = ()
    for prod in Data:
        row = (prod.vegName, prod.vegUnit, int(float(prod.vegPrice)), "Kishurit")
        dataBaseCon.execute(insert_query, row)
        dataBaseCon.commit()

    # # convert the data to a table
    # df = pd.DataFrame.from_records([d.to_dist() for d in Data])
    # # create a cvs file out of the table
    # df.to_csv('משק כישורית.csv', index=False, encoding='utf-8')
    # df = pd.read_csv("משק כישורית.csv")
    # temp = pd.ExcelWriter('משק כישורית.xlsx')
    # # create a excel flie from cvs
    # df.to_excel(temp, index=False)
    # temp.save()
    # os.remove("משק כישורית.csv")

    Data = scrapePageSultan(SultanLink)
    row = ()
    for prod in Data:
        row = (prod.vegName, prod.vegUnit, int(float(prod.vegPrice)), "Sultan")
        dataBaseCon.execute(insert_query, row)
        dataBaseCon.commit()
    # # Create a excel file for sultan site too
    # df = pd.DataFrame.from_records([v.to_dist() for v in Vegetables])
    # df.to_csv('סולטן.csv', index=False, encoding='utf-8')
    # df = pd.read_csv('סולטן.csv')
    # temp = pd.ExcelWriter('סולטן.xlsx')
    # df.to_excel(temp, index=False)
    # temp.save()
    # os.remove("סולטן.csv")

    Data = scrapePageMichaeli(MichaeliLink)
    row = ()
    for prod in Data:
        row = (prod.vegName, prod.vegUnit, int(float(prod.vegPrice)), "Michaeli")
        dataBaseCon.execute(insert_query, row)
        dataBaseCon.commit()
    # for prod in Data:
    #     row = (prod.vegName, prod.vegUnit, int(float(prod.vegPrice)), "Michaeli")
    #     dataBaseCon.execute(insert_query, row)
    #     dataBaseCon.commit()
