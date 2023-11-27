import os, sys, re, math, xml.dom.minidom, time, datetime, traceback
from PIL import Image, ImageFont, ImageDraw

isLive = True
showTransfers = False
isLoggingToFile = True
MagicCaching = True

logFile = "errorRunLog.txt"

logStringList = []

def LOG(message, labels, *args):
	writeToLog("----------- ")
	writeToLog( str(datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple())).ctime()))
	writeToLog(" -----------\n")
	lastStack = traceback.extract_stack()
	writeToLog(message + "\n")
	writeStack(lastStack)
	log(0, labels, args)
	if isLoggingToFile == False:
		print "<!-- "
		for logString in logStringList:
			print logString
		print " -->"
	sys.exit(1)

def writeStack(lastStack):
	writeToLog("Stack Trace: \n")
	for item in lastStack[:-1]:
		writeToLog("\t File: " + str(item[0]) + "\t\t Line: " + str(item[1]) + "\n")
		writeToLog("\t\t Function: " + str(item[2]) + "\n")
		writeToLog("\t\t\t Line: " + str(item[3]) + "\n")

def writeToLog(string):
	if isLoggingToFile == True:
		f = open(logFile,"a")
		f.write(string)
		f.close()
	else:
		logStringList.append(string)

def log(tabLevel, logLabels, *args):
	tabs = ""
	for numTabs in range(tabLevel):
		tabs = tabs + "\t"

	for arg in args[0]:
		if type(arg) == type("string") or type(arg) == type(u"string"):
			#String
			if len(logLabels) > 0:
				writeToLog(tabs + logLabels[0] + ": " + str(arg) + "\n")
				logLabels = logLabels[1:]
			else:
				writeToLog(tabs + "String: " + str(arg) + "\n")
		elif type(arg) == type( getNode("R0") ):
			#Node
			if len(logLabels) > 0:
				writeToLog(tabs + logLabels[0] + ": " + str(getNodeId(arg)) + "\n")
				logLabels = logLabels[1:]
			else:
				writeToLog(tabs + "Node: " + str(getNodeId(arg)) + "\n")
		elif type(arg) == type(42):
			#Int
			if len(logLabels) > 0:
				writeToLog(tabs + logLabels[0] + ": " + str(arg) + "\n")
				logLabels = logLabels[1:]
		elif type(arg) == type([]):
			#List
			if len(logLabels) > 0 and tabLevel == 0:
				writeToLog(tabs + logLabels[0] + ": " + "\n")
				logLabels = logLabels[1:]
				for element in arg:
					log(tabLevel+1, arg)
			else:
				writeToLog(tabs + "List: " + "\n")
				for element in arg:
					log(tabLevel+1, arg)
		else:
			#Unknown
			if len(logLabels) > 0:
				writeToLog(tabs + logLabels[0] + ": " + str(arg) + "\n")
				logLabels = logLabels[1:]
			else:
				writeToLog("tabs + Other: " + str(arg) + "\n")

def drawResults(results):
	count = 0
	flag = False
	singleFlag = False
	firstFlag = True
	listToDisplay = [ [] ]
	displayAllFloorsAlongWay = True

	aList = results[1]

	path = ""
	if isLive:
		path = "../html/PNGCache"
	else:
		path = "PNGCache"

	if not os.path.isdir(path):
		os.mkdir(path)

	path = path + "/"	

	if not os.path.isdir(path + getNodeId(aList[0]) + "to" + getNodeId(aList[-1])):
		os.mkdir(path + getNodeId(aList[0]) + "to" + getNodeId(aList[-1]))

	path = path + getNodeId(aList[0]) + "to" + getNodeId(aList[-1]) + "/"
	
	imageNameList = []
	if (not displayAllFloorsAlongWay) and len(aList)==1:
		drawImage( [path + getFileForNode(aList[0]) + ".png" , aList])
		imageNameList.append(path + getFileForNode(aList[0]) + ".png")
		return imageNameList
	
	for item in aList:
		if firstFlag:	# Warning - this will break things if the first node is a transfer not on the World map
			listToDisplay[count].append(item)
			firstFlag = False
		elif getNodeId(item)[0] == 'T' and singleFlag:
			count = count + 1
			listToDisplay.append( [item] )
		elif getNodeId(item)[0] == "T" and not flag:
			listToDisplay[count].append(item)
			count = count + 1
			listToDisplay.append( [] )
			flag = True
			singleFlag = False
		else:
			listToDisplay[count].append(item)
			if getNodeId(item)[0] == 'T':
				singleFlag = True
			else:
				singleFlag = False
			flag = False
		
	
	for isthmus in listToDisplay:
		if len(isthmus)>0:
			if displayAllFloorsAlongWay == True or len(isthmus) > 1:
				drawImage( [path + getFileForNode(isthmus[0]) + ".png" , isthmus])
				imageNameList.append(path + getFileForNode(isthmus[0]) + ".png")

	return imageNameList

def getFileForNode(idea): 	
	if type(idea) != type(" ") or type(idea) != type(u" "):
		idea = getNodeId(idea)

	if idea == "The Quad":
		return "UICCampus"
	
	theType = "X"
	num = 0
	try:
		theType = idea[0]
		num = int(idea[1:])
	except:
		LOG("String split failed", ["theType", "num", "idea"], theType, num, idea)

	path = ""
	if isLive == True:
		path = "XML/ranges.txt"
	else:
		path = "ranges.txt"

	try:
		rangeFile = open(path, "r")
	except:
		LOG("LIVE FLAG IS NOT SET!", [])

	Lines = rangeFile.readlines()
	for line in Lines:
		arr = line.split()
		if theType == "R":
			if arr[1] != "X" and arr[2] != "X" and num>=int(arr[1]) and num<=int(arr[2]):
				return arr[0]
		if theType == "H":
			if arr[3] != "X" and arr[4] != "X" and num>=int(arr[3]) and num<=int(arr[4]):
				return arr[0]
		if theType == "T":
			if arr[5] != "X" and arr[6] != "X" and num>=int(arr[5]) and num<=int(arr[6]):
				return arr[0]
	if theType == "T" and (num==392 or num == 393):
		return "BSB-2"

	LOG("Failed to get file for " + str(idea) + " in the range file.", ["idea"], idea)

def getRangeFromNode(node):
	if type(node) != type("string") and type(node) != type(u"string"):
		node = getNodeId(node)

	try:
		theType = node[0]
		num = int(node[1:])
	except:
		LOG("Failed to split node string", ["theType", "num", "node"], theType, num, node)

	path = ""
	if isLive == True:
		path = "XML/ranges.txt"
	else:
		path = "ranges.txt"
	
	rangeFile = open(path, "r")
	Lines = rangeFile.readlines()
	for line in Lines:
		arr = line.split()
		if theType == "R":
			if arr[1] != "X" and arr[2] != "X" and num>=int(arr[1]) and num<=int(arr[2]):
				return arr
		if theType == "H":
			if arr[3] != "X" and arr[4] != "X" and num>=int(arr[3]) and num<=int(arr[4]):
				return arr
		if theType == "T":
			if arr[5] != "X" and arr[6] != "X" and num>=int(arr[5]) and num<=int(arr[6]):
				return arr

	LOG("Couldn't get the range for node " + node + " from the ranges file.", ["node"], node)
	

def getXMLFileObject(fileName):
	filePath = ""
	if isLive == True:
		filePath = "XML/" + fileName + ".xml"
	else:
		filePath = fileName + ".xml"
	return xml.dom.minidom.parse( filePath )

def getNode(id):
	xmlObject = getXMLFileObject( getFileForNode(id) )

	for node in xmlObject.getElementsByTagName("node"):
		if node.firstChild.firstChild.data == id:
			return node
	LOG("Failed to find node " + getNodeId(id) + " in file " + str(getFileForNode(id)), ["id", "getFileForNode(id)"], id, getFileForNode(id))

def getNodeId(node):
	if node == "The Quad":
		return "R434"	

	if type(node) == type(" ") or type(node) == type(u" "):
		return node

	try:
		return node.firstChild.firstChild.nodeValue

	except:
		LOG("Failed to getNodeId(node)", ["node"], node)

def getNodeType(node):
	return node.childNodes[1].firstChild.nodeValue

def getNodeCoordinate(node):
	if type(node) == type("string") or type(node) == type(u"string"):
		node = getNode(node)

	return ( float(node.childNodes[2].firstChild.firstChild.nodeValue), float(node.childNodes[2].lastChild.firstChild.nodeValue) )

def getDistanceBetweenCoordinates(firstCoordinate, secondCoordinate):
	return math.sqrt( math.pow(firstCoordinate[0]-secondCoordinate[0], 2) + math.pow(firstCoordinate[1]-secondCoordinate[1], 2) )

def getDistanceBetweenNodes(node1, node2):
	firstCoordinate = getNodeCoordinate(node1)
	secondCoordinate = getNodeCoordinate(node2)

	return getDistanceBetweenCoordinates(firstCoordinate, secondCoordinate)

def getAdjacentNodes(node):
	adjacentNodes = []
	try:
		for childNode in node.lastChild.childNodes:
			adjacentNodes.append( getNode( childNode.firstChild.nodeValue ) )
		return adjacentNodes
	except:
		LOG("Failed to get adjacent nodes\n " + str(inst), ["node"], node)

def getAdjacentTransferNodes(node):
		if type(node) != type("String"):
				node = getNodeId(node)

		adjacentNodes = []
		filePath = ""
		if isLive == True:
				filePath = "XML/transfers.txt"
		else:
				filePath = "transfers.txt"

		transferFile = open(filePath, "r")

		possibleTransfers = []
		readLines = transferFile.readlines()
		transferFile.close()

		for line in readLines:
				items = line.split()
				if node == items[0]:
						return items

