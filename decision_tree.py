""" 

The main idea is about looping through columns and do the following:
1- Checking which column has the highest information gain in each stage, and make it a parent node
2- The Loop continue as much as there are parent nodes
3- Also parent nodes that has a local entropy = 0, means that this is a leaf node
4- We build a dictionary of parents stating their parents and their children
5- We build a dictionary of leaves stating their value from the valuesDecision array
6- We use 2 python modules; "pandas" for ease tracking elements and performing operations on our data frame, and "anytree" for giving life
to our parents and leaves dictionaries as a visual tree    

"""

from __future__ import division
import pandas as pd
import math
from anytree import Node, RenderTree

#define columns' headers 
headersArray = ['Play','Temp','Humidity','Wind','Outlook']
headersArrayLen = len(headersArray)

#importing csv file
testdata = pd.read_csv('testdata.csv', names = headersArray)
print(testdata)

#get number of columns
numberOfColumns = len(testdata.columns)

#get number of rows
numberOfRows = len(testdata[[0]])

#selection by index dataframe.iloc[row,column] ,, unique() get unique values from column as array,, so the .csv file must contain the first column as the decision factor column
valuesDecision = testdata.iloc[:,0].unique()
valuesDecisionLen = len(valuesDecision)

#declaring an array for information gain
informationGainArray = []

#parents dictionary
parentDictionary = {}
parentDictionary['Outlook'] = ['Sunny','Overcast','Rain'] #random
canBeParent = [] #random
areParent = [0]
parentEntropies = [0]
parentDictionaryKey = 0
parentDictionaryValuesArray = [0]
canBeParentEntropies = []

#leaves dictionary
leavesDictionary = {}
leavesDictionary['Outlook'] = 'Yes' #random
canBeLeavesDictionary = {}

#labels parent dictionary
labelsParentDictionary = {}
canBeLabelsParent = {} #random

#define entropy length
entropyLength = 0

#start by the intial entropy:
#debug#testdata[testdata.iloc[:,0] == valuesDecision[1]] #print all columns of Yes
#debug#testdata[testdata.iloc[:,0] == valuesDecision[0]] #print all columns of No
entropyLength = valuesDecisionLen
PP = testdata[testdata.iloc[:,0] == valuesDecision[1]].shape[0] / numberOfRows 
PN = testdata[testdata.iloc[:,0] == valuesDecision[0]].shape[0] / numberOfRows
E_0 = - PP * math.log(PP,valuesDecisionLen) - PN * math.log(PN,valuesDecisionLen)
print("Initial Entropy = %f" %(E_0))

#stage 1 information gain for temp,humidity,wind,outlook
i = 1

#intialise max information gain by 0
maxInformationGain = 0

while(i < headersArrayLen):
	#select a column and reshape with values of Yes or No
	header = testdata.pivot(columns = headersArray[i], values = headersArray[0])
	print(header)
	
	headerColumns = header.columns.values
	headerColumnsLen = len(headerColumns)
	headerColumnsEntropy = []
	j = 0	
	while(j < headerColumnsLen):		
		PP = header[header.iloc[:,j] == valuesDecision[1]].shape[0] / header.count()[j] 
		print(PP)		
		PN = header[header.iloc[:,j] == valuesDecision[0]].shape[0] / header.count()[j]
		print(PN)		
		
		if(PP == 0 or PN == 0):			
			localEntropy = 0
			print(localEntropy)
		else:			
			localEntropy = - PP * math.log(PP,2) - PN * math.log(PN,2)
			print(localEntropy)
		
		#get local entropy 
		localEntropy = header.count()[j] / numberOfRows * localEntropy
		print(localEntropy)
		
		headerColumnsEntropy.append(localEntropy)
		print(headerColumnsEntropy)
		j += 1
	print(sum(headerColumnsEntropy))
	
	#get information gain
	localInformationGain = E_0 - sum(headerColumnsEntropy)
	 
	print("%s Information Gain = %f" %(headersArray[i],localInformationGain))
	informationGainArray.append(localInformationGain)

	if(localInformationGain > maxInformationGain):
		del canBeParent[:]
		leavesDictionary.clear()
		parentDictionary.clear()

		parentIndex = informationGainArray.index(max(informationGainArray)) + 1 #parent index is the index of column in the main original headersArray
		parentDictionary[headersArray[parentIndex]] = headerColumns #adding key parent and array of values
		#parrentDictionaryKeysArray.append(headersArray[parentIndex])
		#parrentDictionaryValuesArray.append(headerColumns) 
		maxInformationGain = localInformationGain
		l = 0
		temparr = []
		while(l < headerColumnsLen):
			temparr.append(headerColumns[l]) #adding the header columns to canbeparent
			l += 1
		canBeParent.append(temparr) #adding the header columns to canbeparent as a grouped values in single index in array,, so canBeParent is an array where each element is an array of values 
		for element in headerColumnsEntropy:
			elementIndex = 0
			if(element == 0):
				yesOrno = header.iloc[:,elementIndex].unique()
				for value in yesOrno:
					if(value == "Yes" or value == "No"):
						yesOrno = value
				leavesDictionary[headerColumns[headerColumnsEntropy.index(element)]] = yesOrno #adding a leaf and its value in the dictionary
			elementIndex += 1
		parentEntropies[0] = headerColumnsEntropy #adding the local entropies of the header to the array of parents' entropies
	i += 1
#end loop
areParent = canBeParent[:]  
print(informationGainArray)
print(areParent)
print(parentDictionary)
print(leavesDictionary)
print(parentEntropies)
print("Firt Stage Done...")
#New we constructed first stage

canBeParentLen = len(canBeParent)
#for the rest
for q in range(len(areParent)):
	for k in range(len(areParent[q])):
		if(parentEntropies[q][k] != 0):
			print(parentEntropies[q][k])
			print(areParent[q][k])
			print(headersArray)
			print(parentIndex)
			ktestdata = testdata[testdata.iloc[:,parentIndex] == areParent[q][k]].iloc[:, testdata.columns != headersArray[parentIndex]]
			print(ktestdata)
			#del headersArray[parentIndex] #del outlook header from main headers since we don't need him anymore
			#headersArrayLen = len(headersArray)
			numberOfColumns = len(ktestdata.columns)
			numberOfRows = len(ktestdata[[0]])
			informationGainArray = []
			PP = ktestdata[ktestdata.iloc[:,0] == valuesDecision[1]].shape[0] / numberOfRows 
			PN = ktestdata[ktestdata.iloc[:,0] == valuesDecision[0]].shape[0] / numberOfRows
			E_0 = - PP * math.log(PP,valuesDecisionLen) - PN * math.log(PN,valuesDecisionLen)
			print("Initial Entropy = %f" %(E_0))
			localHeadersArray = ktestdata.columns.values
			localHeadersArrayLen = len(localHeadersArray)

			i = 1

			#intialise max information gain by 0
			maxInformationGain = 0
			while((i < headersArrayLen) and (headersArray[i] in ktestdata.columns)):
				#select a column and reshape with values of Yes or No
				header = ktestdata.pivot(columns = headersArray[i], values = headersArray[0])
				print(header)
				
				headerColumns = header.columns.values
				headerColumnsLen = len(headerColumns)
				headerColumnsEntropy = []
				j = 0	
				while(j < headerColumnsLen):		
					PP = header[header.iloc[:,j] == valuesDecision[1]].shape[0] / header.count()[j] 
					print(PP)		
					PN = header[header.iloc[:,j] == valuesDecision[0]].shape[0] / header.count()[j]
					print(PN)		
					
					if(PP == 0 or PN == 0):			
						localEntropy = 0
						print(localEntropy)
					else:			
						localEntropy = - PP * math.log(PP,2) - PN * math.log(PN,2)
						print(localEntropy)
					
					#get local entropy 
					localEntropy = header.count()[j] / numberOfRows * localEntropy
					print(localEntropy)
					
					headerColumnsEntropy.append(localEntropy)
					print(headerColumnsEntropy)
					j += 1
				print(sum(headerColumnsEntropy))
				
				#get information gain
				localInformationGain = E_0 - sum(headerColumnsEntropy)
				 
				print("%s Information Gain = %f" %(headersArray[i],localInformationGain))
				informationGainArray.append(localInformationGain)

				if(localInformationGain > maxInformationGain):
					maxInformationGain = localInformationGain
					
					#del canBeParent[canBeParentLen:] #only clear after the original content
					del canBeParent[:]
					parentDictionaryKey = 0 
					del parentDictionaryValuesArray[:]
					canBeLeavesDictionary.clear()
					canBeLabelsParent.clear()

					canBeLabelsParent[areParent[q][k]] = headersArray[i] # this to assign label between 2 nodes,, example: Rain -->> Wind

					pparentIndex = informationGainArray.index(max(informationGainArray)) + 1
					parentDictionaryKey = headersArray[pparentIndex]
					parentDictionaryValuesArray.append(headerColumns)
					l = 0
					temparr = []
					while(l < headerColumnsLen):
						temparr.append(headerColumns[l]) #adding the header columns to canbeparent
						l += 1
					print(temparr)
					print(areParent) 
					canBeParent.append(temparr) #adding the header columns to canbeparent as a grouped values in single index in array,, so canBeParent is an array where each element is an array of values 
					print(headerColumnsEntropy)
					for element in range(len(headerColumnsEntropy)):
						if(headerColumnsEntropy[element] == 0):
							yesOrno = header.iloc[:,element].unique()
							for value in yesOrno:
								if(value == "Yes" or value == "No"):
									yesOrno = value
						canBeLeavesDictionary[headerColumns[element]] = yesOrno #adding a leaf and its value in the dictionary
						print(canBeLeavesDictionary)
					canBeParentEntropies = headerColumnsEntropy #adding the local entropies of the header to the array of parents' entropies
				i += 1
			#end loop
			parentDictionary[parentDictionaryKey] = parentDictionaryValuesArray[0]
			areParent.append(canBeParent[0]) 
			leavesDictionary.update(canBeLeavesDictionary)
			labelsParentDictionary.update(canBeLabelsParent)
			parentEntropies.append(canBeParentEntropies)
			print(areParent)
			print(parentDictionary)
			print(labelsParentDictionary)
			print(leavesDictionary)
			print(parentEntropies)
	testdata = testdata.iloc[:, testdata.columns != headersArray[parentIndex]]
	del headersArray[parentIndex] #del header from main headers since we don't need him anymore
	headersArrayLen = len(headersArray)
	parentIndex = informationGainArray.index(max(informationGainArray)) + 1

