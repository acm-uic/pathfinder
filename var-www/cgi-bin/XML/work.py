import sys, os, re, xml.dom.minidom, subprocess


def withinTolerance(valueNumberOne, valueNumberTwo):
    #print (valueNumberOne, valueNumberTwo), str(valueNumberOne-valueNumberTwo), (abs(valueNumberOne-valueNumberTwo)<10)
    return (abs(valueNumberOne-valueNumberTwo)<8)
    

matchString = '[(]-?[0-9]+[.]?[0-9]* -?[0-9]+[.]?[0-9]* -?[0-9]+[.]?[0-9]* -?[0-9]+[.]?[0-9]*'
def find(searchedString):
    theMatched = re.search(matchString, searchedString)
    
    return searchedString[theMatched.span()[1]:searchedString[theMatched.span()[1]:].find(")")+theMatched.span()[1]].split(" ")[1:]

def createNode(myType, room):
	node = xmlDocument.createElement("node")
	id = xmlDocument.createElement("id")
	idText = xmlDocument.createTextNode(room[1])
	id.appendChild(idText)
	node.appendChild(id)
	type = xmlDocument.createElement("type")
	typeText = xmlDocument.createTextNode(myType)
	type.appendChild(typeText)
	node.appendChild(type)
	coordinate= xmlDocument.createElement("coordinate")
	xcoord = xmlDocument.createElement("x")
	xcoordtext = xmlDocument.createTextNode( str(float(room[0][0])-5 ) )
	xcoord.appendChild(xcoordtext)
	ycoord = xmlDocument.createElement("y")
	ycoordtext = xmlDocument.createTextNode( str(float(room[0][1])-5 ) )
	ycoord.appendChild(ycoordtext)
	coordinate.appendChild(xcoord)
	coordinate.appendChild(ycoord)
	node.appendChild(coordinate)
	connects = xmlDocument.createElement("connects")
	node.appendChild(connects)
	xmlFile.appendChild(node)
	


#def find(svgLine):
#    startPos = svgLine.find('"matrix(%f %f %f %f ') + 17
#    endPos = startPos + svgLine[startPos:].find(')')
#    string = svgLine[startPos:endPos]
#    
#    return string.split(" ")

#a = raw_input("Enter the name of the map (no .svg): ")
#print a
#print sys.path
#print os.path
#.strip("\\Source Code\\XMLCreation")
#listing.txt
newInputFile = sys.path[0][:-24] + "/Images/SVGs/"
#filelisting = open(newInputFile + a + ".svg", "r")
filelisting = open("listing.txt", "r")
outputFile = open("output.txt", "w")
#findall

#theMatched = re.search(matchString, searchedString)
#searchedString[theMatched.span()[1]:searchedString[theMatched.span()[1]:].find(")")+theMatched.span()[1]]

RoomNum = 0
HallNum = 0
TransNum = 0
SegNum = 0

fileNames = filelisting.readlines()[:-1] # I put an empty line at the end of the script
filelisting.close()

rangeFile = open("ranges.txt", "w")

for fileName in fileNames:
    
	Rooms 		= []        # Cities
	Hallways 	= []       	# Counties
	Transfers 	= []      	# Towns
	Segments 	= []		# Line Segments

	xmlDocument = xml.dom.minidom.Document()
	xmlFile = xmlDocument.createElement("file")
	#xmlFileAttribute = xmlDocument.createAttribute( fileName[:-2] )
	xmlFile.setAttribute("name", fileName[:-2])
	#xmlFile.setAttributeNode(xmlFileAttribute)
	xmlDocument.appendChild(xmlFile)
	conversion = xmlDocument.createElement("conversion")
	conversionText = xmlDocument.createTextNode("42.42")
	conversion.appendChild(conversionText)
	xmlFile.appendChild(conversion) 

	svgFile = open(newInputFile +fileName[:-2]+".svg", "r")
	svgLines = svgFile.readlines()
	svgFile.close()

	xmlOutputFile = open(fileName[:-2]+".xml", "w")
	
	foundCapitolFlag = 0
	for svgLine in svgLines:
		if svgLine.find('<use xlink:href="#Capitol"') >= 0:
			foundCapitolFlag = 1
			
		if foundCapitolFlag == 1:
#			print svgLine
			if svgLine.find('<use xlink:href="#City') >= 0:
				pos = find(svgLine)
				Rooms.append([pos, "R"+str(RoomNum)])
				RoomNum+=1
			if svgLine.find('<use xlink:href="#County_Seat') >= 0:
				pos = find(svgLine)
				Hallways.append([pos, "H"+str(HallNum)])
				HallNum+=1
			if svgLine.find('<use xlink:href="#Town') >= 0:
				pos = find(svgLine)
				Transfers.append([pos, "T"+str(TransNum)])
				TransNum+=1
			if svgLine.find('<line fill=') >= 0:
				xPos1Start	= svgLine.find('x1="') + 4
				xPos1End 	= svgLine.find('" y1="')
				yPos1Start	= svgLine.find('y1="') + 4
				yPos1End	= svgLine.find('" x2="')
				xPos2Start	= svgLine.find('x2="') + 4
				xPos2End	= svgLine.find('" y2="')
				yPos2Start	= svgLine.find('y2="') + 4
				yPos2End	= svgLine.find('"/>')
				
				segmentPositionX1 = svgLine[xPos1Start:xPos1End]
				segmentPositionY1 = svgLine[yPos1Start:yPos1End]
				segmentPositionX2 = svgLine[xPos2Start:xPos2End]
				segmentPositionY2 = svgLine[yPos2Start:yPos2End]
				
				segment = [segmentPositionX1, segmentPositionY1, segmentPositionX2, segmentPositionY2]
				Segments.append([segment, "L"+str(SegNum)])
				SegNum+=1

	# Sorry about linear search
        for index, item in enumerate(Segments):