def goingSomewhere(startNode, endNode, count, direction, basement=False):
	startNode = getNodeId(startNode)
	endNode = getNodeId(endNode)

	xmlPath = ""
	if isLive == True:
		xmlPath = "XML/"
	else:
		xmlPath = ""	

	if count < 0:
		LOG("Bad count provided", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)

	if direction < -1 or direction > 1:
		LOG("Bad direction provided", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)

	if direction == 0 and getFileForNode(startNode) == getFileForNode(endNode):
		endNode = "R434"

	if direction == 1 and getFileForNode(startNode) == getFileForNode(endNode) and basement == True:
		endNode = "R" + getRangeForFile( getFileForNode(endNode).split('-')[0] + "-1" )[1]

	if direction == -1 and getFileForNode(startNode) == getFileForNode(endNode):
		if getFileForNode(endNode).split('-')[1] == "1":
			endNode = "R" + getRangeForFile( getFileForNode(endNode).split('-')[0] + "-Basement")[1]
		else:
			path = xmlPath + getFileForNode(endNode).split('-')[0] + "-" + str(int(getFileForNode(endNode).split('-')[1])-1) + ".xml"
			while not os.path.exists(path):
				path = path.split('-')[0] + "-" + str(int(path.split('-')[1][0])-1) + ".xml"
				if int(path.split('-')[1][0]) < 1:
					LOG("We went too far down", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)
				
			endNode = "R" + getRangeForFile( path[:-4] )

	acceptableTransferIds = []

	directionFileName = ""

	# SPECIAL CASE
	startNodeFile = getFileForNode(startNode)
	if len(startNodeFile.split('-')) == 1:
		startNodeFile = startNodeFile + "-1"

	#1st Floor -> Basement
	if direction == -1 and basement == True:
		directionFileName = getFileForNode(startNode).split('-')[0] + "-Basement"

	#Basement -> 1st Floor
	elif direction == 1 and basement == True:
		directionFileName = getFileForNode(startNode).split('-')[0] + "-1"

	#Nth floor -> N-1st floor
	elif direction == -1 and basement == False:
		directionFileName = getFileForNode(startNode).split('-')[0] + "-" + str( int( getFileForNode(startNode).split('-')[1]) - 1 )
		if isLive == True:
			while not os.path.exists("XML/" + directionFileName + ".xml"):
				directionFileName = directionFileName[:-1] + str(int(directionFileName[-1])-1)
				if int(directionFileName[-1]) < 1:
					LOG("While going down, went below floor 1", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)
		else:
			while not os.path.exists(directionFileName + ".xml"):
				directionFileName = directionFileName[:-1] + str(int(directionFileName[-1])-1)
				if int(directionFileName[-1]) < 1:
					LOG("While going down, went below floor 1", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)

	
	#Nth floor -> N+1st floor
	elif direction == 1 and basement == False:
		directionFileName = getFileForNode(startNode).split('-')[0] + "-" + str( int( getFileForNode(startNode).split('-')[1]) + 1 )
		if isLive == True:
			while not os.path.exists("XML/" + directionFileName + ".xml"):
				directionFileName = directionFileName[:-1] + str(int(directionFileName[-1])+1)
				if int(directionFileName[-1]) > 8:
					LOG("While going up, went above floor 8", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)
		else:
			while not os.path.exists(directionFileName + ".xml"):
				#print directionFileName + ".xml"
				directionFileName = directionFileName[:-1] + str(int(directionFileName[-1])+1)
				if int(directionFileName[-1]) > 8:
					LOG("While going up, went above floor 8", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)


	#Inward -> Out
	elif direction == 0 and basement == False and getFileForNode(startNode) != "UICCampus" and startNodeFile.split('-')[1] == "1":
		directionFileName = "UICCampus"

	#Outward -> In
	elif direction == 0 and basement == False and getFileForNode(startNode) == "UICCampus":
		directionFileName = getFileForNode(endNode).split('-')[0] + "-1"
	
	#It should never hit this else
	else:
		LOG("Hit the else condition in goingSomewhere.  Assert.", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)

	ranges = getRangeForFile(directionFileName)
	for i in range( int(ranges[5]), int(ranges[6])+1 ):
		acceptableTransferIds.append( "T" + str(i) )

	transfersOnFloor = []
	transfersOnFloorRange = getRangeFromNode(startNode)	

	for i in range( int( transfersOnFloorRange[5] ), int( transfersOnFloorRange[6]) + 1):
		transfersOnFloor.append( "T" + str(i) )

	# Special case 392 and 393 are "Sean's special T's"
	if getFileForNode(startNode) == "BSB-2":
		transfersOnFloor.append( "T" + str(392) )
		transfersOnFloor.append( "T" + str(393) )

	transfers = []

	for transferOnFloor in transfersOnFloor:
		for acceptableTransferId in acceptableTransferIds:
			for adjacentTransfer in getAdjacentTransferNodes( transferOnFloor ):
				if adjacentTransfer == acceptableTransferId:
					transfers.append([transferOnFloor, adjacentTransfer])

	startBuildingCoordinate = getBuildingTransferCoordinate(startNode)
	endBuildingCoordinate =   getBuildingTransferCoordinate(endNode)

	heuristicCoordinate = (0,0)

	# When we're in the basement and going up, sort by what is closest to the currentNode
	if basement == True and direction == 1:
		heuristicCoordinate = getNodeCoordinate( startNode )
	
	#When we're going down to the basement, sort by what is closest to the currentNode
	elif basement == True and direction == -1:
		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're going upward, sort by what is closest to the currentNode
	elif basement == False and direction == 1:
		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're going downward, sort by what is closest to the currentNode
	elif basement == False and direction == -1:
		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're exiting the building, sort by the extrapolated distance from startBuildingCoordinate to endBuildingCoordinate
	#	pushed out to the boundaries of the image
	elif basement == False and direction == 0 and getFileForNode(startNode) != "UICCampus":
		if startBuildingCoordinate[0] < endBuildingCoordinate[0]:
			#Positive
			slope = (endBuildingCoordinate[1] - startBuildingCoordinate[1]) / (endBuildingCoordinate[0] - startBuildingCoordinate[0])
			heuristicCoordinate = ( (startBuildingCoordinate[0] + 2000), (startBuildingCoordinate[1] + (2000*slope)) )

		elif startBuildingCoordinate[0] > endBuildingCoordinate[0]:
			#Negative
			slope = (endBuildingCoordinate[1] - startBuildingCoordinate[1]) / (endBuildingCoordinate[0] - startBuildingCoordinate[0])
			heuristicCoordinate = ( (startBuildingCoordinate[0] - 2000), (startBuildingCoordinate[1] - (2000*slope)) )

		else:
			if startBuildingCoordinate[1] < endBuildingCoordinate[1]:
				heuristicCoordinate = (startBuildingCoordinate[0], endBuildingCoordinate[0] + 2000)
			elif startBuildingCoordinate[1] > endBuildingCoordinate[1]:
				heuristicCoordinate =  (startBuildingCoordinate[0], endBuildingCoordinate[0] - 2000)
			else:
				heuristicCoordinate = startBuildingCoordinate

	# When we're entering a building, 
	elif basement == False and direction == 0 and getFileForNode(startNode) == "UICCampus":
		# SEAN, FILL ME IN
		heuristicCoordinate = (0,0)
		
	else:
		LOG("WTF MATE!?", ["startNode", "endNode", "direction", "count", "basement"], startNode, endNode, direction, count, basement)

	if direction == 0:
		transfers.sort(key=lambda(k): getDistanceBetweenCoordinates( getNodeCoordinate(getNode(k[0])), heuristicCoordinate ) )
	else:
		transfers.sort(key = lambda(k): getDistanceBetweenNodes(startNode, getNode(k[0]) ))

	return transfers[count]				