#Now we will convert the Dictionaries we have (parents,label parents, leaves nodes) from the key-value dictionary format
#into parent-child tree format ,, level by level as follow:

nodes = []
nodes2 = []
nodes3 = []
nodes4 = []
nodes5 = []
nodes6 = []

origin = parentDictionary.iterkeys().next()
print(origin)
root = Node(origin)
print(root)

pdk = parentDictionary.keys()
print(pdk)
for x in pdk:
	nodes.append(Node(x))
print(nodes)

for key, value in parentDictionary.iteritems():
		for v in value:
			for x in range(len(pdk)):		
				if(key == pdk[x] and key == origin):
					nodes2.append(Node(v,parent = root))
				elif(key == pdk[x]):
					nodes2.append(Node(v,parent = nodes[x]))
print(nodes2)

pdv = []
for key, value in parentDictionary.iteritems():
		for v in value:
			pdv.append(v)
print(pdv)


for key, value in labelsParentDictionary.iteritems():
		for x in range(len(pdv)):		
			if(key == pdv[x]):
				nodes3.append(Node(value,parent = nodes2[x]))

print(nodes3)

for key,value in parentDictionary.iteritems():
	for x in range(len(nodes3)):
		if(nodes3[x].name == key):
			for v in value:	
				nodes4.append(Node(v,parent=nodes3[x]))

print(nodes4)

for key,value in leavesDictionary.iteritems():
	for x in range(len(nodes4)):
		if(nodes4[x].name == key):
			nodes5.append(Node(value,parent=nodes4[x]))
	for x in range(len(nodes2)):
		if(nodes2[x].name == key):
			nodes5.append(Node(value,parent=nodes2[x]))

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))