#!/usr/bin/python3

import sys
import json
import datetime

#word="aircraft carrier"
#k = 100
'''
if(sys.argv[1] and sys.argv[2]):
	word = sys.argv[1]
	k = float(sys.argv[2])
'''
if(sys.argv[1] and sys.argv[2]):
	word = sys.argv[1]
	k = float(sys.argv[2])
	
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

def eucledian_dist(arr):
	dist = pow( (pow(arr[0][0],2) + pow(arr[1][0],2)) , 0.5)
	return dist

for line in sys.stdin:
		j=json.loads(line)
		drawing = j["drawing"]
		if(isnotbad(j)):
			if(j["word"]==word): #check to see if its the word we want
				dist = eucledian_dist(drawing[0])
				if(dist > k):
					print("%s\t%d" %(j["countrycode"], 1))


