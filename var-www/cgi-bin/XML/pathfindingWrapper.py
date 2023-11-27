import pathfinding, os, sys

isLive = True
DoIReadFromCache = True

def testAll(lowerBoundX = 0, upperBoundX = 435, lowerBoundY = 0, upperBoundY = 435): # tests all the rooms if no bound is specified
	#434 is the number of rooms we have.
	x = 0
	y = 0
	failureFile = "failures.txt"
	for a in range(lowerBoundX, upperBoundX):
		x = a
		try:
			for b in range(lowerBoundY, upperBoundY):  #includes a
				y = b
				result = pathfinding.overallAStarSearch(pathfinding.getNode("R"+str(a)), pathfinding.getNode("R"+str(b)), 0, 0, [])
				#print "Result ", result[0], " found."
				StrToWrite = str(result[0]) + "\n"
				for item in result[1]:
					StrToWrite = StrToWrite + pathfinding.getNodeId(item) + "\n" # to make it look nice.
				tempFile = open("Cache/" + "R"+str(a)+ "R"+str(b) + ".txt", "w")
				tempFile.write(StrToWrite)
				tempFile.close()
				sys.stdout.write(".")
		except:
			print "" #ROFL
			print "Failure: " + str(x) + " -> " + str(y)
			tempFile = open(failureFile, "a")
			tempFile.write(str(x) + " -> " + str(y) + "\n") 
			tempFile.close()
	print

def AStarSearch(startNode, endNode):
	if isLive:
		if DoIReadFromCache and os.path.isfile("../html/PNGCache/"+startNode+endNode+".txt"):
			fileToOpen = open("../html/PNGCache/"+startNode+endNode+".txt", "r")
			theString = fileToOpen.readlines()
			theNewString = ""
			for item in theString:
				theNewString = theNewString + item + " "
			theString = theNewString
			theString = theString.split()    #.replace(" ", "")
			result = [float(theString[0])]
			result2 = []
			for item in theString[1:]:
				result2.append(pathfinding.getNode(item))
			result.append(result2)
			return result
		else:
			result = pathfinding.overallAStarSearch(pathfinding.getNode(startNode), pathfinding.getNode(endNode), pathfinding.getNode(startNode), 0, [])
			StrToWrite = str(result[0]) + "\n"
			for item in result[1]:
				StrToWrite = StrToWrite + pathfinding.getNodeId(item) + "\n" # to make it look nice.
			tempFile = open("../html/PNGCache/" + startNode + endNode + ".txt", "w")
			tempFile.write(StrToWrite)
			tempFile.close()
			return result
	else:
		if DoIReadFromCache and os.path.isfile("PNGCache/"+startNode+endNode+".txt"):
			fileToOpen = open("PNGCache/"+startNode+endNode+".txt", "r")
			theString = fileToOpen.readlines()
			theNewString = ""
			for item in theString:
				theNewString = theNewString + item + ""
			theString = theNewString
			print theString
			theString = theString.split()    #.replace(" ", "")
			print theString
			result = [float(theString[0])]
			result2 = []
			for item in theString[1:-1]:
				result2.append(pathfinding.getNode(item))
			result.append(result2)
			return result
		else:
			result = pathfinding.overallAStarSearch(pathfinding.getNode(startNode), pathfinding.getNode(endNode), pathfinding.getNode(startNode), 0, [])
			StrToWrite = str(result[0]) + "\n"
			for item in result[1]:
				StrToWrite = StrToWrite + pathfinding.getNodeId(item) + "\n" # to make it look nice.
			tempFile = open("PNGCache/" + startNode + endNode + ".txt", "w")
			tempFile.write(StrToWrite)
			tempFile.close()
			return result	

#testAll()        
		
