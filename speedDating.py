#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Speed dating algorithm:
# Groups of 6 people, then rotate groups, 
# no 2 people from same lab (ideally), no 2 people meet again
# 10 times

#number of people per group
peopleInGroup = 7

numberOfTimes = 10

#How optimize it we want it to be
numberOfBestMinimum = 6


# In[ ]:


import random
import numpy as np
import math
import pandas as pd


# In[ ]:


# Read excel/csv
fileName = 'ListOfPeoplewithPI.xlsx'
listOfPeople = pd.read_excel(fileName)
listOfPeople


# In[ ]:


max(listOfPeople.index) + 1


# In[ ]:


# Create list of available people for each person
availableChoices = dict();
for numPerson in listOfPeople.index:
    availableChoices[numPerson] = listOfPeople.index[listOfPeople.Groups[numPerson] != listOfPeople.Groups]


# In[ ]:





# In[ ]:


uniquePeopleMetBest = 0;
repeatedPeopleTotalBest = 100;
membersSameLabBest = 100;
groupsPerTimeBest = list();
newBest = 0
while newBest < numberOfBestMinimum:
    availableChoicesPrev = availableChoices.copy();
    availableChoicesCurrent = availableChoices.copy();

    remainingPeople = list(listOfPeople.index);
    groupsPerTime = list();
    numTime = 0
    while len(groupsPerTime)+1 < ((max(listOfPeople.index) + 1) / peopleInGroup)*numberOfTimes or len(remainingPeople) > 0:
        #print(numTime)
        remainingPeople = list(listOfPeople.index);
        try:
            while len(remainingPeople) > 0:
                random_num = random.choice(remainingPeople)
                #print(random_num)
                currentGroup = [random_num];
                remainingPeople.remove(random_num);

                while len(currentGroup) < peopleInGroup and len(remainingPeople) > 0:
                    currentAvailableGroup = availableChoicesCurrent[currentGroup[0]]
                    for person in currentGroup:
                        currentAvailableGroup = currentAvailableGroup.intersection(availableChoicesCurrent[person])
                    currentAvailableGroup = currentAvailableGroup.intersection(remainingPeople)
                    if len(currentAvailableGroup) > 0:
                        random_num = random.choice(currentAvailableGroup)
                    else:
                        random_num = random.choice(remainingPeople)
                    #print(random_num)
                    currentGroup.append(random_num);
                    remainingPeople.remove(random_num);

                for person in currentGroup:
                    for otherPerson in currentGroup:
                        availableChoicesCurrent[person] = availableChoicesCurrent[person].delete(availableChoicesCurrent[person] == otherPerson)

                groupsPerTime.append(currentGroup);
            numTime = numTime + 1;
        except Exception as e:
            #print(e)
            #print(remainingPeople)
            #print(len(groupsPerTime))
            numTime = 0;
            availableChoicesCurrent = availableChoices.copy();
            groupsPerTime = list();

    # Calculate average number of people that have seen each other more than once
    repeatedPeopleTotal = 0;
    uniquePeopleMet = 0;
    membersSameLab = 0;
    for idPerson in listOfPeople.index:
        unique_numbers = list();
        for group in groupsPerTime:
            if idPerson in group:
                for item in group:
                    unique_numbers.append(item)
                unique_numbers.remove(idPerson)

        #print(unique_numbers)
        repeatedPeopleTotal += len(unique_numbers) - len(set(unique_numbers))
        uniquePeopleMet += len(set(unique_numbers))
        membersSameLab += sum(listOfPeople.Groups[unique_numbers] == listOfPeople.Groups[idPerson])


    uniquePeopleMetCurrent = uniquePeopleMet / (max(listOfPeople.index) + 1)
    repeatedPeopleTotalCurrent = repeatedPeopleTotal / (max(listOfPeople.index) + 1)
    membersSameLabCurrent = membersSameLab / (max(listOfPeople.index) + 1);
        
    if uniquePeopleMetCurrent >= uniquePeopleMetBest and repeatedPeopleTotalCurrent <= repeatedPeopleTotalBest and membersSameLabCurrent <= membersSameLabBest:
        print('New Best!')
        groupsPerTimeBest = groupsPerTime.copy();
        uniquePeopleMetBest = uniquePeopleMetCurrent;
        repeatedPeopleTotalBest = repeatedPeopleTotalCurrent;
        membersSameLabBest = membersSameLabCurrent;
        print(uniquePeopleMetBest)
        print(repeatedPeopleTotalBest)
        print(membersSameLabBest)
        newBest = newBest + 1


# In[ ]:


fileName = 'groupsOfPeople_N_' + str(peopleInGroup) + '_times_' + str(numberOfTimes) + '.xlsx'
fileName


# In[ ]:


numGroup = 1;
numRound = 1;
maxGroups = math.ceil((max(listOfPeople.index) + 1) / peopleInGroup);

columnNames = list();
for num in range(maxGroups):
    columnNames.append('Group' + str(num+1))

df = pd.DataFrame(columns=columnNames, index = range(peopleInGroup))
#print('Round 1:')
with pd.ExcelWriter(fileName) as writer:
    df = pd.DataFrame(columns=columnNames, index = range(peopleInGroup))
    for group in groupsPerTimeBest:
        #print('Group ' + str(numGroup) + ':')
        numPerson = 0;
        for person in group:
            #print(str(listOfPeople.FirstName[person]) + ' ' + listOfPeople.LastName[person] + ' (' + listOfPeople.Groups[person] + ')')
            df.loc[numPerson, 'Group' + str(numGroup)] = (str(listOfPeople.FirstName[person]) + ' ' + listOfPeople.LastName[person] + ' (' + listOfPeople.Groups[person] + ')')
            numPerson = numPerson + 1;
        numGroup = numGroup + 1;
        if numGroup > maxGroups:
            numGroup = 1
            #print('Round ' + str(numRound) + ':')
            df.to_excel(writer, sheet_name='Round' + str(numRound))
            numRound = numRound + 1


# In[ ]:





# In[ ]:


# Calculate average number of people that have seen each other more than once
repeatedPeopleTotal = 0;
uniquePeopleMet = 0;
membersSameLab = 0;
for idPerson in listOfPeople.index:
    unique_numbers = list();
    for group in groupsPerTimeBest:
        if idPerson in group:
            for item in group:
                unique_numbers.append(item)
            unique_numbers.remove(idPerson)

    #print(unique_numbers)
    repeatedPeopleTotal += len(unique_numbers) - len(set(unique_numbers))
    uniquePeopleMet += len(set(unique_numbers))
    membersSameLab += sum(listOfPeople.Groups[unique_numbers] == listOfPeople.Groups[idPerson])


uniquePeopleMetCurrent = uniquePeopleMet / (max(listOfPeople.index) + 1)
repeatedPeopleTotalCurrent = repeatedPeopleTotal / (max(listOfPeople.index) + 1)
membersSameLabCurrent = membersSameLab / (max(listOfPeople.index) + 1);
print(uniquePeopleMetBest)
print(repeatedPeopleTotalBest)
print(membersSameLabBest)


# In[ ]:




