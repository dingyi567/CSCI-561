import sys
import json

def GetValue(key):
    if isinstance(key, str):
        return key
    else:
        return key[1]

def IsResult(key):
    for subkey in key:
        if len(subkey) == 0:
            return False
    return True

def ResultProcess(key): #supposing key is str or not str, factory
    result = ""
    if isinstance(key, str):
        result = key + "=true"
    else:
        result = key[1] + "=false"
    return result

def IsGoal(key):
    if isinstance(key, str):
        return True
    elif key[0] == 'not' and isinstance(key[1], str):
        return True
    else:
        return False


def TransItem(key):
    if isinstance(key, str):
        var = ['not']
        var.append(key)
        return var
    else:
        return key[1]

def UnitClauseRule(theUnit, itemList, unitList):
    for item in itemList[:]:
        if item in operatorsList:
            continue
        if IsGoal(item):
            """ and p not p """
            if item == TransItem(theUnit):
                unitList.remove(item)
                itemList.remove(item)
                itemList.append([])
        else:
            if theUnit in item[1:]:
                itemList.remove(item)
            if TransItem(theUnit) in item[1:]:
                item.remove(TransItem(theUnit))
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

def DoingUnitRule(unitClauseList, key, symbolList, resultList):
    while unitClauseList:
        unit = unitClauseList.pop()
        resultList.append(ResultProcess(unit))
        key.remove(unit)
        UnitClauseRule(unit, key, unitClauseList)
        symbol = GetValue(unit)
        if symbol in symbolList:
            symbolList.remove(symbol)

def FindUnitClause(unitClauseList, key, symbolList, resultList):
    """ get unit """
    for _item in key:
        if _item in operatorsList:
            continue
        if IsGoal(_item):
            unitClauseList.append(_item)

    """ doing unit rule """
    DoingUnitRule(unitClauseList, key, symbolList, resultList)
    

def DoingPureRule(pureList, key, symbolList, resultList):
    while pureList:
        pure = pureList.pop()
        resultList.append(ResultProcess(pure))
        for item in key:
           for subitem in item[1:]:
               if pure == subitem:
                   key.remove(item)
        symbol = GetValue(pure)
        if symbol in symbolList:
            symbolList.remove(symbol)

def FindPureSymbols(pureList, key, symbolList, resultList):
    """ get pure element """
    amountList = []
    for item in key:
        if item in operatorsList:
            continue
        for subitem in item[1:]:
            if not subitem in amountList:
                amountList.append(subitem)
    for item in amountList:
        if not TransItem(item) in amountList:
            pureList.append(item)

    """ doing pure rule """
    DoingPureRule(pureList, key, symbolList, resultList)
    

def Split(unitList, key, resultList, symbolList):
    if symbolList:###
        symbol = symbolList.pop()
        splitItemList = key
        splitUnitList = unitList
        UnitClauseRule(symbol, splitItemList, splitUnitList)
        resultList.append(ResultProcess(symbol))
        flag = addDealing(splitItemList, symbolList, resultList)
        if flag:
            return True
        else:
            symbol = ['not', symbol]
            resultList.pop()
            splitItemList = key
            splitUnitList = unitList
            UnitClauseRule(symbol, splitItemList, splitUnitList)
            resultList.append(ResultProcess(symbol))
            flag2 = addDealing(splitItemList, symbolList, resultList)
            if flag2:
                return True
            else:
                return False
    else:
        return DPLLprocess(key, symbolList, resultList)

def addDealing(key, symbolList, resultList):
    #unit clause rule
    UnitClauseList = []
    FindUnitClause(UnitClauseList, key, symbolList, resultList)
    if not IsResult(key):
        return False

    #pure symbol rule
    PureSymbolsList = []
    FindPureSymbols(PureSymbolsList, key, symbolList, resultList)
    if not IsResult(key):
        return False

    #the splitting rule
    return Split(UnitClauseList, key, resultList, symbolList)

def DPLLprocess(item, symbolList, resultList):
    if len(item) == 0: ###
        return True
    if not IsResult(item):###
        return False
    
    key = item[0] #operator --> key
    if key not in operatorsList:###????????
        resultList.append(ResultProcess(key))####?????
        return True
    #begin with 'not'
    if key == 'not':
        resultList.append(ResultProcess(item))###
        return True
    #begin with 'or'
    if key == 'or':
        for _item in item[1:]:
            resultList.append(ResultProcess(_item))
        return True

    #else begin with 'and'
    item.pop(0)

    return addDealing(item, symbolList, resultList)
    
    

    
def SymbolInitialize(symbolList, key):
    for _item in key:
        if _item in operatorsList:
            continue
        if IsGoal(_item):
            symbol = GetValue(_item)
            if symbol not in symbolList:
                symbolList.append(symbol)
        else:
            SymbolInitialize(symbolList, _item) 


def DPLL(key):
    resultList = []
    symbolList = []
    results = []
    SymbolInitialize(symbolList, key)
    flag = DPLLprocess(key, symbolList, resultList)
    if flag:
        results.append('true')
        results += resultList
    else:
        results.append('false')

    return results



operatorsList = ['not', 'and', 'or' ]


inputFile = open(sys.argv[2], 'r')
outputFile = open('CNF_satisfiability.txt', 'w')

linenum = inputFile.readline()

for line in inputFile:
    result = DPLL(eval(line))
    json.dump(result, outputFile)
    outputFile.write('\n') 
    print result 
outputFile.close()
inputFile.close()