import sys
import json

def TransNot(item):
	result = ['not']
	result.append(item)
	return result

def TransItem(item):
	if isinstance(item, str):
		result = ['not']
		result.append(item)
		return result
	else:
		return item[1]

def EqualCheck(item1, item2):
	temp1 = sorted(item1[1:])
	del item1[1:]
	item1 += temp1

	temp2 = sorted(item2[1:])
	del item2[1:]
	item2 += temp2

	if item1 == item2:
		return True
	else:
		return False

def GoalCheck(item):
    if isinstance(item, str):
        return True
    operator = item[0]
    if operator == 'not' and isinstance(item[1], str):
        return True
    else:
        return False

def Combine(result, subresult):
	if not GoalCheck(subresult):
		temp = sorted(subresult[1:])
		del subresult[1:]
		subresult += temp
	if subresult in result:
		return result
	# elif TransItem(subresult) in result:
	# 	result[:] = []
	# 	return result
	else:
		if GoalCheck(subresult):
			result.append(subresult)
			return result
		""" deal with the condition that outer and inner have duplicate and, or """
		outProcessor = result[0]
		inProcessor = subresult[0]
		if outProcessor == inProcessor:
			for i in subresult[1:]:
				if not i in result:
					result.append(i)
		else:
			result.append(subresult)

def BioProcessor(item1, item2):
	result = ['implies']
	result.append(item1)
	result.append(item2)
	return result

def BioElimination(item):
	result = ['and']
	subitem1 = BioProcessor(item[1], item[2])
	subitem2 = BioProcessor(item[2], item[1])
	subresult1 = CNF(subitem1)
	subresult2 = CNF(subitem2)
	Combine(result, subresult1)
	Combine(result, subresult2)
	return result

def ImpElimination(item):
	result = ['or']
	subresult1 = CNF(TransNot(item[1]))
	subresult2 = CNF(item[2])
	Combine(result, subresult1)
	Combine(result, subresult2)
	if subresult1[0] == "and" or subresult2[0] == "and":
		return CNF(result)
	else:
		return result

def NotImpElimination(item):
	result = ['or']
	subresult1 = CNF(TransNot(item[1]))
	subresult2 = CNF(item[2])
	Combine(result, subresult1)
	Combine(result, subresult2)
	return result

def NotBioElimination(item):
	result = ['and']
	subitem1 = BioProcessor(item[1], item[2])
	subitem2 = BioProcessor(item[2], item[1])
	subresult1 = NotImpElimination(subitem1)
	subresult2 = NotImpElimination(subitem2)
	Combine(result, subresult1)
	Combine(result, subresult2)
	return result

def AndProcessor(item):
	result=['and']
	for subitem in item[1:]:
		subresult = CNF(subitem)
		Combine(result, subresult)
	""" to avoid ['and', 'A']"""
	if len(result) == 2:
		result.pop(0)
	return result


def Dis1(unit, several, result):
	for item in several[1:]:
		""" a V (a ^ b) """
		if unit == item:
			Combine(result, item)
		else:
			temp = ['or']
			Combine(temp, unit)
			Combine(temp, item)
			Combine(result, temp)

def Dis2(units, several, result):
	for item in several[1:]:
		temp = list(units)
		Combine(temp, item)
		Combine(result, temp)

def Dis3(item1, item2, result):
	for subitem2 in item2[1:]:
		for subitem1 in item1[1:]:
			if subitem1 == subitem2:
				Combine(result, subitem1)
			else:
				temp = ['or']
				Combine(temp, subitem2)
				Combine(temp, subitem1)
				Combine(result, temp)


