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


# In[6]:


availableChoices[1]


# In[7]:


import random
import numpy as np
import math

availableChoicesPrev = availableChoices;
availableChoicesCurrent = availableChoices;

remainingPeople = list(listOfPeople.index);
groupsPerTime = list();


# In[ ]:





# In[8]:


numTime = 0
while len(groupsPerTime) < peopleInGroup*numberOfTimes:
    print(numTime)
    remainingPeople = list(listOfPeople.index);
    #try:
    while len(remainingPeople) > 0:
        random_num = random.choice(remainingPeople)
        #print(random_num)
        currentGroup = [random_num];
        remainingPeople.remove(random_num);

        while len(currentGroup) < peopleInGroup:
            currentAvailableGroup = availableChoicesCurrent[currentGroup[0]]
            for person in currentGroup:
                currentAvailableGroup = currentAvailableGroup.intersection(availableChoicesCurrent[person])
            currentAvailableGroup = currentAvailableGroup.intersection(remainingPeople)
            random_num = random.choice(currentAvailableGroup)
            #print(random_num)
            currentGroup.append(random_num);
            remainingPeople.remove(random_num);

        for person in currentGroup:
            for otherPerson in currentGroup:
                availableChoicesCurrent[person] = availableChoicesCurrent[person].delete(availableChoicesCurrent[person] == otherPerson)

        groupsPerTime.append(currentGroup);
    numTime = numTime + 1;
    #except Exception:
        #numTime = 0;
        #availableChoicesCurrent = availableChoices;
        #groupsPerTime = list();


# In[13]:


remainingPeople


# In[ ]:


unique_numbers = list()
for group in groupsPerTime:
    for item in group:
        unique_numbers.append(item)
print(set(unique_numbers))
len(unique_numbers)


# In[28]:


availableChoicesCurrent = availableChoices;
groupsPerTime = list();
remainingPeople = list(listOfPeople.index);
#try:
while len(remainingPeople) > 0:
    random_num = random.choice(remainingPeople)
    #print(random_num)
    currentGroup = [random_num];
    remainingPeople.remove(random_num);

    while len(currentGroup) < peopleInGroup:
        currentAvailableGroup = availableChoicesCurrent[currentGroup[0]]
        for person in currentGroup:
            currentAvailableGroup = currentAvailableGroup.intersection(availableChoicesCurrent[person])
        currentAvailableGroup = currentAvailableGroup.intersection(remainingPeople)
        random_num = random.choice(currentAvailableGroup)
        #print(random_num)
        currentGroup.append(random_num);
        remainingPeople.remove(random_num);

    for person in currentGroup:
        for otherPerson in currentGroup:
            availableChoicesCurrent[person] = availableChoicesCurrent[person].delete(availableChoicesCurrent[person] == otherPerson)

    groupsPerTime.append(currentGroup);


# In[29]:


groupsPerTime