def getRangeForFile(fileName):
	path = ""
	if isLive == True:
		path = "XML/ranges.txt"
	else:
		path = "ranges.txt"

	rangeFile = ""
	try:
		rangeFile = open(path, "r")
	except:
		LOG("LIVE FLAG IS NOT SET", ["fileName"], fileName)
	
	for line in rangeFile.readlines():
		line = line.split()
		if line[0] == fileName:
			return line
	
	LOG("Failed to find fileName in ranges file.", ["fileName"], fileName)

def goingSomewhereOld(startNode, endNode, count, direction, basement=False):
	if type(startNode) != type("str") or type(startNode) != type(u"str"):
		startNode = getNodeId(startNode)
	if type(endNode) != type("str") or type(endNode) != type(u"str"):
		endNode = getNodeId(endNode)
		
	if count < 0: # Why did you have this? or count > 1:
		print "What you doing!?  Bad direction."
		sys.exit(1)
	print  "Going Somewhere: Start File: " + getFileForNode(startNode) + " End File: " + getFileForNode(endNode) + " Count: " + str(count) + " Direction: " + str(direction) + " Basement? " + str(basement)
	

	allTransferIdsRange = getRangeFromNode(startNode)
	allTransferIds = range(int(allTransferIdsRange[5]), int(allTransferIdsRange[6])+1)
	if getFileForNode(startNode) == "BSB-2":
		#392, 393 are "Sean's special T's"
		allTransferIds.append(392)
		allTransferIds.append(393)
	
	transfers = []

	outsideTransferIds = []
	if direction == 0:  
		outsideTransferIds = getRangeFromNode("T" + str(390) )  #Something outside
		outsideTransferIds = range(int(outsideTransferIds[5]), int(outsideTransferIds[6])+1)
	
	for transferId in allTransferIds:
		nodeObject = getNode( "T" + str(transferId) )
		adjNodes = getAdjacentTransferNodes( "T" + str(transferId) )
		if direction == -1:
			if basement == False:
				maxNode = -1
				for adjNode in adjNodes[1:]:
					if int(adjNode[1:]) < int(adjNodes[0][1:]):
						if int(adjNode[1:]) > maxNode:
							maxNode = int(adjNode[1:])
				if maxNode != -1:
					transfers.append(["T" + adjNodes[0][1:] ,"T" + str(maxNode)])
			else:
				maxNode = -1
				for adjNode in adjNodes[1:]:
					if int(adjNode[1:]) > int(adjNodes[0][1:]):
						if int(adjNode[1:]) < 367:  #Ignore outside transfers
							if int(adjNode[1:]) > maxNode:
								maxNode = int(adjNode[1:])
				if maxNode != -1:
					transfers.append(["T" + adjNodes[0][1:], "T" + str(maxNode)])

		elif direction == 1:
			if basement == False:
				minNode = 99999
				for adjNode in adjNodes[1:]:
					if int(adjNode[1:]) > int(adjNodes[0][1:]):
						if int(adjNode[1:]) < minNode:
							if ( int(adjNode[1:]) < 367 ) or ( int(adjNode[1:]) > 391 ):
								minNode = int(adjNode[1:])
				if minNode != 99999:
					transfers.append(["T" + adjNodes[0][1:],"T" + str(minNode)])
			else:
				minNode = 99999
				for adjNode in adjNodes[1:]:
					if int(adjNode[1:]) < int(adjNodes[0][1:]):
						if int(adjNode[1:]) < minNode:
							if ( int(adjNode[1:]) < 367 ) or ( int(adjNode[1:]) > 391 ):
								minNode = int(adjNode[1:])
								#print "minNode is now: " + str(minNode)
					transfers.append(["T" + adjNodes[0][1:], "T" + str(minNode)])

		elif direction == 0:
			if basement == True:
				LOG("You shouldn't be calling me with the basement flag!", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)
			for outsideTransfer in outsideTransferIds:
				for adjNode in adjNodes[1:]:
					if adjNode[1:] == str(outsideTransfer):
						transfers.append(["T" + adjNodes[0][1:], "T" + str(outsideTransfer)])

		else:
			LOG("Bad direction chose", ["startNode", "endNode", "count", "direction", "basement"], startNode, endNode, count, direction, basement)
	if basement == True:
		transfers = sorted(transfers,key=lambda x:[1])
		transfers.reverse()

	for index, node in enumerate(transfers[count:]):
		file1 = getFileForNode(getNode(node[0]))
		file2 = getFileForNode(getNode(node[1]))
		if file1 == "UICCampus":
			if direction == 0:
				break
			#print "UICCampus is not valid in goingSomewhere"
			transfers.remove(node)
		if file2 == "UICCampus":
			if direction == 0:
				break
			#print "UICCampus is not valid in goingSomewhere"
			transfers.remove(node)

		#transfers across building
		if file1.split('-')[0] != file2.split('-')[0]:
			if direction != 0:
				transfers.remove(node)	
	
			file1 = file1.split('-')[1]
			file2 = file2.split('-')[1]
			if file1 == "Basement":
				file1=-1
			if file2 == "Basement":
				file2=-1       
			if file1<file2:
				if direction == 0:
					transfers.remove(node)
				if direction == -1:
					transfers.remove(node)                
			if file1>file2:
				if direction == 0:
					transfers.remove(node)
				if direction == 1:
					transfers.remove(node)

	if basement == True:
		while(len(transfers[count])<2):
			count=count+1
			if count>len(transfers):
				return getNode(startNode), getNode(endNode)     #Don't error out?

		return [getNode( transfers[count][0] ), getNode( transfers[count][1] )]