def OrProcessor(item):
	result = []
	if len(item) == 3:
		subitem1 = CNF(item[1])
		subitem2 = CNF(item[2])
		""" a V b """
		if GoalCheck(subitem1) and GoalCheck(subitem2):
			result.append('or')
			Combine(result, subitem1)
			Combine(result, subitem2)
			return result
		elif GoalCheck(subitem1):
			""" a V (b V c)"""
			if subitem2[0] == 'or':
				result.append('or')
				Combine(result, subitem1)
				Combine(result, subitem2)
				return result
			""" a V (b ^ c) """
			if subitem2[0] == 'and':
				result.append('and')
				Dis1(subitem1, subitem2, result)
				return result
		elif GoalCheck(subitem2):
			""" (a V b) V c """
			if subitem1[0] == 'or':
				result.append('or')
				Combine(result, subitem2)
				Combine(result, subitem1)
				return result
			""" (a ^ b) V c """
			if subitem1[0] == 'and':
				result.append('and')
				Dis1(subitem2, subitem1, result)
				return result
		else:
			if EqualCheck(subitem1, subitem2):
				result = subitem1
				return result
			""" (a V b) V (c V d) """
			if subitem1[0] == 'or' and subitem2[0] == 'or':
				result.append('or')
				for temp in subitem1:
					Combine(result, temp)
				for temp in subitem2:
					Combine(result, temp)
				return result
			""" (a V b) V (c ^ d) """
			if subitem1[0] == 'or' and subitem2[0] == 'and':
				result.append('and')
				Dis2(subitem1, subitem2, result)
				return result
			""" (a ^ b) V (c V d) """
			if subitem2[0] == 'or' and subitem1[0] == 'and':
				result.append('and')
				Dis2(subitem2, subitem1, result)
				return result
			""" (a ^ b) V (c ^ d) """
			if subitem1[0] == 'and' and subitem2[0] == 'and':
				result.append('and')
				Dis3(subitem1, subitem2, result)
				return result
	else:
		""" deal with multi items, first separate it into two group,
		and solve them recursively """
		temp = list(item)
		firstitem = CNF(temp.pop(1))
		tempResult = OrProcessor(temp)
		newtemp = ['or']
		newtemp.append(tempResult)
		newtemp.append(firstitem)
		return CNF(newtemp)

def NotProcessor(item):
	result = []
	operator = item[0]

	""" double negation elimination """
	if operator == 'not':
		return item[1]

	""" De Morgan of and """
	if operator == 'and':
		result.append('or')
		for subitem in item[1:]:
			Combine(result, CNF(TransNot(subitem)))
		return result

	""" De Morgan of or """
	if operator == 'or':
		result.append('and')
		for subitem in item[1:]:
			Combine(result, CNF(TransNot(subitem)))
		return result

	""" for implies and iff """
	if operator == 'implies':
		result = NotProcessor(NotImpElimination(item))
		return result
	if operator == 'iff':
		result = NotProcessor(NotBioElimination(item))
		return result

def CNF(item):
	if GoalCheck(item):
		return item

	results = []
	operator = item[0]

	""" deal with BioElimination """
	if operator == 'iff':
		results = BioElimination(item)
		return results

	""" deal with Implication Elimination """
	if operator == 'implies':
		results = ImpElimination(item)
		return results

	""" deal with De Morgan and Double Negation Elimination """
	if operator == 'not':
		transResult = NotProcessor(item[1])
		results = CNF(transResult)
		return results

	""" deal with and, nothing special"""
	if operator == 'and':
		results = AndProcessor(item)
		return results
	
	""" deal with Distributivity """
	if operator == 'or':
		results = OrProcessor(item)
		return results
	
""" read the input file """
inputFile = open(sys.argv[2], 'r')
#inputFile = open("sentences.txt", 'r')

""" initial a list to store original data """
sequenceList = list()

""" read the first line, which is the object number """
linenum = inputFile.readline()

""" use buildin method eval to get data as array, then append it in list """
for line in inputFile:
	sequenceList.append(eval(line))

inputFile.close()

""" write result """
with open('sentences_CNF.txt', 'w') as out_file:

	""" doing the CNF, print the result after conversion  """
	for item in sequenceList:
		result = CNF(item)
		json.dump(result, out_file)
		out_file.write('\n')
		
out_file.close()