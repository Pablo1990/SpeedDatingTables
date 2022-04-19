#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Speed dating algorithm:
# Groups of 6 people, then rotate groups, 
# no 2 people from same lab (ideally), no 2 people meet again
# 10 times

#number of people per group
peopleInGroup = 6

numberOfTimes = 12


# In[2]:


# Read excel/csv
import pandas as pd

fileName = 'ListOfPeoplewithPI.xlsx'
listOfPeople = pd.read_excel(fileName)

print(listOfPeople)


# In[3]:


max(listOfPeople.index) + 1


# In[4]:


# https://stackoverflow.com/questions/36429507/python-combinations-without-repetitions
# Author: hahho
from itertools import chain, repeat, count, islice
from collections import Counter


def repeat_chain(values, counts):
    return chain.from_iterable(map(repeat, values, counts))


def unique_combinations_from_value_counts(values, counts, r):
    n = len(counts)
    indices = list(islice(repeat_chain(count(), counts), r))
    if len(indices) < r:
        return
    while True:
        yield tuple(values[i] for i in indices)
        for i, j in zip(reversed(range(r)), repeat_chain(reversed(range(n)), reversed(counts))):
            if indices[i] != j:
                break
        else:
            return
        j = indices[i] + 1
        for i, j in zip(range(i, r), repeat_chain(count(j), counts[j:])):
            indices[i] = j


def unique_combinations(iterable, r):
    values, counts = zip(*Counter(iterable).items())
    return unique_combinations_from_value_counts(values, counts, r)


# In[5]:


# Create list of available people for each person
availableChoices = dict();
for numPerson in listOfPeople.index:
    availableChoices[numPerson] = listOfPeople.index[listOfPeople.Groups[numPerson] != listOfPeople.Groups]


# In[ ]:





# In[6]:


import random
import numpy as np
import math


# In[ ]:





# In[ ]:


uniquePeopleMetBest = 0;
repeatedPeopleTotalBest = 100;
groupsPerTimeBest = list();
while uniquePeopleMetBest <= 60 and repeatedPeopleTotalBest >= 1:
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
                    random_num = random.choice(currentAvailableGroup)
                    #print(random_num)
                    currentGroup.append(random_num);
                    remainingPeople.remove(random_num);

                #for person in currentGroup:
                    #for otherPerson in currentGroup:
                        #availableChoicesCurrent[person] = availableChoicesCurrent[person].delete(availableChoicesCurrent[person] == otherPerson)

                groupsPerTime.append(currentGroup);
            numTime = numTime + 1;
        except Exception as e:
            #print(e)
            #print(remainingPeople)
            numTime = 0;
            availableChoicesCurrent = availableChoices.copy();
            groupsPerTime = list();

    # Calculate average number of people that have seen each other more than once
    repeatedPeopleTotal = 0;
    uniquePeopleMet = 0;
    for idPerson in listOfPeople.index:
        unique_numbers = list();
        for group in groupsPerTime:
            if idPerson in group:
                for item in group:
                    unique_numbers.append(item)
                unique_numbers.remove(idPerson)
        repeatedPeopleTotal += len(unique_numbers) - len(set(unique_numbers))
        uniquePeopleMet += len(set(unique_numbers))

    uniquePeopleMetCurrent = uniquePeopleMet / (max(listOfPeople.index) + 1)
    repeatedPeopleTotalCurrent = repeatedPeopleTotal / (max(listOfPeople.index) + 1)
        
    if uniquePeopleMetCurrent > uniquePeopleMetBest and repeatedPeopleTotalCurrent < repeatedPeopleTotalBest:
        print('New Best!')
        groupsPerTimeBest = groupsPerTime.copy();
        uniquePeopleMetBest = uniquePeopleMetCurrent;
        repeatedPeopleTotalBest = repeatedPeopleTotalCurrent;
        print(uniquePeopleMetBest)
        print(repeatedPeopleTotalBest)


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


repeatedPeopleTotal = 0;
uniquePeopleMet = 0;
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

uniquePeopleMetCurrent = uniquePeopleMet / (max(listOfPeople.index) + 1)
repeatedPeopleTotalCurrent = repeatedPeopleTotal / (max(listOfPeople.index) + 1)
print(uniquePeopleMetCurrent)
print(repeatedPeopleTotalCurrent)


# In[ ]:




