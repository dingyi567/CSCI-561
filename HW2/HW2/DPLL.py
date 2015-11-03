import sys
import json

def ResultCheck(item):
    for subitem in item:
        if len(subitem) == 0:
            return True
    return False

def GoalCheck(item):
    if isinstance(item, str):
        return True
    elif item[0] == 'not' and isinstance(item[1], str):
        return True
    else:
        return False

def GoalValue(item):
    if isinstance(item, str):
        return item
    else:
        return item[1]

def Factory(item):
    result = ""
    if isinstance(item, str):
        result = item + "=true"
    else:
        result = item[1] + "=false"
    return result

def Trans(unit):
    if isinstance(unit, str):
        var = ['not']
        var.append(unit)
        return var
    else:
        return unit[1]

def UnitRule(unit, itemList, unitList):
    itemList.remove(unit)
    for item in itemList:
        if item in operatorList:
            continue
        if GoalCheck(item):
            """ and p not p """
            if item == Trans(unit):
                unitList.remove(item)
                itemList.remove(item)
                itemList.append([])
        else:
            if unit in item[1:]:
                itemList.remove(item)
            if Trans(unit) in item[1:]:
                item.remove(Trans(unit))
                """Ex: left 'or A'"""
                if len(item) == 2:
                    subitem = item[1]
                    itemList.remove(item)
                    itemList.append(subitem)
                    if not subitem in unitList:
                        unitList.append(subitem)
                """ only left 'not', after remove """
                if len(item) == 1:
                    item.pop()

def PureRule(pure, itemList):
    for item in itemList:
        for subitem in item[1:]:
            if pure == subitem:
                itemList.remove(item)

def UnitProcessor(unitList, itemList, resultList, symbolList):
    """ get unit """
    for item in itemList:
        if item in operatorList:
            continue
        if GoalCheck(item):
            unitList.append(item)

    """ doing unit rule """
    while unitList:
        unit = unitList.pop()
        resultList.append(Factory(unit))
        UnitRule(unit, itemList, unitList)
        symbol = GoalValue(unit)
        if symbol in symbolList:
            symbolList.remove(symbol)

def pureProcessor(pureList, itemList, resultList, symbolList):
    """ get pure element """
    amountList = []
    for item in itemList:
        if item in operatorList:
            continue
        for subitem in item[1:]:
            if not subitem in amountList:
                amountList.append(subitem)
    for item in amountList:
        if not Trans(item) in amountList:
            pureList.append(item)

    """ doing pure rule """
    while pureList:
        pure = pureList.pop()
        resultList.append(Factory(pure))
        PureRule(pure, itemList)
        symbol = GoalValue(pure)
        if symbol in symbolList:
            symbolList.remove(symbol)

def splitProcessor(unitList, itemList, resultList, symbolList):
    if symbolList:###
        symbol = symbolList.pop()
        splitItemList = itemList
        splitUnitList = unitList
        UnitRule(symbol, splitItemList, splitUnitList)
        resultList.append(Factory(symbol))
        flag = DPLL(splitItemList, resultList, splitUnitList)
        if flag:
            return True
        else:
            symbol = ['not', symbol]
            resultList.pop()
            splitItemList = itemList
            splitUnitList = unitList
            UnitRule(symbol, splitItemList, splitUnitList)
            resultList.append(Factory(symbol))
            flag2 = DPLL(splitItemList, resultList, splitUnitList)
            if flag2:
                return True
            else:
                return False
    else:
        return DPLL(itemList, resultList, symbolList)

def DPLL(itemList, resultList, symbolList):
    if len(itemList) == 0: ###
        return True
    if ResultCheck(itemList):###
        return False

    operator = itemList[0]
    if not operator in operatorList:###
        resultList.append(Factory(operator))####
        return True
    if operator == 'or':
        for item in itemList[1:]:
            resultList.append(Factory(item))
        return True
    if operator == 'not':
        resultList.append(Factory(itemList))###
        return True

    """ deal with and """
    itemList.pop(0)
    """ for unit rule """
    unitList = []
    UnitProcessor(unitList, itemList, resultList, symbolList)
    if ResultCheck(itemList):
        return False

    """ for pure rule """
    pureList = []
    pureProcessor(pureList, itemList, resultList, symbolList)
    if ResultCheck(itemList):
        return False

    """ doing splitting """
    return splitProcessor(unitList, itemList, resultList, symbolList)
    

    
def InitialSymbols(itemList, symbolList):
    for item in itemList:
        if item in operatorList:
            continue
        if GoalCheck(item):
            symbol = GoalValue(item)
            if not symbol in symbolList:
                symbolList.append(symbol)
        else:
            InitialSymbols(item, symbolList) 


def Main(itemList):
    resultList = []
    symbolList = []
    InitialSymbols(itemList, symbolList)
    flag = DPLL(itemList, resultList, symbolList)
    output = []
    if flag:
        output.append('true')
        output += resultList
    else:
        output.append('false')

    return output

operatorList = ['and', 'or', 'not']

""" read the input file """
inputFile = open(sys.argv[2])

""" initial a list to store original data """
sequenceList = list()

""" read the first line, which is the object number """
linenum = inputFile.readline()

""" use buildin method eval to get data as array, then append it in list """
for line in inputFile:
    sequenceList.append(eval(line))

inputFile.close()

with open('CNF_satisfiability.txt', 'w') as out_file:

    for item in sequenceList:
        result = Main(item)
        json.dump(result, out_file)
        out_file.write('\n')
        print result
        
out_file.close()