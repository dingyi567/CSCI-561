import sys
import json

def IsEqual(key1, key2):
	temp1 = sorted(key1[1:])
	temp2 = sorted(key2[1:])
	del key1[1:]
	del key2[1:]
	key1 += temp1
	key2 += temp2

	if key1 == key2:
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


def TransToNot(key):
	var = ['not']
	var.append(key)
	return var


def IsGoal(key):
    if isinstance(key, str):
        return True
    theOperator = key[0]
    if theOperator == 'not' and isinstance(key[1], str):
        return True
    else:
        return False

def ProduceResult(subresults, results):
	if not IsGoal(subresults):
		temp = sorted(subresults[1:])
		del subresults[1:]
		subresults += temp
	if subresults in results:
		if len(results) == 2:
			del results[:]
			results += subresults
		return results

	else:
		if IsGoal(subresults):
			results.append(subresults)
			return results
		outProcessor = results[0]
		inProcessor = subresults[0]
		if outProcessor == inProcessor:
			for i in subresults[1:]:
				if not i in results:
					results.append(i)
		else:
			results.append(subresults)

def BiconditionalConvert(key1, key2):
	results = ['implies']
	results.append(key1)
	results.append(key2)
	return results

def NotImpliesFormula(key):
	results = ['or']
	subresults1 = CNFconverter(TransToNot(key[1]))
	subresults2 = CNFconverter(key[2])
	ProduceResult(subresults1, results)
	ProduceResult(subresults2, results)
	return results

def NotBiconditionalFormula(key):
	results = ['and']
	subkey1 = BiconditionalConvert(key[1], key[2])
	subkey2 = BiconditionalConvert(key[2], key[1])
	subresults1 = NotImpliesFormula(subkey1)
	subresults2 = NotImpliesFormula(subkey2)
	Produceresult(subresults1, results)
	Produceresult(subresults2, results)
	return results

def CompondAndCompond(subkey1, subkey2):
	results = []
	if IsEqual(subkey1, subkey2):
		results = subkey1
		return results

	if subkey1[0] == 'and' and subkey2[0] == 'and':
		results.append('and')
		for _key2 in subkey2[1:]:
			for _key1 in subkey1[1:]:
				if _key1 == _key2:
					ProduceResult(_key1, results)
				else:
					tempresult = ['or']
					ProduceResult(_key2, tempresult)
					ProduceResult(_key1, tempresult)
					ProduceResult(tempresult, results)
		return results

	if subkey1[0] == 'or' and subkey2[0] == 'or':
		results.append('or')
		for _key in subkey1:
			ProduceResult(_key, results)
		for _key in subkey2:
			ProduceResult(_key, results)
		return results

	if subkey2[0] == 'or' and subkey1[0] == 'and':
		results.append('and')
		for _key in subkey1[1:]:
			tempresult = list(subkey2)
			ProduceResult(_key, tempresult)
			ProduceResult(tempresult, results)
		return results

	if subkey1[0] == 'or' and subkey2[0] == 'and':
		results.append('and')
		for _key in subkey2[1:]:
			tempresult = list(subkey1)
			ProduceResult(_key, tempresult)
			ProduceResult(tempresult, results)
		return results

def UnitAndCompond2(subkey1, subkey2):
	results = []
	if subkey2[0] == 'or':
		results.append('or')
		ProduceResult(subkey1, results)
		ProduceResult(subkey2, results)
		return results

        if subkey2[0] == 'and':
		results.append('and')
	        for _key in subkey2[1:]:
			if subkey1 == _key:
				ProduceResult( _key, results)
			else:
				tempresult = ['or']
				ProduceResult(subkey1, tempresult)
				ProduceResult( _key, tempresult)
				ProduceResult(tempresult, results)
		return results

def UnitAndCompond1(subkey1, subkey2):
	results = []
	if subkey1[0] == 'or':
		results.append('or')
		ProduceResult(subkey2, results)
		ProduceResult(subkey1, results)
		return results
	if subkey1[0] == 'and':
		results.append('and')
		for _key in subkey1[1:]:
			if subkey2 == _key:
				ProduceResult( _key, results)
			else:
				tempresult = ['or']
				ProduceResult(subkey2, tempresult)
				ProduceResult( _key, tempresult)
				ProduceResult(tempresult, results)
		return results

def UnitAndUnit(subkey1, subkey2):
	results = []
	results.append('or')
	ProduceResult(subkey1, results)
	ProduceResult(subkey2, results)
	return results

def OrFormula(key):
	if len(key) == 3:
		subkey1 = CNFconverter(key[1])
		subkey2 = CNFconverter(key[2])

		if IsGoal(subkey1) and IsGoal(subkey2):
			return UnitAndUnit(subkey1, subkey2)
			
		elif IsGoal(subkey2):
			return UnitAndCompond1(subkey1, subkey2)
			

		elif IsGoal(subkey1):
			return UnitAndCompond2(subkey1, subkey2)

		else:
			return CompondAndCompond(subkey1, subkey2)

	else:
		# more than 2 keys
		temporary = list(key)
		firstkey = CNFconverter(temporary.pop(1))
		temporaryResult = OrFormula(temporary)
		newtemporary = ['or']
		newtemporary.append(temporaryResult)
		newtemporary.append(firstkey)
		return CNFconverter(newtemporary)

def NotFormula(key):
	results = []
	theOperator = key[0]

	if theOperator == 'not':
		return key[1]

	elif theOperator == 'and':
		results.append('or')
		for subkey in key[1:]:
			ProduceResult(CNFconverter(TransToNot(subkey)), results)
		return results

	elif theOperator == 'or':
		results.append('and')
		for subkey in key[1:]:
			ProduceResult(CNFconverter(TransToNot(subkey)), results)
		return results

	elif theOperator == 'iff':
		results = NotFormula(NotBiconditionalFormula(key))
		return results

	elif theOperator == 'implies':
		results = NotFormula(NotImpliesFormula(key))
		return results



def CNFconverter(key):
	if IsGoal(key):
		return key

	results = []
	theOperator = key[0]

	if theOperator == 'not':
		tempResult = NotFormula(key[1])
		results = CNFconverter(tempResult)
		return results

	elif theOperator == 'or':
		results = OrFormula(key)
		return results

	elif theOperator == 'and':
		results = ['and']
		for subkey in key[1:]:
			subresult = CNFconverter(subkey)
			ProduceResult(subresult, results)
		""" to avoid ['and', 'A']"""
		if len(results) == 2:####???????
			results.pop(0)
		return results

	elif theOperator == 'iff':
		results = ['and']
		subkey1 = BiconditionalConvert(key[1], key[2])
		subkey2 = BiconditionalConvert(key[2], key[1])
		subresult1 = CNFconverter(subkey1)
		subresult2 = CNFconverter(subkey2)
		ProduceResult(subresult1, results)
		ProduceResult(subresult2, results)
		return results


	elif theOperator == 'implies':
		results = ['or']
		subresult1 = CNFconverter(TransToNot(key[1]))
		subresult2 = CNFconverter(key[2])
		ProduceResult(subresult1, results)
		ProduceResult(subresult2, results)
		if subresult1[0] == "and" or subresult2[0] == "and":
			return CNFconverter(results)
		else:
			return results
	

inputFile = open(sys.argv[2], 'r')
outputFile = open('sentences_CNF1.txt', 'w')

linenum = inputFile.readline()

for line in inputFile:
	result = CNFconverter(eval(line))
	json.dump(result, outputFile)
	outputFile.write('\n')
	print result
inputFile.close()	
outputFile.close()