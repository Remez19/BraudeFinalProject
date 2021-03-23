def compareNameToBaseName(name, baseNameList):
    """
       : finds the 'base' name that closest to name
       :param name: the original name of the veg.
       :param baseNameList: the 'base' name of a veg.
       :return bestBaseMatch: the name of the closest 'base' name.
       """
    maxPrecent = 0
    bestBaseMatch = ""
    for baseName in baseNameList:
        precent = copmareByPerecent(name, baseName)
        if maxPrecent <= precent:
            maxPrecent = precent
            bestBaseMatch = baseName
    return bestBaseMatch


def copmareByPerecent(name, baseName):
    """
    : compare two veg names according to continues characters
    :param name: the original name of the veg.
    :param baseName: the 'base' name of a veg.
    :return matchPercent: the percentage of the two products resemblance.
    """
    matchPercent = 0
    count = 0
    for A, B in zip(baseName, name):
        if A == B:
            count += 1
        else:
            break
    matchPercent = float(count / min(len(name), len(baseName)))
    return matchPercent
