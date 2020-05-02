TERMINAL = ['S', 'A', 'B', 'C', 'E']
NONTERMINAL = ['a', 'd']

INPUT = [
	'S->dB',
	'S->A',
	'A->d',
	'A->dS',
	'A->aAdAB',
	'B->aC',
	'B->aS',
	'B->AC',
	'C->_',
	'E->AS'
]

EPS = '_'
  
def readRules(inputArr, separator='->'):
	res = {}
	for el in inputArr:
		x = el.split(separator)

		if not x[0] in res:
			res[x[0]] = []
		
		res[x[0]].append(x[1])

	return res

def _haveEpsilon(rules):
	for key in rules:
		for el in rules[key]:
			if el == EPS:
				return True, key
	
	return False, None

def removeEpsilon(rules):
	haveEpsilon, epsKey = _haveEpsilon(rules)

	while haveEpsilon:
		rules[epsKey].remove(EPS)
		if len(rules[epsKey]) == 0:
			del rules[epsKey]

		for key in rules:
			if key == epsKey:
				continue
			
			for i, el in enumerate(rules[key]):
				if epsKey in el:
					woEps = el.replace(epsKey, '')

					if epsKey in rules:
						if woEps:
							rules[key].append(woEps)
					else:
						if len(rules[key][i]) == 1:
							rules[key].remove(epsKey)
						else:
							rules[key][i] = woEps
			
		haveEpsilon, epsKey = _haveEpsilon(rules)
	
	return rules

def _haveRenaming(key, rules):
	for el in rules[key]:
		if ( len(el) == 1 ) and (el in rules):
			return True, el

	return False, None

def _removeRenaming(key, initialValue, rules):
	haveRenaming, value = _haveRenaming(initialValue, rules)

	if haveRenaming:
		_removeRenaming(initialValue, value, rules)
	
	rules[key].remove(initialValue)

	rules[key] = rules[key] + rules[initialValue]

	print(rules)
	

def removeRenamings(rules):
	for key in rules:
		haveRenaming, val = _haveRenaming(key, rules)
		if haveRenaming:
			_removeRenaming(key, val, rules)



rules = readRules(INPUT)
print(rules)

rules = removeEpsilon(rules)

removeRenamings(rules)
# print(rules)