#            print item
            x1, y1, x2, y2 = item[0]
            x1 = float(x1)
            x2 = float(x2)
            y1 = float(y1)            
            y2 = float(y2)
            newName1 = ""
            newName2 = ""
            point1Found = 0
            point2Found = 0
            if not (point1Found and point2Found):
                for anotherList in Rooms:
                    room = anotherList[0]
                    aX = float(room[0])-5
                    aY = float(room[1])-5
                    #print "Comaparing " + str(item[0]) + " " + str(aX) + " " + str(aY)
                    if withinTolerance(x1, aX) and withinTolerance(y1, aY):
                        point1Found = 1
                        newName1 = anotherList[1]
                    #    print "Match! 1R"
                    if withinTolerance(x2, aX) and withinTolerance(y2, aY):
                        point2Found = 1
                        newName2 = anotherList[1]
                    #    print "Match! 2R"
                        
                for anotherList in Hallways:
                    room = anotherList[0]
                    aX = float(room[0])-5
                    aY = float(room[1])-5
                    #print "Comparing " + str(item[0]) + " " + str(aX) + " " + str(aY)                    
                    if withinTolerance(x1, aX) and withinTolerance(y1, aY):
                        point1Found = 1
                        newName1 = anotherList[1]
                    #    print "Match! 1H"
                    if withinTolerance(x2, aX) and withinTolerance(y2, aY):
                        point2Found = 1
                        newName2 = anotherList[1]
                    #    print "Match! 2H"


                for anotherList in Transfers:
                    room = anotherList[0]
                    aX = float(room[0])-5
                    aY = float(room[1])-5                
#                    print "Comparing" + str(item[0]) + " " + str(aX) + " " + str(aY)
                    if withinTolerance(x1, aX) and withinTolerance(y1, aY):
                        point1Found = 1
                        newName1 = anotherList[1]
#                        print "Match! 1T"                        
                    if withinTolerance(x2, aX) and withinTolerance(y2, aY):
                        point2Found = 1
                        newName2 = anotherList[1]
#                        print "Match! 2T"
            if not (point1Found and point2Found):
                print "Points not found for" 
                print item
                item.append([newName1, newName2])
                Segments[index] = item
            else:
                item.append([newName1, newName2])
                Segments[index] = item
                
	# Write the ranges file
	if Rooms == []:
		print "No rooms in file " + fileName[:-1]
		rangeFile.write(fileName[:-2] + " X X ")
	else:
		rangeFile.write(fileName[:-2] + " " + (Rooms[0][1][1:]) + " " + (Rooms[-1][1][1:]) + " ")
	if Hallways == []:
		print "No hallways in file " + fileName[:-2]
		rangeFile.write( "X X " )
	else:
		rangeFile.write( (Hallways[0][1][1:]) + " " + (Hallways[-1][1][1:]) + " ")
	if Transfers == []:
		print "No transfers in file " + fileName[:-2]
		rangeFile.write( "X X")
	else:
		rangeFile.write( (Transfers[0][1][1:]) + " " + (Transfers[-1][1][1:]) )
	
	rangeFile.write("\n")

	# Output File
	outputFile.write("File: " + fileName[:-2] + "\n")

	outputFile.write("Rooms:\n")
	for room in Rooms:
		outputFile.write("\t " + room[1] + ": "  + str(float(room[0][0])-5) + " " + str(float(room[0][1])-5) + "\n")
		createNode("room", room)	

	outputFile.write("Hallways:\n")
	for hallway in Hallways:
		outputFile.write("\t " + hallway[1] + ": "  + str(float(hallway[0][0])-5) + " " + str(float(hallway[0][1])-5) + "\n")
		createNode("hallway", hallway)

	outputFile.write("Transfers:\n")
	for transfer in Transfers:
		outputFile.write("\t " + transfer[1] + ": "  + str(float(transfer[0][0])-5) + " " + str(float(transfer[0][1])-5) + "\n")
		createNode("transition", transfer)        

	outputFile.write("Segments:\n")
	for seg in Segments:
		outputFile.write("\t " + seg[1] + ": " + str(float(seg[0][0])-5) + " " + str(float(seg[0][1])-5) + " "
                                 + str(float(seg[0][2])-5) + " " + str(float(seg[0][3])-5) + "\n\t\tConnects: "
                                 + seg[2][0] + " and " + seg[2][1] + "\n")
	
		for node in xmlDocument.getElementsByTagName("node"):
			if node.firstChild.firstChild.nodeValue == seg[2][0]:
				connection = xmlDocument.createElement("connection")
				connectsText = xmlDocument.createTextNode(seg[2][1])
				connection.appendChild(connectsText)
				node.lastChild.appendChild(connection)
			
			if node.firstChild.firstChild.nodeValue == seg[2][1]:
				connection = xmlDocument.createElement("connection")
				connectsText = xmlDocument.createTextNode(seg[2][0])
				connection.appendChild(connectsText)
				node.lastChild.appendChild(connection)
				
	xmlFileText = xmlDocument.toxml()
	xmlOutputFile.write(xmlFileText)
	xmlOutputFile.close()
	#subprocess.call(["tidy", "-xml", "-i", "-q", "-o", fileName[:-2] + ".xml", fileName[:-2] + ".xml"])

outputFile.close()
rangeFile.close()	
