from collections import deque
import sys
import json
import linecache
import itertools
import operator
import math

inputFileName = sys.argv[2]
inputFile = open(inputFileName, 'r')
#name3, name4 = inputFileName.rsplit("/", 1)
#name1, name2 = name4.rsplit(".", 1)
name1, name2 = inputFileName.rsplit(".", 1)
outputFileName = name1 + "_inference.txt"
outputFile = open(outputFileName, 'w')

linecount = sum(1 for line in inputFile)
inputFile.seek(0,0)

P_disease = {}
P_feature_disease = {}
P_feature_not_disease = {}
diseasesName = list()
featureName = list()
wholeFeatureList = list()

temp = inputFile.readline()
diseasesNO, patientsNO = temp.split(" ")
diseasesNO = int(diseasesNO)
patientsNO = int(patientsNO)


for i in range(0,diseasesNO):
	featureList = list()
	featureList1 = list()
	P1List = list()
	P2List = list()
	P1List1 = list()
	P2List1 = list()
	diseaseName, symptomsNO, Pdisease = inputFile.readline().split()
	diseasesName.append(diseaseName)

	P_disease[diseaseName] = float(Pdisease)
	featureList1.append(eval(inputFile.readline()))
	for j in featureList1:
		for k in j:
			featureList.append(k)
			wholeFeatureList.append(k)

	P1List1.append(eval(inputFile.readline()))
	for j in P1List1:
		for k in j:
			P1List.append(k)
	queue1 = deque(P1List)

	P2List1.append(eval(inputFile.readline()))
	for j in P2List1:
		for k in j:
			P2List.append(k)
	queue2 = deque(P2List)


	for feature in featureList:	
		P_feature_disease[diseaseName + "/" + feature] = float(queue1.popleft())
		P_feature_not_disease[diseaseName + "/" + feature] = float(queue2.popleft())
		featureName.append(diseaseName + "/" + feature)

queue4 = deque(featureName)





def func1(featureQueue, flag):
	P_result = {}
	flag *= diseasesNO 
	for j in diseasesName:
		P_result[j] = 1 
		temp1 = 1
		temp2 = 1 		   
		P3List = list()
		P3List.append(eval(linecache.getline(inputFileName, 4 * diseasesNO + 2 + flag)))
		for item1 in P3List:
			for item in item1:
				temp = featureQueue.popleft()
				if item == "T":
					temp1 *= P_feature_disease[temp]
					temp2 *= P_feature_not_disease[temp]
				elif item == "F":
					temp1 *= 1 - P_feature_disease[temp]
					temp2 *= 1 - P_feature_not_disease[temp]
				elif item == "U":
					temp1 *= 1   
					temp2 *= 1
		temp1 *= P_disease[j]
		temp2 *= 1 - P_disease[j]
		P_result[j] = temp1 / (temp1 + temp2)
		P_result[j] = "{0:.4f}".format(P_result[j])
		flag += 1
	return P_result

def func2(flag):
	flag *= diseasesNO 
	flag1 = 0 # index
	flag2 = 0 # disease number, 1,2,3...
	flag3 = 0 # feature count for each disease
	flag4 = 0 
	P_result = {}
	for j in diseasesName:
		count = 0 #count of the combination
		wholeTempList = list()
		resultList = list()
		tempList1 = list()
		P3List = list()
		P3List.append(eval(linecache.getline(inputFileName, 4 * diseasesNO + 2 + flag)))
		for item1 in P3List:
			for item in item1:
				if item == "U":
					count += 1
		Ulist = list(itertools.product(["F", "T"], repeat=count))
		for List in Ulist:
			tempList = []
			queue = deque(List)
			for item1 in P3List:
				for item in item1:
					if item == "F":
						tempList.append("F")
					elif item == "T":
						tempList.append("T")
					elif item == "U":
						tempList.append(queue.popleft())
			wholeTempList.append(tempList)

		for List in wholeTempList: 
			flag1 = flag4
			temp1 = 1
			temp2 = 1
			for item in List:
				temp = featureName[flag1]
				if item == "T":
					temp1 *= P_feature_disease[temp]
					temp2 *= P_feature_not_disease[temp]
				elif item == "F":
					temp1 *= 1 - P_feature_disease[temp]
					temp2 *= 1 - P_feature_not_disease[temp]
				elif item == "U":
					temp1 *= 1   
					temp2 *= 1
				flag1 += 1

			temp1 *= P_disease[j]
			temp2 *= 1 - P_disease[j]
			result = temp1 / (temp1 + temp2)
			#result = float("{0:.4f}".format(result))
			resultList.append(result)

		flag2 += 1
		flag3 = len(List)
		flag4 += flag3
		#tempList1.append(str(float("{0:.4f}".format(min(resultList)))))
		#tempList1.append(str(float("{0:.4f}".format(max(resultList)))))
		tempList1.append("{0:.4f}".format(min(resultList)))
		tempList1.append("{0:.4f}".format(max(resultList)))
		P_result[j] = tempList1
		flag += 1
	return P_result


def func4(j,positionList, ValueIndex):
	temp = int(math.ceil((float(ValueIndex) + 1) / 2))
	temporary1 = positionList[temp - 1]
	flag6 = 0
	for feature in wholeFeatureList:
		if (j + "/" + feature) in featureName:				
			if flag6 == temporary1:
				theFeatureName = feature
				break;
			flag6 += 1
	return theFeatureName


