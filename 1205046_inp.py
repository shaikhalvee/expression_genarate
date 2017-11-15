# Not auto generated input. Takes input from user.

import random
# global variables
opr = ['+', '-', '*']       #operator list
num = list(range(1, 10))    #number list [1,10]

def fitness(v, i):          #returns fitness value
	return -abs(v-evaluate(i))

def evaluate(A):            #evaluation function
	temp = "".join(str(i) for i in A)
	if temp == "":
		return 'EOF'
	return eval(temp)

def tournamentSelection(P):     #Selecton Function
	t = 5   # as stated in question
	best = random.choice(P)
	for i in range(t-1):
		Next = random.choice(P)
		if fitness(mainValue, Next) > fitness(mainValue, best):
			best = Next[:]
	return best[:]					#returns correct or not

def crossover(A, B):
	l = len(A) if len(A) < len(B) else len(B)	# taking the smallest length
	(lef, rit) = (random.randrange(l), random.randrange(l))
	(lef, rit) = (lef, rit) if lef < rit else (rit, lef)
	if random.random() < 0.5:       # cointoss, one point cross over
		for i in range(lef, l):
			(A[i], B[i]) = (B[i], A[i])
	else:
		for i in range(lef, rit):
			(A[i], B[i]) = (B[i], A[i])

	return (A[:], B[:])

def changeOperator(ch):
	return random.choice([x for x in opr if x is not ch])

def mutate(P):
	l = len(P)
	p = 1/l
	b = 0.5
	for i in range(l):
		if p >= random.random():
			while True:
				n = random.choice([1,-1])
				for x in range(len(P)):
					if (x % 2 != 0):
						P[x] = changeOperator(P[x])
					else:
						if 0 < (P[x] + n) < 10:
							P[x] = (P[x] + n)
						else:
							P[x] = (P[x] - n)
				if b < random.random():
					break
	return P[:]

def geneticAlgorithm(inpNumOfOpr, mainValue):
	itr = 0
	popSize = 15
	P = []
	for i in range(popSize):
		listSize = (inpNumOfOpr << 1) + 1
		temp = []
		for j in range(listSize):
			if j%2 != 0:
				temp.append(random.choice(opr))
			else:
				temp.append(random.choice(num))

		P.append(temp)
	Best = []
	while (evaluate(Best) != mainValue) and (itr <= 100):     # see about mainValue, can pass or not
		itr += 1
		for Pi in P:
			if Best == [] or fitness(mainValue, Pi) > fitness(mainValue, Best):
				Best = Pi[:]
		Q = []
		for p in range(popSize//2):
			Pa, Pb = tournamentSelection(P), tournamentSelection(P)
			Ca, Cb = crossover(Pa[:], Pb[:])
			Q.extend([mutate(Ca), mutate(Cb)])
		P = Q       #[_[:] for _ in Q]  if not copy

	return Best, itr, popSize

p = -1e40
outF = open("Output.txt","w")
inpNumOfOpr = int(input("Input the number of operators: "))
mainValue = int(input("Input the evaluating number: "))
outF.write("Target     Operators    Popsize    Iterations      Best-fitness\n")
outF.write("===============================================================\n")
for i in range(5):
	answer, itr, popSize = geneticAlgorithm(inpNumOfOpr, mainValue)
	outF.write("%-10d %-12d %-10d %-15d %-15d\n" % (mainValue, inpNumOfOpr, popSize, itr - 1, fitness(mainValue, answer)))
	outF.write("Answer: %s evaluation: %d\n" % ("".join(str(i)+" " for i in answer), evaluate(answer)))
	if fitness(mainValue, answer) > p:
		p = fitness(mainValue, answer)
		ans = answer[:]
outF.write("\nBest answer: %s evaluation: %d\n" % ("".join(str(i)+" " for i in ans), evaluate(ans)))
outF.close()
