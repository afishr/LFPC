import copy
import string

INPUT_FILES = [
	'cnf_input_1.txt',
	'cnf_input_2.txt'
]
INPUT = open(INPUT_FILES[0], 'r').read().split('\n')
EPS = 'ε'

def _powerset(seq):
	"""
	Returns all the subsets of this set. This is a generator.
	"""

	if len(seq) <= 1:
		yield seq
		yield []
	else:
		for item in _powerset(seq[1:]):
			yield [seq[0]]+item
			yield item

def _replace(str, subStr, mask):
	result = []
	for m in mask:
		modified = str
		pos = 1
		for i in m:
			for _ in range(i):
				pos = modified.find(subStr, pos-i)
			
			modified = modified[:pos] + modified[pos+1:]
		result.append(modified)
	return result

def _printRules(rules):
	for key in rules:
		print(key, '->', rules[key])
	print('-------------------------')
  
def _haveEpsilon(rules):
	for key in rules:
		for el in rules[key]:
			if el == EPS:
				return True, key
	
	return False, None

def _haveRenaming(key, rules):
	for el in rules[key]:
		if ( len(el) == 1 ) and (el in rules):
			return True, el

	return False, None

def _removeRenaming(key, initialValue, rules):
	haveRenaming, value = _haveRenaming(initialValue, rules)

	if haveRenaming:
		rules = _removeRenaming(initialValue, value, rules)
	
	rules[key].remove(initialValue)
	rules[key] = rules[key] + rules[initialValue]

	return rules	

def _containsTerminal(str):
	for letter in str:
		if letter in string.ascii_lowercase:
			return True
	return False

def _containsNonterminal(str, rules):
	for letter in str:
		if letter in rules:
			return True
	return False

def _generateSymbol(pos, rules):
	#FIXME: Function can't handle situation when all letters in alphabet are used

	letters = string.ascii_uppercase

	while letters[pos] in rules:
		pos -= 1
	
	return letters[pos], pos

def readRules(inputArr, separator='->'):
	res = {}
	for el in inputArr:
		x = el.split(separator)

		if not x[0] in res:
			res[x[0]] = []
		
		res[x[0]].append(x[1])

	return res

def removeEpsilon(rules):
	localRules = copy.deepcopy(rules)

	haveEpsilon, epsKey = _haveEpsilon(localRules)

	while haveEpsilon:
		localRules[epsKey].remove(EPS)
		if len(localRules[epsKey]) == 0:
			del localRules[epsKey]

		for key in localRules:
			for i, el in enumerate(localRules[key]):
				if epsKey in el:
					if epsKey in localRules:
						# Count how many times the epsKey is found in production
						count = el.count(epsKey)
						# Generate list with elements from 1 to previously counted value
						#FIXME: Should generete here array with indexes of occurences
						# instead of dummy array from 1 to count of occurences
						arr = [i for i in range(1, count + 1)] 
						# Generate all subsets of previous list. This subsets mean the mask by which epsKey will be excluded. 
						# E.g., mask [1, 2] means that 1st and 2nd occurences of epsKey in production will be excluded.
						subSets = [x for x in _powerset(arr)]
						# _replace() get as one of the parameters a list of such masks and returns a list of productions that will be appended to existings
						# Here I make a slice of list w/o last element, because last element is always a prodcution that contains all epsKey,
						# but such production already is present, in fact this is the original one that we pass as parameter to _replace()
						toAdd = _replace(el, epsKey, subSets)[:-1]
						# Reverse the list just for just for aesthetics
						toAdd.reverse()
						localRules[key] = localRules[key] + toAdd
					else:
						if len(localRules[key][i]) == 1:
							localRules[key].remove(epsKey)
						else:
							localRules[key][i] = el.replace(epsKey, '')
			
		haveEpsilon, epsKey = _haveEpsilon(localRules)
	return localRules

def removeRenamings(rules):
	localRules = copy.deepcopy(rules)
	for key in localRules:
		haveRenaming, val = _haveRenaming(key, localRules)
		if haveRenaming:
			localRules = _removeRenaming(key, val, localRules)
	
	return localRules

def removeInaccessibles(rules):
	localRules = copy.deepcopy(rules)
	accessedKeys = set()

	for key in localRules:
		for el in localRules[key]:
			for letter in el:
				if (letter in localRules):
					accessedKeys.add(letter)

	for key in list(localRules):
		if key not in accessedKeys:
			del localRules[key]

	return localRules

def removeNonproductives(rules):
	localRules = copy.deepcopy(rules)

	productives = set()

	for key in localRules:
		for el in localRules[key]:
			if ( len(el) == 1 ) and (el not in localRules):
				productives.add(key)

	callStack = 1
	while callStack:
		for key in localRules:
			if key in productives:
				continue

			for el in localRules[key]:
				for letter in el:
					# FIXME: Should check if all nonterminals in production are productione 
					# in other way, if first nonterm. is productive and others not the key
					# anyway gets in productives set()
					if (letter in productives):
						productives.add(key)
						callStack += 1
		
		callStack -= 1

	for key in list(localRules):
		if key not in productives:
			del localRules[key]

			for innerKey in list(localRules):
				for el in localRules[innerKey]:
					if key in el:
						localRules[innerKey].remove(el)

	return localRules
	
def normalize(rules):
	localRules = copy.deepcopy(rules)

	cache = {}
	terminals = string.ascii_lowercase
	lettersCounter = len(string.ascii_uppercase) - 1


	# Normalize wave #1: Change productions that have more than 2 symbols
	callStack = 1
	while callStack:
		for key in list(localRules):
			for i, el in enumerate(localRules[key]):
				if len(el) > 2:
					if el in cache:
						localRules[key][i] = cache[el]
					else:
						symbol, lettersCounter = _generateSymbol(lettersCounter, localRules)
						cache[el] = symbol + el[len(el)-1]

						localRules[symbol] = [el[:len(el)-1]]
						localRules[key][i] = cache[el]

						callStack += 1
	
		callStack -= 1

	# Normalize wave #2: Change productions that have more than one noneterminal symbols with terminals
	for key in list(localRules):
		for i, el in enumerate(localRules[key]):
			if len(el) == 2 and _containsTerminal(el):
				if el in cache:
					localRules[key][i] = cache[el]
				else:
					for letter in el:
						if letter in terminals:
							if letter in cache:
								localRules[key][i] = localRules[key][i].replace(letter, cache[letter])
							else:
								symbol, lettersCounter = _generateSymbol(lettersCounter, localRules)
								cache[letter] = symbol
								localRules[ cache[letter] ] = [letter]
								localRules[key][i] = localRules[key][i].replace(letter, cache[letter])
					cache[el] = localRules[key][i]

	return localRules					

rules = readRules(INPUT)
# print('INITIAL')
_printRules(rules)

rules = removeEpsilon(rules)
# print('REMOVE EPSILON')
# _printRules(rules)

rules = removeRenamings(rules)
# print('REMOVE RENAMINGS')
# _printRules(rules)

rules = removeInaccessibles(rules)
# print('REMOVE INACCESSIBLES')
# _printRules(rules)

rules = removeNonproductives(rules)
# print('REMOVE NONPRODUCTIVE')
# _printRules(rules)

rules = normalize(rules)
# print('NORMALIZE')
_printRules(rules)