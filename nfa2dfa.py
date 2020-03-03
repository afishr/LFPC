import pandas as pd

rules = [ # Proper hardcode
	'A-a-B',
	'B-c-B',
	'B-b-C',
	'C-a-C',
	'A-a-A',
	'B-a-A'
]

def getNFA(rules):
	nfa = {}
	for rule in rules:
		x = rule.split('-')

		if not x[0] in nfa:
			nfa[x[0]] = {}
		
		if not x[1] in nfa[x[0]]:
			nfa[x[0]][x[1]] = ''
		
		nfa[x[0]][x[1]] += x[2]
	return nfa

def getStates(nfa):
	states = []
	for x in nfa:
		states.append(x)

	for x in nfa:
		for y in nfa[x]:
			if len(nfa[x][y]) > 1:
				if not nfa[x][y] in states:
					states.append(nfa[x][y])
			else:
				if not nfa[x][y][0] in states:
					states.append(nfa[x][y][0])
	return states

def getMethods(nfa):
	methods = []

	for x in nfa:
		for j in nfa[x]:
			if not j in methods:
				methods.append(j)

	return methods

def convertNFA2DFA(nfa, states, methods):
	dfa = nfa
	for s in states:
		if not s in dfa:
			separated = list(s)
			for m in methods:
				temp = []
				for sp in separated:
					if m in dfa[sp]:
						temp.append(dfa[sp][m])
				if not s in dfa:
					dfa[s] = {}
				dfa[s][m] = max(temp, key=len)
	return dfa

nfa = getNFA(rules)
states = getStates(nfa)
methods = getMethods(nfa)
dfa = convertNFA2DFA(nfa, states, methods)

df = pd.DataFrame(dfa)
df = df.fillna("-")
print(df.transpose())





# nfa_table = pd.DataFrame(formatted)
# print(nfa_table.transpose())