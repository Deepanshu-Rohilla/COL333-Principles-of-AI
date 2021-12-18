import sys
import numpy as np
import json
import copy
import time


sys.setrecursionlimit(100000)

n = 0
d = 0
m = 0
e = 0 
a = 0
s = 0 
T = 100000

startTime = time.time()

cur_cst = 0

# 0 to n-1 nurses + 0 - d-1 days

fileName = sys.argv[1]

data = np.genfromtxt(fileName,delimiter=',',skip_header=1,dtype='int')

soln_list = [   ]




nursesNode = {   }

for i in range(n):
	nursesNode[i] = {  }
	for j in range(d):
		nursesNode[i][j] = None

shifts = ['M','A','E','R']

vals = [ m , a , e , n - m - a - e  ]




def checkRestinWeek(day,doneRests):
	global d
	if d < 7:
		return True
	rem = day%7
	notGot = 0
	for i in range(n):
		gotRest = False
		for j in range(rem+1):
			if nursesNode[i][day-j] == 'R':
				gotRest = True
				break
		if gotRest == False:
			notGot+=1

	if notGot > (n-m-a-e)*(6-rem) + (n-m-a-e- doneRests):
		return False
	return True

Ans = [  ]


recur_cnt=0

def dfs1(i,j,cnt):
	global recur_cnt
	recur_cnt+=1
	#print(recur_cnt)
	rem = j%7
	notRest = [ ]
	for idx in range(n):
		gotRest = False
		for jdx in range(rem):
			if nursesNode[idx][j-jdx-1] == 'R':
				gotRest = True
				break
		if gotRest == False and nursesNode[idx][j]==None:
			notRest.append(idx)
	i1 = i
	for idx in range(n):
		if nursesNode[idx][j] == None:
			i1 = idx
			break
	newVals = ['M','A','E','R']
	if len(notRest)>0:
		i1 = notRest[0]
		newVals = ['R','M','E','A']

	else:
		if j!=0:


			Morn = []
			Even = []
			After = []

			for idx in range(n):
				if nursesNode[idx][j]==None:
					if nursesNode[idx][j-1]=='M':
						Morn.append(idx)
					elif nursesNode[idx][j-1]=='E':
						Even.append(idx)
					elif nursesNode[idx][j-1]=='A':
						After.append(idx)
			if len(Morn)>0:
				i1 = Morn[0]
				newVals = [ 'A','R','E','M' ]
			elif len(Even)>0:
				i1 = Even[0]
				newVals = [ 'A','R','E','M' ]
			elif len(After)>0:
				i1 = After[0]
				newVals = ['M','R','E','A']



	for idx in range(4):

		nursesNode[i1][j] = newVals[idx]
		idx2 = idx
		for kl in range(4):
			if shifts[kl] == newVals[idx]:
				idx2 = kl
				break
		cnt[idx2]+=1
		if cnt[idx2] <= vals[idx2]:
			if j==0 or nursesNode[i1][j]!='M' or nursesNode[i1][j-1]=='A' or nursesNode[i1][j-1]=='R':
				if i!=(n-1) or checkRestinWeek(j,cnt[3]):
					if i == n-1 and j == d-1:
						Ans.append(dict(nursesNode))
						return True
					elif i == n-1:
						gotAns = dfs1(0,j+1,[0,0,0,0])
						if gotAns:
							return True
					else:
						gotAns = dfs1(i+1,j,cnt)
						if gotAns:
							return True

		cnt[idx2]-=1
		nursesNode[i1][j] = None

	return False











def dfs_e(i,j,cnt,cst):
	if time.time() - startTime > T:
		return False
	global recur_cnt
	recur_cnt+=1
	#print(recur_cnt)
	rem = j%7
	notRest = [ ]
	for idx in range(n):
		gotRest = False
		for jdx in range(rem):
			if nursesNode[idx][j-jdx-1] == 'R':
				gotRest = True
				break
		if gotRest == False and nursesNode[idx][j]==None:
			notRest.append(idx)
	i1 = i
	for idx in range(n):
		if nursesNode[idx][j] == None:
			i1 = idx
			break
	newVals = ['M','A','E','R']
	if len(notRest)>0:
		i1 = notRest[0]
		newVals = ['R','M','E','A']
	else:
		if j!=0:
			Morn = []
			Even = []
			After = []
			for idx in range(n):
				if nursesNode[idx][j]==None:
					if nursesNode[idx][j-1]=='M':
						Morn.append(idx)
					elif nursesNode[idx][j-1]=='E':
						Even.append(idx)
					elif nursesNode[idx][j-1]=='A':
						After.append(idx)
			if len(Morn)>0:
				i1 = Morn[0]
				newVals = [ 'A','R','E','M' ]
			elif len(Even)>0:
				i1 = Even[0]
				newVals = [ 'A','R','E','M' ]
			elif len(After)>0:
				i1 = After[0]
				newVals = ['M','R','E','A']

	for idx in range(4):

		nursesNode[i1][j] = newVals[idx]
		idx2 = idx
		for kl in range(4):
			if shifts[kl] == newVals[idx]:
				idx2 = kl
				break
		if i1<s and (idx2==0 or idx2==2):
			cst *=2
		cnt[idx2]+=1
		if cnt[idx2] <= vals[idx2]:
			if j==0 or nursesNode[i1][j]!='M' or nursesNode[i1][j-1]=='A' or nursesNode[i1][j-1]=='R':
				if i!=(n-1) or checkRestinWeek(j,cnt[3]):
					if i == n-1 and j == d-1:
						global cur_cst
						cur_cst = cst
						Ans.append(copy.deepcopy(nursesNode))
						return True
					elif i == n-1:
						gotAns = dfs_e(0,j+1,[0,0,0,0],cst)
						if gotAns:
							return True
					else:
						gotAns = dfs_e(i+1,j,cnt,cst)
						if gotAns:
							return True

		if i1<s and (idx2==0 or idx2==2):
			cst/=2

		cnt[idx2]-=1
		nursesNode[i1][j] = None

	return False


