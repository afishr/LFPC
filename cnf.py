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
  
def readRules(rules, separator='->'):
	res = {}
	for rule in rules:
		x = rule.split(separator)

		if not x[0] in res:
			res[x[0]] = []
		
		res[x[0]].append(x[1])

	return res

print( readRules(INPUT) )