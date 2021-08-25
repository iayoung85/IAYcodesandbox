#Weekly Random Group generator
#By Isaac Young
#03-26-2017

#program written to satisfy the need to assign random groups each week that do not repeat throughout the semester. 

#step 1: using a list of all different students that have attended lab to date, take attendance then add new students who have not attended lab in previous weeks. Add the new students to the list of all students who have ever attended the lab
#step 2: #if the attendance list is an odd number of students. add a fake student to the list for picking random groups then have the person with the fake student join another random group.
#step 3: using the current week's attendance (with or without the fake student), use the round robin tournament algorithm to generate a set of all possible different weeks where # of different weeks is n minus 1.
#step 4: pick a random week from step 2 such that no 2-person group used in previous weeks is repeated
#step 5: return the following: 
    #1. this week's group assignments: a random week from the set of all weeks such that it does not repeat any pairing from any previous week. 
    #2. an updated set of all group assignments used thus far since the beginning of the semester
    #3. This week's attendance list.
    #4. an updated list of all students that have ever attended the lab.
    #5 week number





   
#given list of unique names with an even numbered list, returns a matrix of pairings for n-1 weeks where n is length of list
def roundrobinmaker(fulllist):
    if len(fulllist)%2==1:
        input('there was a critical error in the round robin algorithm enter to continue')
        return 'error roundrobin'
    matrix=list()
    splitset=listsplitter(fulllist)
    mergedset=splitsetmerger(splitset)
    matrix.append(mergedset)
    for n in range(int(len(fulllist)-2)):
        splitset=rotater(splitset)
        mergedset=[]
        mergedset=splitsetmerger(splitset)
        matrix.append(mergedset)
    import random
    for n in matrix:
        random.shuffle(n)
    return(matrix)

#split fulllist into 2: set1 and set2
def listsplitter(fulllist):
    set1=[]
    set2=[]
    for n in range(int(len(fulllist)/2)):
        set1.append(fulllist[n])
        set2.append(fulllist[-n-1])
    set2.reverse()
    returnset=[set1,set2]
    return returnset

# fix the 0th item in set1 and rotate all others clockwise by 1
def rotater(splitset):
    toprowendperson=splitset[0][-1]
    bottomrowfrontperson=splitset[1][0]
    splitset[0].remove(toprowendperson)
    splitset[0].insert(1,bottomrowfrontperson)
    splitset[1].remove(bottomrowfrontperson)
    splitset[1].append(toprowendperson)
    return(splitset)

#takes a split set of two lists of equal length and pairs the nth value from each set returns a list of pairs
def splitsetmerger(splitset):
    mergedgroups=[]
    for n in range(int(len(splitset[0]))):
        mergedgroups.append([splitset[0][n],splitset[1][n]])
    return mergedgroups

#checks to see if a group is in a matrix of lists of groups, returns a new matrix containing only the rows of the original matrix where the group was not contained
def checkforgroup(matrix,group):
    listn=[]
    for n in matrix:
        if group not in n and [group[1],group[0]] not in n:
            listn.append(n)
    return listn
#given a *matrix* of list of groups, returns a *new_matrix* containing only the rows of the original *matrix* where all of the groups in the list *all_groups* are not used
def checkforallgroups(matrix,all_groups):
    new_matrix=list()
    for n in matrix:
        new_matrix.append(n)
    for n in all_groups:
        new_matrix=checkforgroup(new_matrix,n)
    if len(new_matrix)==0:
        #print('there are not possible combinations where no one will have a repeat partner')
        return 'none'
    else:
        return new_matrix

#given an *attendance* list, prints a combination of groups (*todayspartners*) where no one has a repeat partner then edits the list of previous groups (*prvgroups*) to include chosen set of groups
def findweekspartners(attendance,prvgroups):
    matrixallposspairs=roundrobinmaker(attendance)
    legalweeks=checkforallgroups(matrixallposspairs,prvgroups)
    if legalweeks=='none':
        print('unable to find a set of groups that satisfies rules to have one partner per week')
        return 'none'
    import random
    todayspartners=legalweeks[random.randrange(len(legalweeks))]

    return todayspartners

#from the total list of all students to come to class, populates a list of those students who attended this week.
def takeattendance(masterstudentlist):
    attendancelist=list()
    student=''
    for n in masterstudentlist:
        print(n)
        student=input('is he or she present? y/n')
        print()
        if student=='y':
            attendancelist.append(n)
    return attendancelist

#adds names of students who are coming to class this week for the first time to this week's attendance
def getnewnames(weeksfullattendance,masterstudentlist):
    namq=0
    while namq!='end':
        namq=input("Enter name of new student to add to list. type 'end' when finished")
        while namq in masterstudentlist or namq in weeksfullattendance:
            namq=input('sorry but you must enter a unique name for each student. try again')
        if namq!='end':
            weeksfullattendance.append(namq)
            masterstudentlist.append(namq)
    return weeksfullattendance

errco=0
while errco==0:
    try:
        with open('studentdata.txt','r') as infile:
            allprevdata=list(infile)
        infile.closed
        errco=1
    except:
        outfile=open('studentdata.txt','w')
        outfile.close
        continue
if allprevdata==[]:
    weeknum=0
    cumattendance=[]
    prevpairs=[]
else:
    selecteddata=[]
    for n in range(-5,0,1):
        selecteddata.append(allprevdata[n])
    weeknum=int(selecteddata[0])
    import random
    import ast
    cumattendance=ast.literal_eval(selecteddata[-1])
    prevpairs=ast.literal_eval(selecteddata[-2])
weeknum=weeknum+1
print('this week:',weeknum)
returningstudents=takeattendance(cumattendance)
attendance=getnewnames(returningstudents,cumattendance)
for n in attendance:
    if n not in cumattendance:
        cumattendance.append(n)
if len(attendance)%2==1:
    try:
        attendance.remove('join another group')
    except:
        attendance.append('join another group')
        import random
        oddoneout=random.randrange(1,int(1+((len(attendance)-1)/2)))
        print()
        print()
        print('the odd person out must join group # ',oddoneout,'from the list')
weeksgroups=findweekspartners(attendance,prevpairs)
if weeksgroups=='none':
    import sys
    input('you are out of weeks. enter to exit')
    sys.exit()
for n in weeksgroups:
    prevpairs.append(n)
print('for week #',weeknum)
if 'join another group' in attendance:
    attendance.remove('join another group')
print('this weeks attendance was:',attendance)
print('this weeks groups will be:',weeksgroups)
print('all pairs to date:',prevpairs)
print('cumulative list of all students to come to class:',cumattendance)
input('enter to exit')
filelineitem=[weeknum,attendance,weeksgroups,prevpairs,cumattendance]
outfile=open('studentdata.txt', 'a')
outfile.write('\n'.join(list(map(str,filelineitem)))+'\n')
outfile.close()
