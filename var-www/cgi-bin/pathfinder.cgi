#!/usr/bin/env python2
import sys

from traceback import *

# Import the CGI module
import cgi, os

sys.path.append(os.getcwd() + "/XML")
import pathfinding, pathfindingWrapper

#FOR DEBUG, UNCOMMENT THIS LINE
#sys.stderr = sys.stdout

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

def generate_head():
        print r'<html>'
        print r'<head>'
        print r'<title> UIC Mega Path Finder </title>'
        print r'<link rel="stylesheet" type="text/css" href="../umpf/Style.css" />'
        print r'</head>'
        print r'<body>'
        print r'<script>'
        print r'function changeMaps()'
        print r'{'
        print r'var btnSubmitTags = document.getElementById( "changeMapButton" );'
        print r'btnSubmitTags.click();'
        print r'}'
        print r'</script>'
        print r'<div id="head"></div>'
        print r'<div id="headRight"></div>'
        print r'<div id="left">'
        print r'<div class="padding2"></div>'
        print r'<ul>'
        print r'<li><a class="nav" href="./pathfinder.cgi" title="Pathfinder">Pathfinder</a></li>'
        print r'<li><a class="nav" href="../umpf/about.html" title="About">About</a></li>'
        print r'<li><a class="nav" href="../umpf/faqs.html" title="Frequently Asked Questions">FAQs</a></li>'
        print r'</ul>'
        print r'</div>'
        print r'<div id="content">'
        print r'<div class="padding2"></div>'

def generate_tail():
        #print r'<div class="padding2"></div>'
        #print r'<div class="padding2"></div>'
        print r'</div>'
        print r'</body>'
        print r'</html>'

def generate_images(shouldShowImages, imageFileNames):
        #TODO: We need to figure out how many images we need to display :-)
        if shouldShowImages == True:
                for imageFileName in imageFileNames:
                        #We need to remove a "html/" from the string
                        imageFileName = str(imageFileName)
                        imageFileName = imageFileName.replace("html/", "")

                        print r'<p>'
                        print r'<a href="' + imageFileName + '">'
                        print r'<img style="width:792;height=612;" src="' + imageFileName + '"/>'
                        print r'</a>'
                        print r'</p>'


def generate_building_list(selectionName, mapToCheck):
        print r'<select onchange="changeMaps();" name="' + selectionName + '">'

        #Print out all the files
        file = open("XML/listing.txt", "r")
        lines = file.readlines()
        previousBuilding = "Guinevere"
        for line in lines:
                line = line[:-2]
                if previousBuilding != line.split('-')[0]:
                        #Special case for The Quad
                        if line == "UICCampus":
                                line = "The Quad"

                        if line.split('-')[0] == mapToCheck:
                                print r'<option selected>' + line.split('-')[0] + r'</option>'
                        else:
                                print r'<option>' + line.split('-')[0] + r'</option>'
                        previousBuilding = line.split('-')[0]
        file.close()

        print r'</select>'


# Define function to generate HTML form.
def generate_form(map1, map2, room1, room2, shouldShowImages, imageFileNames):

        generate_head()

        print r'<form method=post action="pathfinder.cgi">'
        print r'<input type=hidden name="action" value="changebuilding">'
        print r'<table border="0" cellspacing="3" cellpadding="3">'
        print r'<tr>'
        print r'<td VALIGN=TOP>'
        print r'<table border="0" cellspacing="3" cellpadding="3">'
        print r'<tr>'
        print r'<td>'
        print r'Building 1:'
        print r'</td>'
        print r'<td>'
        print r'Building 2:'
        print r'</td>'
        print r'</tr>'
        print r'<tr>'
        print r'<td>'
        generate_building_list("building1", map1)
        print r'</td>'
        print r'<td>'
        generate_building_list("building2", map2)
        print r'</td>'
        print r'</tr>'
        print r'<input id="changeMapButton" name="changebuilding" style="visibility:hidden" type="submit" value="Change!">'
        print r'<tr>'
        print r'<td>'
        if map1 != "The Quad":
                print r'Building 1 Rooms:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        print r'</td>'
        print r'<td>'
        if map2 != "The Quad":
                print r'Building 2 Rooms:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        print r'</td>'
        print r'</tr>'
        print r'<tr>'
        print r'<td>'
        printRoomOptions(1, room1, map1)
        print r'</td>'
        print r'<td>'
        printRoomOptions(2, room2, map2)
        print r'</td>'
        print r'<td>'
        print r'<input type="submit" id="changeroom" name="changeroom" value="Path!">'
        print r'</td>'
        print r'</tr>'
        print r'</table>'
        print r'<td>'
        print r'<p>'
        generate_images(shouldShowImages, imageFileNames)
        print r'</p>'
        print r'</td>'
        print r'</tr>'
        print r'</table>'
        print r'</form>'
        generate_tail()

def printRoomOptions(roomNumber, roomSelected, currentRoom):

        if currentRoom == "The Quad":
                return

        if roomNumber == 1:
                print r'<select  name="room1">'
        elif roomNumber == 2:
                print r'<select  name="room2">'
        else:
                print r'<h1>ERROR!</h1>'

        file = open("XML/ranges.txt", "r")
        lines = file.readlines()
        roomNamesList = []
        for line in lines:
                items = line.split()
                if currentRoom == items[0].split('-')[0]:
                        if items[1] != "X":
                                if currentRoom != "The Quad":
                                        for num in range( int(items[1]), int(items[2])+1 ):
                                                res = pathfinding.getRoomNameForNode("R" + str(num) )
                                                if res == roomSelected:
                                                        roomNamesList.append("<option selected>" + res + r'</option>')
                                                else:
                                                        roomNamesList.append("<option>" + res + r'</option>')
                                        #for num in range( int(items[5]), int(items[6])+1 ):
                                        #       res = "T" + str(num)
                                        #       if res == roomSelected:
                                        #               roomNamesList.append("<option selected>" + res + r'</option>')
                                        #       else:
                                        #               roomNamesList.append("<option>" + res + r'</option>')

                                #else:
                                #       if roomSelected == "The Quad":
                                #               roomNamesList.append("<option selected>The Quad")
                                #       else:
                                #               roomNamesList.append("<option>The Quad")
                                #       for num in range( int(items[5]), int(items[6])+1 ):
                                #               res = pathfinding.getRoomNameForNode("T" + str(num) )
                                #               if res == roomSelected:
                                #                       roomNamesList.append("<option selected>" + res + r'</option>')
                                #               else:
                                #                       roomNamesList.append("<option>" + res + r'</option>')
                        #elif items[4] != "X":
                        #       for num in range( int(items[5]), int(items[6])+1):
                        #               res= pathfinding.getRoomNameForNode("T" + str(num) )
                        #               if res == roomSelected:
                        #                       roomNamesList.append("<option selected>" + res + r'</option>')
                        #               else:
                        #                       roomNamesList.append("<option>" + res + r'</option>')
                                else:
                                        return
        roomNamesList.append("<option>" + "  " + r"</option>")
        roomNamesList.sort()
        for roomName in roomNamesList:
                print roomName
        file.close()
        print r'</select>'


    # Define main function.
def main():
        room1 = "NONE"
        room2 = "NONE"
        map1 = "Unknown"
        map2 = "Unknown"
        imageFileNames = ""
        form = cgi.FieldStorage()

        #print "<!-- " + str(form) + " -->"

        if (form.has_key("action") and form.has_key("changebuilding")):
                #Do functionality for changing the room
                map1 = form["building1"].value
                map2 = form["building2"].value
                if form.has_key("room1"):
                        room1 = form["room1"].value
                if form.has_key("room2"):
                        room2 = form["room2"].value

                #For now, we'll not show any images :-)
                shouldShowImages = False

        elif (form.has_key("action") and form.has_key("changeroom")):
                #Do functionality for changing the path
                map1 = form["building1"].value
                map2 = form["building2"].value

                if map1 != "The Quad":
                        if form.has_key("room1"):
                                room1 = form["room1"].value
                        else:
                                room1 = "  "
                else:
                        room1 = "The Quad"

                if map2 != "The Quad":
                        if form.has_key("room2"):
                                room2 = form["room2"].value
                        else:
                                room2 = "  "
                else:
                        room2 = "The Quad"

                if room1 == "  ":
                        room1 = pathfinding.getNodeId(pathfinding.getNodeToEnter(map1))
                else:
                        room1 = pathfinding.getNodeId(pathfinding.getNodeFromRoomName(room1))
                if room2 == "  ":
                        room2 = pathfinding.getNodeId(pathfinding.getNodeToEnter(map2))
                else:
                        room2 = pathfinding.getNodeId(pathfinding.getNodeFromRoomName(room2))



                shouldShowImages = True

                try:
                        imageFileNames = pathfinding.drawResults( pathfindingWrapper.AStarSearch(room1, room2) )
                except:
                        print r'<html>'
                        print r'<head>'
                        print r'<title>UMPF - Error Occurred</title>'
                        print r'</head>'
                        print r'<body>'
                        print r'<p>'
                        print r'<b>An error occurred somewhere.</b></p>'
                        print r'<p>'
                        print r"Whatever caused it, it's logged and some guys will fix it.<br>"
                        print r"I can't really tell you right now what's causing it because I'm just a computer.<br>"
                        print r'Here I am, the brain the size of a planet and they have me calculating paths.<br>'
                        print r'You call this job satisfaction?<br>'
                        print r"Because I don't."
                        print r'</p>'
                        print r'<p>'
                        print r'Oh yea, you probably want to hit the Back button at this point.'
                        print r'</p>'
                        print r'</body>'
                        print r'</html>'
                        sys.exit()

                if map1 != "The Quad":
                        if form.has_key("room1"):
                                room1 = form["room1"].value
                        else:
                                room1 = "  "
                else:
                        room1 = "The Quad"

                if map2 != "The Quad":
                        if form.has_key("room2"):
                                room2 = form["room2"].value
                        else:
                                room2 = "  "
                else:
                        room2 = "The Quad"

                map1 = form["building1"].value
                map2 = form["building2"].value

        else:
                map1 = "The Quad"
                map2 = "The Quad"
                room1 = "  "
                room2 = "  "
                imageFileNames = pathfinding.drawResults( pathfindingWrapper.AStarSearch( pathfinding.getNodeId("The Quad") , pathfinding.getNodeId("The Quad") ) )
                shouldShowImages = True

        generate_form(map1, map2, room1, room2, shouldShowImages,imageFileNames)

# Call main function.
main()
