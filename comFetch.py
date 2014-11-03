import urllib
import urllib.request
import urllib.parse
import re
import os
import sys
import time

def retrieveHtml(url):
	response = urllib.request.urlopen(url)
	html = response.read().decode('utf-8')
	response.close()
	return html
	
def searchComic(comicName):
	html=retrieveHtml("http://s.sfacg.com/?Key="+urllib.parse.quote(comicName))
	resultList = re.findall('<li><strong class="\w+"><a href="http:\/\/comic.sfacg.com\/HTML\/(\w+)" id="\w+" class="\w+">(.+)<\/a>', html) 

    # download each chapter
	count=0
	for result in resultList:
		print("%02d"%count+".  "+result[0]+"\t"+result[1])
		count+=1
	return resultList
	
def showComic(cmd):
	comicName=cmd[1]
	html=retrieveHtml("http://comic.sfacg.com/HTML/"+comicName)
	
	title=re.search('\<title\>(.+),',html).group(1).split(',')[0]
	chapterList = re.findall('\<li\>\<a\shref=\"\/HTML\/'+comicName+'\/([a-zA-Z0-9]+)\/"', html)
	print(title+"("+cmd[1]+") \n最新一話:"+chapterList[0]+"\n")
	chapterList.sort()
	count=0
	for chapter in chapterList:
		print(chapter,"  ",end='')
		count+=1
		if(count%10==0):
			print()
	print()

def getImgPathList(chapter, comicID):
	url = "http://comic.sfacg.com/Utility/%s/%s.js"%(comicID, chapter)
	html = retrieveHtml(url)
	imgPathList = re.findall('picAy\[(\d+)\] = "([^"]+)"', html)
	return imgPathList
	
def downComic(cmd):
	comicName=cmd[1]
	chapter=cmd[2]
	html=retrieveHtml("http://comic.sfacg.com/HTML/"+comicName+'/')
	title=re.search('\<title\>(.+),',html).group(1).split(',')[0]
	title=title.split('/')[0]
	if not os.path.exists('./'+title):
		os.makedirs('./'+title)
	comicID=re.search("var\scomicCounterID\s=\s(\d+);", html).group(1)
	if(chapter=='all'):
		chapterList = re.findall('\<li\>\<a\shref=\"\/HTML\/'+comicName+'\/([a-zA-Z0-9]+)\/"', html)
		print("共計%d個項目，確定要下載?(y/N)"%len(chapterList))
		line=sys.stdin.readline()
		if(not line.strip('\r\n')=='Y' and not line.strip('\r\n')=='y'):
			return
		chapterList.sort()
	elif(chapter==''):
		return
	else:
		chapterList=[chapter];
		
	for chapter in chapterList:
		if not os.path.exists('./'+title+'/'+chapter):
			os.makedirs('./'+title+'/'+chapter)
		readerFile=open('./'+title+'/'+chapter+'/'+title+'_'+chapter+'.html','w')
		imgPathList=getImgPathList(chapter, comicID)
		for imgNum, imgPath in imgPathList:
			imgType = imgPath[-4:]
			srcPath = "http://comic.sfacg.com"+imgPath
			imgNum = imgNum.rjust(3,"0")
			dstPath = './%s/%s/%s%s'%(title,chapter, imgNum, imgType)
			urllib.request.urlretrieve(srcPath, dstPath)
			readerFile.write('<img src="%s%s"><br />\n'%(imgNum, imgType))
			print('downloading to ... '+dstPath)
		readerFile.close()
		print("%s chapter %s Downloded."%(title,chapter))
	print("Request Done.")
	