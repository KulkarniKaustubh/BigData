#!/usr/bin/python

import sys
import json
import datetime

#word="aircraft carrier"
n=len(sys.argv)
word=""
for i in range(1,n):
        word+=" "+sys.argv[i]
word=word.strip()


def isnotbad(record):
	word = record["word"]
	code = record["countrycode"]
	recognised = record["recognized"]
	key_id = record["key_id"]
	drawing = record["drawing"]
	#word Contains alphabets and whitespaces only.
	for i in word:
		if(not(i.isalpha() or i==' ')):
			return False
	#countrycode Contains only two uppercase letters
	if(not(code.isupper() and len(code)==2)):
		return False
	#recognized Boolean value containing either "true" or "false"
	if(recognised != False and recognised != True):
		return False
	#key_id Numeric string containing 16 characters only
	if(not(len(key_id)==16 and key_id.isdigit())):
		return False
	#drawing Array containing n(>=1) strokes. Every stroke has exactly 2 arrays where each array repr
	""" This is a valid drawing array
	[
		[
			[119, 107, 76, 70, 49, 39, 60, 93], 
			[72, 41, 3, 0, 1, 5, 38, 70]
		], 
		[
			[207, 207, 210, 221, 238], 
			[74, 103, 114, 128, 135]
		]
	]
	"""
	if(len(drawing) >=1 ):
		for arr in drawing:
			if(len(arr) != 2):
				return False
	return True

for line in sys.stdin:
        j=json.loads(line)
        #checking if it is the word we are looking for
        if isnotbad(j)==True:
        
                if j["word"]==word:
                        # checking if word is recognized
                        if j["recognized"]==True:
                
                                print("%s\t%s" %(j["recognized"],1))
                        # have to check this to ignore bad records
                        elif j["recognized"]==False:
                        
                                date_1=j["timestamp"].split()[0]
                                # date as a list of integers [yyyy,mm,dd]
                                date_2=list(map(int,date_1.split("-")))
                                # checking if it is weekday -------> Mon: 0 and Sun: 6
                                if datetime.date(date_2[0],date_2[1],date_2[2]).weekday() >4:
                                        print("%s\t%s" %(j["recognized"],1))
          

