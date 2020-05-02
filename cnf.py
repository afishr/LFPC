import copy

# TERMINAL = ['S', 'A', 'B', 'C', 'E']
# NONTERMINAL = ['a', 'd']

INPUT_FILES = [
	'cnf_input_1.txt',
	'cnf_input_2.txt'
]
INPUT = open(INPUT_FILES[0], 'r').read().split('\n')
EPS = '_'

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
			if key == epsKey:
				continue
			
			for i, el in enumerate(localRules[key]):
				if epsKey in el:
					woEps = el.replace(epsKey, '')

					if epsKey in localRules:
						if woEps:
							localRules[key].append(woEps)
					else:
						if len(localRules[key][i]) == 1:
							localRules[key].remove(epsKey)
						else:
							localRules[key][i] = woEps
			
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

	counter = 1
	while counter:
		for key in localRules:
			if key in productives:
				continue

			for el in localRules[key]:
				for letter in el:
					if (letter in productives):
						productives.add(key)
						counter += 1
		
		counter -= 1

	for key in list(localRules):
		if key not in productives:
			del localRules[key]

			for innerKey in list(localRules):
				for el in localRules[innerKey]:
					if key in el:
						localRules[innerKey].remove(el)

	return localRules
	

rules = readRules(INPUT)

# _printRules(rules)

rules = removeEpsilon(rules)
rules = removeRenamings(rules)
rules = removeInaccessibles(rules)
rules = removeNonproductives(rules)
_printRules(rules)