#	print getFileForNode(endNode)
#	for item in transfers:
#		print item[0], item[1]

		# could extrapolate out.  vector from getNodeToEnter(getFileForNode(startNode)) to getNodeToEnter(getFileForNode(endNode)), extended to edge
		# This won't work for UICCampus
		if getFileForNode(endNode)!="UICCampus":
#			print getFileForNode(endNode)
			transfers.sort(key=lambda(k): getDistanceBetweenNodes(getNodeToEnter(getFileForNode(endNode).split('-')[0]), getNode(k[1])))
#			for item in transfers:
#				print item[0], item[1]

	
	startBuildingCoordinate = getBuildingTransferCoordinate(startNode)
	endBuildingCoordinate =   getBuildingTransferCoordinate(endNode)

	heuristicCoordinate = (0,0)

	# When we're in the basement and going up, sort by what is closest to the currentNode
#	if basement == True and direction == 1:
#		heuristicCoordinate = getNodeCoordinate( startNode )
	
	#When we're going down to the basement, sort by what is closest to the currentNode
#	elif basement == True and direction == -1:
#		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're going upward, sort by what is closest to the currentNode
	if basement == False and direction == 1:
		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're going downward, sort by what is closest to the currentNode
	elif basement == False and direction == -1:
		heuristicCoordinate = getNodeCoordinate( startNode )

	#When we're exiting the building, sort by the extrapolated distance from startBuildingCoordinate to endBuildingCoordinate
	#	pushed out to the boundaries of the image
	elif basement == False and direction == 0:
		exponent = -9999
		if startBuildingCoordinate[0] < endBuildingCoordinate[0]:
			#Positive
			slope = (endBuildingCoordinate[1] - startBuildingCoordinate[1]) / (endBuildingCoordinate[0] - startBuildingCoordinate[0])
			heuristicCoordinate = ( (startBuildingCoordinate[0] + 2000), (startBuildingCoordinate[1] + (2000*slope)) )

		elif startBuildingCoordinate[0] > endBuildingCoordinate[0]:
			#Negative
			exponent = 1
			slope = (endBuildingCoordinate[1] - startBuildingCoordinate[1]) / (endBuildingCoordinate[0] - startBuildingCoordinate[0])
			heuristicCoordinate = ( (startBuildingCoordinate[0] - 2000), (startBuildingCoordinate[1] - (2000*slope)) )

		else:
			if startBuildingCoodinate[1] < endBuildingCoordinate[1]:
				heuristicCoordinate = (startBuildingCoordinate[0], endBuildingCoordinate[0] + 2000)
			elif startBuildingCoordinate[1] > endBuildingCoordinate[1]:
				heuristicCoordinate =  (startBuildingCoordinate[0], endBuildingCoordinate[0] - 2000)
			else:
				heuristicCoordinate = startBuildingCoordinate

	if basement == False:
		transfers.sort(key=lambda(k): getDistanceBetweenCoordinates( startBuildingCoordinate, heuristicCoordinate ) )

	while(len(transfers[count])<2):
			count=count+1
			if count>len(transfers):
				return getNode(startNode), getNode(endNode)     #Don't error out?

	return [getNode( transfers[count][0] ), getNode( transfers[count][1] )]

def getBuildingTransferCoordinate(node):
	if type(node) != type("String") or type(node) != type(u"string"):
		node = getNodeId(node)

	if(node=="R434"):
		returnNode = getNode(node)
	else:
		returnNode = getNodeFromRoomName( getFileForNode(node).split('-')[0] )
	
	return getNodeCoordinate(returnNode)
	
def debugPrintNode(id, levels=0):
	if type(id) == type("string"):
		id = getNode(id)

	for x in range(levels):
		print "\t",
	print "Information for node: " + getNodeId( id )
	
	for x in range(levels):
		print "\t",
	print "\t Type:              " + getNodeType( id )

	for x in range(levels):
		print "\t",
	print "\t Coord:             " + str(getNodeCoordinate( id ))

def aStarSearchOld(startNode, endNode):
	# Type corrections
	if type(startNode) == type("someString"):
		startNode = getNode(startNode)
	if type(endNode) == type("someString"):
		endNode = getNode(endNode)

	# Return a list with only "startNode" if startNode and endNode are equivalent
	if getNodeId(startNode) == getNodeId(endNode):
		return [ 0, [startNode] ]

	closedSet = []
	openSet = [ startNode ]
	g_score = {}
	g_score[startNode] = [0, [startNode]]
	while len(openSet) > 0:
		x = sorted(openSet, key=lambda(k): getDistanceBetweenNodes(k, endNode))[0]

		if getNodeId(x) == getNodeId(endNode):
			return g_score[x]
		
		closedSet.append(x)
		openSet.remove(x)

		if x != startNode and x != endNode and getNodeType(x) == "transition":
			continue

		adjacentNodes = getAdjacentNodes( x )

		for node in adjacentNodes:
			if getNodeType(node) != "transition" or True:

				TriforceOfWisdom = 1
				TriforceOfCourage = 1
				for danger in closedSet:
					if getNodeId(danger) == getNodeId(node):
						TriforceOfWisdom = 0
				for peril in openSet:
					if getNodeId(peril) == getNodeId(node):
						TriforceOfCourage = 0
				if TriforceOfCourage:
					if TriforceOfWisdom:
						openSet.append(node)

				#if not (node in closedSet):
					#if not (node in openSet):
				#if closedSet.count(node) == 0:
					#if openSet.count(node) == 0:

				g_score[node] = [g_score[x][0] + getDistanceBetweenNodes(x, node), g_score[x][1]+[node]]
	LOG("AStarSearch found no path!", ["startNode", "endNode"], startNode, endNode)

def drawImage(parameter):
	results = parameter
	endImagePath = parameter[0]

	imagePath = ""
	if isLive == True:
		imagePath = r"PNGs/" + getFileForNode( getNodeId(results[1][0]) ) + ".png"
	else:
		imagePath = r"../../Images/Converted Files/" + getFileForNode( getNodeId(results[1][0]) ) + ".png"

	image = Image.open(imagePath)
	
	offset = 0
	if getFileForNode( getNodeId(results[1][0]) ) != "UICCampus":
		image = image.rotate(-90)
	else:
		offset = -50
	
	triangles = []

	draw = ImageDraw.Draw(image)
	x1, y1 = getNodeCoordinate(results[1][0])
	x1 = int(x1)
	y1 = int(y1)
	x1 = x1*2+offset
	y1 = y1*2
	asize = 15
	arcs = []
	for excaliber in range(asize-2,asize+2):
		arcs.append( [(x1-excaliber, y1-excaliber, x1+excaliber, y1+excaliber), (0,0,255,255)] )
	for index, result in enumerate(results[1]):
		if(index!=0):
			x1, y1 = getNodeCoordinate(result)
			x2, y2 = getNodeCoordinate(results[1][index-1])
			y3 = 612-x1-135
			x3 = 792-y1+120
			y4 = 612-x2-135
			x4 = 792-y2+120
			x1 = int(x1)*2+offset
			x2 = int(x2)*2+offset
			y1 = int(y1)*2
			y2 = int(y2)*2
			x3 = int(x3)*2+offset
			x4 = int(x4)*2+offset
			y3 = int(y3)*2
			y4 = int(y4)*2
			if index != 0 and index != len(results[1])-1:
				psize = 5
				draw.pieslice( (x1-psize, y1-psize, x1+psize, y1+psize), 0, 360, fill = (10, 230, 70, 120) )
			draw.line((x1,y1, x2,y2), fill = (10,230,70,120),width=12)
			
			triX = (x1 + x2)/2
			triY = (y1 + y2)/2
			angle = math.atan2( (y1 - y2), (x1 - x2) )
			size = 10
			triX1 = triX + size*math.cos(angle)
			triY1 = triY + size*math.sin(angle)

			triX2 = triX + (size/2)*math.sin(angle)
			triY2 = triY - (size/2)*math.cos(angle)

			triX3 = triX - (size/2)*math.sin(angle)
			triY3 = triY + (size/2)*math.cos(angle)
			
			triangles.append( (triX1,triY1, triX2, triY2, triX3, triY3) )
	
	for triangle in triangles:
		draw.polygon( triangle, fill=(255,0,70,120) )
	x1, y1 = getNodeCoordinate(results[1][len(results[1])-1])
	x1 = int(x1)*2+offset
	y1 = int(y1)*2
	for excaliber in range(asize-2,asize+2):
		arcs.append([ (x1-excaliber, y1-excaliber, x1+excaliber, y1+excaliber), (255,0,0,255)] )

	for arc in arcs:
		draw.arc(arc[0], 0, 360, fill = arc[1])

	imageSavePath = ""
	if isLive == True:
		imageSavePath = endImagePath
	else:
		imageSavePath = endImagePath

	# Debug showTransfers
	if showTransfers == True:
		someListVar = getRangeFromNode(getNodeId(results[1][0]))
	
		for anInt in range(int(someListVar[5]), int(someListVar[6])+1):
			anotherNode = getNode("T"+str(anInt))
			x1, y1 = getNodeCoordinate(anotherNode)
			x1 = 2*int(x1)
			y1 = 2*int(y1)
		
			f = ImageFont.load("XML/font/courB24.pil")
			draw.text((x1-5, y1-5), getNodeId(anotherNode), font=f, fill = (0,0,0) )        

	if getFileForNode( getNodeId(results[1][0]) ) != "UICCampus":
		image = image.rotate(90)

	image.save(imageSavePath)


def findErroneousNodes():
	if isLive == False:
		#Do Debug Drawing
		
		for anInt in range(434):
			if getRoomNameForNode("R"+str(anInt)).find("BROKEN")!=-1:
				imagePath = r"../../Images/Converted Files/" + getFileForNode( "R" + str(anInt) ) + ".png"

				image = Image.open(imagePath)
				image = image.rotate(-90)
				draw = ImageDraw.Draw(image)                
				x1, y1 = getNodeCoordinate(getNode("R"+str(anInt)))
				draw.line((x1-15, y1-15, x1+15, y1+15),  fill = (0, 255, 0, 255)) 
				draw.line((x1-15, y1+15, x1+15, y1-15),  fill = (0, 255, 0, 255)) 
				image = image.rotate(90)
				image.save(imagePath[:-4]+"R"+str(anInt)+".png")

def getRoomNameForNode( node ):
	#If we're given a node, convert it to a string
	if type(node) != type("someString"):
		node = getNodeId(node)

	filePath = ""
	if isLive == True:
		filePath = r"XML/roomnumbermap.txt"
	else:
		filePath = r"roomnumbermap.txt"

	thefile = open(filePath, "r")
	Lines = thefile.readlines()
	thefile.close()
	for Line in Lines:
		item = Line.split()
		fileNodeId = "R" + item[0]
		if fileNodeId == node:
			fileName = getFileForNode( node )
			if fileName.find("-") != -1:
				fileName = fileName[0:fileName.find("-")]
			return fileName + " " + item[1]

	#Special case!!!
	if node[0] == "T":
		campusFilePath = ""
		if isLive == True:
			campusFilePath = r"XML/UICCampusnumbermap.txt"
		else:
			campusFilePath = r"UICCampusnumbermap.txt"
		
		campusFile = open(campusFilePath, "r")
		for line in campusFile.readlines():
			item = line.split()
			if node == item[0]:
				return item[1]
		
		#Later on, we want to remove this return node, somehow
		return node

	LOG("Tried searching for room name for " + getNodeId(node) + " and failed.", ["node", "getFileForNode(node)"], node, getFileForNode(node))

def getNodeFromRoomName( roomName ):
	if type(roomName) != type("string"):
		LOG("getNodeFromRoomName given a non-string", [])
		
	filePath = ""
	if isLive == True:
		filePath = r"XML/roomnumbermap.txt"
	else:
		filePath = r"roomnumbermap.txt"
	
	thefile = open(filePath, "r")
	Lines = thefile.readlines()
	thefile.close()
	for Line in Lines:
		item = Line.split()
		#print roomName, item
		if str(roomName) == (item[2] + " " + item[3]):
			return "R" + item[0]

	#Special Case!!!
	if roomName == "The Quad" and roomName != "TH":
		return roomName

	campusFilePath = ""
	if isLive == True:
		campusFilePath = r"XML/UICCampusnumbermap.txt"
	else:
		campusFilePath = r"UICCampusnumbermap.txt"
	
	campusFile = open(campusFilePath, "r")
	for line in campusFile.readlines():
		item = line.split()
		if item[1] == roomName:
			return item[0]

	if roomName == "UICCampus":
		return "R434"
			
	LOG("Tried searching for " + roomName + " to get a node and failed.", ["roomName"], roomName)

def addToRoomNumberMap():
	if isLive == True:
		LOG("YOU SHOULDNT RUN THIS LIVE!", [])

	aFile = open("roomnumbermap.txt", 'r')
	bFile = open("roomnumbermapfinal.txt", 'w')

	theMajorString = ""

	Lines = aFile.readlines()
	for line in Lines:
		item = line.split()
		theMajorString = theMajorString + item[0] + "\t" + item[1] + "\t"
		fileName = getFileForNode( "R" + item[0] )
		if fileName.find("-") != -1:
			fileName = fileName[0:fileName.find("-")]
		theMajorString = theMajorString + fileName + "\t" + item[1] + "\n"
	
	bFile.write(theMajorString)
	aFile.close()
	bFile.close()
	

def overallAStarSearch(startNode, endNode, currentNode, stepsTravelled, History, specialCountSuchAHack = 0):
	if type(startNode) == type([1]):
		stepsTravelled = stepsTravelled + startNode[0]
		History.extend(startNode[1])        #startNode[1].extend(History)
		startNode = currentNode
		
	count = 0
	initialFile = getFileForNode(startNode)
	endingFile = getFileForNode(endNode)
	basementSearch = False

	#Test for Initial file being a basement
	if len(initialFile.split('-')) == 2:
				if initialFile.split('-')[1]=='Basement':
	#					if len(endingFile.split('-')) == 2:
	#						if endingFile.split('-')[1]=='1':
								basementSearch = True

	#Test for Ending file being a basement
	if len(endingFile.split('-')) == 2:
				if endingFile.split('-')[1]=='Basement':# and initialFile.split('-')[0] == endingFile.split('-')[0]:
						if len(initialFile.split('-')) == 2:
							if initialFile.split('-')[0]==endingFile.split('-')[0] and initialFile.split('-')[1] == "1":
								basementSearch = True

	if initialFile.split('-')[0] == endingFile.split('-')[0]:   # I don't think this is a special case for UICCampus
		if initialFile == endingFile:
			retVale = simpleAStarSearch(startNode, endNode)
			if retVale == "FAIL":
				if len(initialFile.split('-'))==1:
					while count<10:
						nextNode = goingSomewhere(startNode,endNode, count, 0, basementSearch)
						result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)   #getNodeToEnter(initialFile.split('-')[0])
						count = count+1
						if result[2]== "alive":
							return [result[0], result[1], "alive", History]					
				else:
					if len(initialFile.split('-'))==0 or initialFile.split('-')[1]=='1':
						nextNode = goingSomewhere(startNode,endNode, 0, 0, basementSearch)
						result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)   #getNodeToEnter(initialFile.split('-')[0])
						return [result[0], result[1], "alive", History]
					elif initialFile.split('-')[1]=="Basement":
						while True:
							nextNode = goingSomewhere(startNode, endNode, count, 1, basementSearch) # 1 for going up
							result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History, 2)
							count = count+1
							if count > 30 :     # there aren't more than 10 ways up in a map
								return [result[0], result[1], "dead", History]
							if result[2] == "alive":
								return [result[0], result[1], "alive", History]
					else: # int(initialFile.split('-')[1])>1:
						while True:
							nextNode = goingSomewhere(startNode, endNode, count, -1, basementSearch) # -1 for going down
							result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)
							count = count+1
							if count > 30 :     # there aren't more than 10 ways up in a map
								return [result[0], result[1], "dead", History]
							if result[2] == "alive":
								return [result[0], result[1], "alive", History]
				return [startNode, endNode, "dead", History]
			return [retVale[0], History+retVale[1], "alive", History]

		initialFile = initialFile.split('-')[1]        
		if initialFile == "Basement":
			initialFile = -1
		else:
			initialFile = int(initialFile)

		endingFile = endingFile.split('-')[1]
		if endingFile == "Basement":
			endingFile = -1
		else:
			endingFile = int(endingFile)
		
		if initialFile<endingFile:
			while True:
				nextNode = goingSomewhere(startNode, endNode, count, 1, basementSearch) # 1 for going up
				result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)
				count = count+1
				if count > 30 :     # there aren't more than 10 ways up in a map
					return [result[0], result[1], "dead", History]
				if result[2] == "alive":
					return [result[0], result[1], "alive", History]
		
		if initialFile>endingFile:
			while True:
				nextNode = goingSomewhere(startNode, endNode, count+specialCountSuchAHack, -1, basementSearch)    # -1 for going down.  WIN!
				result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)
				count = count+1
				if count > 20 :     # there aren't more than 10 ways up in a map
					return [result[0], result[1], "dead", History]
				if result[2] == "alive":
					return [result[0], result[1], "alive", History]
				
	else:
		if initialFile == "UICCampus":
			while True:
				nextNode = getNodeToEnter(endingFile.split('-')[0])
				listOfEntryPoints = getAdjacentTransferNodes(getNodeId(nextNode))	# It will still go around a building to enter at the closest to the endpoint.
				currNode993 = listOfEntryPoints[0]
				listOfEntryPoints = sorted(listOfEntryPoints[1:], key=lambda(k): getDistanceBetweenNodes(k, endNode))
				listOfEntryPoints.append(currNode993)
				result = overallAStarSearch(simpleAStarSearch(startNode, nextNode),endNode, listOfEntryPoints[count], stepsTravelled, History)
				count = count+1
				if count>10:    # Not more than 8 entries to a building.
					return [result[0], result[1], "dead", History]
				if result[2] == "alive":
					return [result[0], result[1], "alive", History]

