import os
import time
import sys
import hashlib
from graphics import *

#Creates folders for different file types
def makeFolders(downloadDirectory, fileTypes):
    for fileType in fileTypes.keys():
        directory = downloadDirectory + "\\" + fileType
        
        if not os.path.exists(directory):
            os.mkdir(directory)

#Moves file to its proper folder and delete any duplicates
def moveFile(moveFile, downloadDirectory, fileTypes):
    #The file format is what is after the period in the file name
    if "." in moveFile:
        temp = moveFile.split(".")
        fileFormat = temp[-1] 
    else:
        return
    out = ""
    for fileType in fileTypes.keys():
        if fileFormat in fileTypes[fileType]:
            srcPath = downloadDirectory + "\\" + moveFile
            dstPath = downloadDirectory + "\\" + fileType + "\\" + moveFile
            #If the file doesn't have a duplicate in the new folder, move it
            if not os.path.isfile(dstPath):
                os.rename(srcPath, dstPath)
                out = (moveFile + " moved to: " + fileType)
            #If the file already exists with that name and has the same md5 sum
            elif os.path.isfile(dstPath) and \
                checkSum(srcPath) == checkSum(dstPath):
                os.remove(srcPath)
                out = ("removed " + srcPath)
        
    return out

#Get md5 checksum of a file. Chunk size is how much of the file to read at a time.
def checkSum(fileDir, chunkSize = 8192):
        md5 = hashlib.md5()
        f = open(fileDir)
        while True:
            chunk = f.read(chunkSize)
            #If the chunk is empty, reached end of file so stop
            if not chunk:
                break
            md5.update(chunk)
        f.close()
        return md5.hexdigest()

#check if button clicked
def inside(point, rectangle):
    """ Is point inside rectangle? """

    ll = rectangle.getP1()  # assume p1 is ll (lower left)
    ur = rectangle.getP2()  # assume p2 is ur (upper right)

    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

		
def main():

    #Dictionary contains file types as keys and lists of their corresponding file formats
    fileTypes = {}
    fileTypes["Images"] = ["jpg", "gif", "png", "jpeg", "bmp", "PNG"]
    fileTypes["Audio"] = ["mp3", "wav", "aiff", "flac", "aac"]
    fileTypes["Video"] = ["m4v", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", \
                          "MOV", "mp4"]
    fileTypes["Documents"] = ["doc", "docx", "txt", "ppt", "pptx", "pdf", "rtf"]
    fileTypes["Exe"] = ["exe"]
    fileTypes["Compressed"] = ["zip", "tar", "7", "rar"]
    fileTypes["Virtual_Machine_and_iso"] = ["vmdk", "ova", "iso"]

    
    #The second command line argument is the download directory
    downloadDirectory = r'C:\Users\Sol\Downloads'
    downloadFiles = os.listdir(downloadDirectory)
    makeFolders(downloadDirectory, fileTypes)
    oldlen = len(os.listdir(downloadDirectory))

    # display graphics
    win = GraphWin("My Circle", 500, 500)
    win.setBackground("white")

    #objects
    org = Text(Point(250,25),"ORGANIZE")
    button = Rectangle(Point(200,10), Point(300,40))
    button.draw(win)
    org.draw(win)

    cls = Text(Point(250,465),"CLOSE")
    clsRect = Rectangle(Point(150,450), Point(350,480))
    cls.draw(win)
    clsRect.draw(win)

    dirText = Text(Point(250,60),"Working directory: " + downloadDirectory)
    dirText.draw(win)
    
    
    while True:
        lst = []
        clickPoint = win.getMouse()
        if inside(clickPoint, button):
            for filename in downloadFiles:
                out = moveFile(filename, downloadDirectory, fileTypes)
                if out:
                    lst.append(out)
        count = 0    
        for i in range(len(lst)):
            txt = Text(Point(250, 100 + (20*i)),lst[i])
            txt.setStyle("italic")
            txt.setSize(8)
            time.sleep(.3)
            txt.draw(win)
            count = i

        time.sleep(.3)
        ter = Text(Point(250, 140 + (20*count)),"ALL FILES HAVE BEEN SORTED")
        ter.setFill("red")
        ter.setStyle("bold")
        ter.setSize(16)
        ter.draw(win)

        clickPoint = win.getMouse()
        if inside(clickPoint, clsRect):
            win.close()
        
        

main()