def dfs(i,j,cnt,cst):
	if time.time() - startTime > T:
		return False
	global recur_cnt
	recur_cnt+=1
	#print(recur_cnt)
	rem = j%7
	notRest = [ ]
	for idx in range(n):
		gotRest = False
		for jdx in range(rem):
			if nursesNode[idx][j-jdx-1] == 'R':
				gotRest = True
				break
		if gotRest == False and nursesNode[idx][j]==None:
			notRest.append(idx)
	i1 = i
	for idx in range(n):
		if nursesNode[idx][j] == None:
			i1 = idx
			break
	newVals = ['M','A','E','R']
	if i1<s:
		newVals = ['M','E','A','R' ]
	if len(notRest)>0:
		i1 = notRest[0]
		newVals = ['R','M','E','A']

		if i1<s:
			newVals = ['E','R','M','A']


	else:
		if j!=0:


			Morn = []
			Even = []
			After = []

			for idx in range(n):
				if nursesNode[idx][j]==None:
					if nursesNode[idx][j-1]=='M':
						Morn.append(idx)
					elif nursesNode[idx][j-1]=='E':
						Even.append(idx)
					elif nursesNode[idx][j-1]=='A':
						After.append(idx)
			if len(Morn)>0:
				i1 = Morn[0]
				newVals = [ 'A','R','E','M' ]
				if i1<s:
					newVals = ['E','A','R','M']
			elif len(Even)>0:
				i1 = Even[0]
				newVals = [ 'A','R','E','M' ]
				if i1<s:
					newVals = ['E','A','R','M']
			elif len(After)>0:
				i1 = After[0]
				newVals = ['M','R','E','A']
				if i1<s:
					newVals = ['M','E','R','A']
	

	for idx in range(4):

		nursesNode[i1][j] = newVals[idx]
		idx2 = idx
		for kl in range(4):
			if shifts[kl] == newVals[idx]:
				idx2 = kl
				break
		if i1<s and (idx2==0 or idx2==2):
			cst *=2
		cnt[idx2]+=1
		if cnt[idx2] <= vals[idx2]:
			if j==0 or nursesNode[i1][j]!='M' or nursesNode[i1][j-1]=='A' or nursesNode[i1][j-1]=='R':
				if i!=(n-1) or checkRestinWeek(j,cnt[3]):
					if i == n-1 and j == d-1:
						global cur_cst
						if cst > cur_cst:
							Ans.append(copy.deepcopy(nursesNode))
							cur_cst = cst
						#print(cst)
					elif i == n-1:
						gotAns = dfs(0,j+1,[0,0,0,0],cst)
					else:
						gotAns = dfs(i+1,j,cnt,cst)

		if i1<s and (idx2==0 or idx2==2):
			cst/=2

		cnt[idx2]-=1
		nursesNode[i1][j] = None

	return False



if data.shape[1] == 5:
	for ii in range(data.shape[0]):
		n = data[ii][0]
		Ans = [ ]
		d = data[ii][1]
		m = data[ii][2]
		a = data[ii][3]
		e = data[ii][4]
		

		nursesNode = {   }

		for i in range(n):
			nursesNode[i] = {  }
			for j in range(d):
				nursesNode[i][j] = None

		shifts = ['M','A','E','R']

		vals = [ m , a , e , n - m - a - e  ]

		finalAns = dfs1(0,0,[0,0,0,0])

		if finalAns:
			soln_list.append(copy.deepcopy(Ans[0]))
		else:
			soln_list.append({  })

else:
	for ii in range(data.shape[0]):
		n = data[ii][0]
		Ans = [ ]
		d = data[ii][1]
		m = data[ii][2]
		a = data[ii][3]
		e = data[ii][4]
		s = data[ii][5]
		T = data[ii][6]

		nursesNode = {   }

		for i in range(n):
			nursesNode[i] = {  }
			for j in range(d):
				nursesNode[i][j] = None

		shifts = ['M','A','E','R']

		vals = [ m , a , e , n - m - a - e  ]


		startTime = time.time()

		Ans = [  ]

		cur_cst = 0


		dfs_e(0,0,[0,0,0,0],1)

		nursesNode = {   }

		for i in range(n):
			nursesNode[i] = {  }
			for j in range(d):
				nursesNode[i][j] = None

		shifts = ['M','A','E','R']

		vals = [ m , a , e , n - m - a - e  ]


		finalAns = dfs(0,0,[0,0,0,0],1)


		if len(Ans)>0:
			soln_list.append(copy.deepcopy(Ans[-1]))
		else:
			soln_list.append({ })



with open("solution.json" , 'w') as file:
   for d in soln_list:
       json.dump(d,file)
       file.write("\n")