#       if endingFile == "UICCampus":
#           if initialFile.split('-')[1]=='1':
#               nextNode = goingSomewhere(startNode,endNode, 0, 0)
#               return overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History) #getNodeToEnter(initialFile.split('-')[0])

		if len(initialFile.split('-')) == 1 or initialFile.split('-')[1]=='1':
			#print "XXXXXXXXXXXXXXXX"
			while True:
				nextNode = goingSomewhere(startNode,endNode, count, 0, basementSearch)
				result1 = simpleAStarSearch(startNode, nextNode[0])
				count = count + 1
				if result1 != "FAIL":
					break
			result = overallAStarSearch(result1, endNode, nextNode[1], stepsTravelled, History)   #getNodeToEnter(initialFile.split('-')[0])
			print result[0]
			
			if count>30:
				return [result[0], result[1], "dead", History]
			if result[2] == "alive":
				return [result[0], result[1], "alive", History]

		while True:
			if initialFile.split('-')[1]=='Basement':
					nextNode = goingSomewhere(startNode, endNode, count, 1, True)      # basementSearch better equal True
			else:
					nextNode = goingSomewhere(startNode, endNode, count, -1, basementSearch)
			#print "WHY?"
			result = overallAStarSearch(simpleAStarSearch(startNode, nextNode[0]), endNode, nextNode[1], stepsTravelled, History)

			count = count+1
			if count>30:
				return [result[0], result[1], "dead", History]
			if result[2] == "alive":
				return [result[0], result[1], "alive", History]
		
def getNodeToEnter(value):
	ImTiredpath = ""
	if isLive==True:
		ImTiredpath = "XML/UICCampusnumbermap.txt"
	else:
		ImTiredpath = "UICCampusnumbermap.txt"
	aFile = open(ImTiredpath)
	ALLines = aFile.readlines()
	for aline in ALLines:
		ithem = aline.split()
		if ithem[1]==value:
			return getNode(ithem[0])
		
		
def simpleAStarSearch(startNode, endNode):
	# Type corrections
	if type(startNode) == type("someString"):
		startNode = getNode(startNode)
	if type(endNode) == type("someString"):
		endNode = getNode(endNode)

	# Return a list with only "startNode" if startNode and endNode are equivalent
	if getNodeId(startNode) == getNodeId(endNode):
		return [ 0, [startNode] ]

	closedSet = []
	openSet = [ startNode ]
	g_score = {}
	g_score[startNode] = [0, [startNode]]
	while len(openSet) > 0:
		BrickOfHope = sorted(openSet, key=lambda(k): getDistanceBetweenNodes(k, endNode)+g_score[k][0])
		x = BrickOfHope[0]
		#print "Open Set"
		#for unnode in BrickOfHope:
		#	print getNodeId(unnode),
		#print "" #LOL

		if getNodeId(x) == getNodeId(endNode):
			return g_score[x]
		
		closedSet.append(x)
		openSet.remove(x)

		if x != startNode and x != endNode and getNodeType(x) == "transition":
			continue

		adjacentNodes = getAdjacentNodes( x )

		for node in adjacentNodes:
			if getNodeType(node) != "transition" or True:
				
				TriforceOfWisdom = 1
				TriforceOfCourage = 1
				for danger in closedSet:
					if getNodeId(danger) == getNodeId(node):
						TriforceOfWisdom = 0
				for peril in openSet:
					if getNodeId(peril) == getNodeId(node):
						TriforceOfCourage = 0
				if TriforceOfCourage:
					if TriforceOfWisdom:
						openSet.append(node)

				#if not (node in closedSet):
					#if not (node in openSet):
				#if closedSet.count(node) == 0:
					#if openSet.count(node) == 0:

				if getNodeType(node) == "room" and getNodeId(node)!="The Quad":
					g_score[node] = [g_score[x][0] + 4*getDistanceBetweenNodes(x, node), g_score[x][1]+[node]]
				else:
					g_score[node] = [g_score[x][0] + getDistanceBetweenNodes(x, node), g_score[x][1]+[node]]

	return "FAIL"