def func3(flag):
	flag *= diseasesNO 
	flag1 = 0 # index
	flag2 = 0 # disease number, 1,2,3...
	flag3 = 0 # feature count for each disease
	flag4 = 0 
	P_result = {}
	for j in diseasesName:
		count = 0 #count of the combination
		wholeTempList = list()
		resultList = list()
		resultList1 = list()
		compareResultDict = {}
		P3List = list()
		P3List.append(eval(linecache.getline(inputFileName, 4 * diseasesNO + 2 + flag)))

		for item1 in P3List:
			wholeTempList.append(item1)
			for item in item1:
				if item == "U":
					count += 1
		"""no 'U' exist"""
		if count != 0: 
			positionList = []
			"""all possible occassions"""
			for k in range(0, count):
				tempList1 = []
				tempList2 = []			
				flag5 = 0 # just change one 'U'
				for List in P3List:
					for position, item in enumerate(List):	
						if item == "F":
							tempList1.append("F")
							tempList2.append("F")
						elif item == "T":
							tempList1.append("T")
							tempList2.append("T")
						elif item == "U":
							if position not in positionList:
								if flag5 == 0:
									positionList.append(position)
									tempList1.append("T")
									tempList2.append("F")
									flag5 = 1
								else:
									tempList1.append("U")
									tempList2.append("U")
							else:
								tempList1.append("U")
								tempList2.append("U")

				wholeTempList.append(tempList1)
				wholeTempList.append(tempList2)

			"""compute P for each occassion"""
			for position, List in enumerate(wholeTempList): 
				flag1 = flag4
				temp1 = 1
				temp2 = 1
				for item in List:
					temp = featureName[flag1]
					if item == "T":
						temp1 *= P_feature_disease[temp]
						temp2 *= P_feature_not_disease[temp]
					elif item == "F":
						temp1 *= 1 - P_feature_disease[temp]
						temp2 *= 1 - P_feature_not_disease[temp]
					elif item == "U":
						temp1 *= 1   
						temp2 *= 1
					flag1 += 1

				temp1 *= P_disease[j]
				temp2 *= 1 - P_disease[j]
				result = temp1 / (temp1 + temp2)

				if position == 0:
					originalResult = result
				else:
					resultList.append(result)

			"""compute max and min deficit"""
			for position, item in enumerate(resultList):
				compareResultDict[position] = (originalResult - item)

			#DecreaseValueIndex = max(compareResultDict.items(), key=operator.itemgetter(1))[0]
			#IncreaseValueIndex = min(compareResultDict.items(), key=operator.itemgetter(1))[0]
			"""find DecreaseValueIndex and IncreaseValueIndex"""
			DecreaseValue = compareResultDict[0]
			DecreaseValueIndex = 0
			IncreaseValue = compareResultDict[0]
			IncreaseValueIndex = 0

			for key, value in compareResultDict.iteritems():
				if value > DecreaseValue:
					DecreaseValueIndex = key
					DecreaseValue = value
				elif value == DecreaseValue:
					"""current key value pair"""
					tempName1 = func4(j,positionList, key) 
					"""stored pair"""
					tempName2 = func4(j,positionList, DecreaseValueIndex)
					if tempName1 < tempName2:
						DecreaseValueIndex = key

			for key, value in compareResultDict.iteritems():
				if value < IncreaseValue:
					IncreaseValueIndex = key
					IncreaseValue = value
				elif value == IncreaseValue:
					"""current key value pair"""
					tempName1 = func4(j,positionList, key) 
					"""stored pair"""
					tempName2 = func4(j,positionList, IncreaseValueIndex)
					if tempName1 < tempName2:
						IncreaseValueIndex = key


			"""generate resultList1"""
			"""for IncreaseValueIndex"""
			if compareResultDict[IncreaseValueIndex] != 0:
				theFeatureName = func4(j,positionList, IncreaseValueIndex)
				resultList1.append(theFeatureName)
				if (IncreaseValueIndex + 1) % 2 == 1:
					resultList1.append("T")
				else:
					resultList1.append("F")
			elif compareResultDict[IncreaseValueIndex] == 0:
				resultList1.append("none")
				resultList1.append("N")



			"""for DecreaseValueIndex"""
			if compareResultDict[DecreaseValueIndex] != 0:
				theFeatureName = func4(j, positionList, DecreaseValueIndex)
				resultList1.append(theFeatureName)
				if (DecreaseValueIndex + 1) % 2 == 1:
					resultList1.append("T")
				else:
					resultList1.append("F")
			elif compareResultDict[DecreaseValueIndex] == 0:
				resultList1.append("none")
				resultList1.append("N")

			P_result[j] = resultList1

			flag2 += 1
			flag3 = len(List)
			flag4 += flag3
			flag += 1

		else:
			P_result[j] = ["none", "N", "none", "N"]
	return P_result



for i in range(0,patientsNO):	
	outputFile.write("Patient-" + str(i+1) + ":" + "\n")
	"""question1"""
	P_result = func1(queue4, i)
	queue4 = deque(featureName)
	json.dump(P_result, outputFile)
	outputFile.write('\n')
	"""question2"""
	P_result = func2(i)
	json.dump(P_result, outputFile)
	outputFile.write('\n')
	"""question3"""
	P_result = func3(i)
	json.dump(P_result, outputFile)
	outputFile.write('\n')


inputFile.close()
outputFile.close()

