import math
import scipy 
from scipy.stats import bernoulli, binom
import numpy as np
import matplotlib.pyplot as plt
import itertools
import collections
from collections import Counter
import statistics
import random

#User's input:

#1. number of nodes
n=int(input("number of nodes: "))

# Max number of links (in-degrees) a node can have in a network of size n
l=n-1

#Creating a list of nodes based on user's input, n:

list1=[]

for i in range(1,n+1):
    list1.append(i)



#-----------------------------------------------------------

# Basic constant Meachanism 

def constant_mechanism():
    #Workflow:
    #1. Assign manually popularity to each node
    #2. Choose as a default winner node, node with highest popularity
    #3. Additive approximation: calculate difference in degrees between winner node and node with max in-degree 
    
    #Assign popularity to each node manually
    list2=[]
    for i in list1:
        z="popularity of a node number"+" "+str(i)+": "
        b=input(z)
        i += 1
        list2.append(b)
        list3 = [float(i) for i in list2]
    #print(f"list of popularities: {list3}")

    #Find highest popularity inserted 
    max_value = max(list3) 
    
    #Find index of highest popularity (index+1 will be a node number with max popularity), this node is a winner
    max_index = list3.index(max_value)
 
    
    print(f"max_index: {max_index}")
    print(f"CONSTANT MECHANISM:\nThe winner node is node number {max_index+1} with probability {max_value}")
    
    #Generate random in-degree for each node based on binomial distribution 
    list4=[]
    for i in list3:
        #generate random in-degree for each node with different probability using binomial distribution binom(l,p,size)
        #where l- max possible number of links a graph can have, p-succes probability, size- number of repeats
        rnd_values = binom.rvs(l, i, size=1)
        v=rnd_values.item() #takes value from each array
        list4.append(v)
    print(f"list of indegrees: {list4}") #list with degree for each node 

    #winner node in-degree
    wd=list4[max_index] 
    #print(wd)
    
    #Find maximum value of in-degree for the network
    max_indegree = max(list4) 
    
    print(f"additive approximation: {max_indegree-wd}")
    
#----------------------------------------------------------------------------------------------------------------    

#Basic AVD mechanism with various popularities of each node manually inserted
def AVD_mechanism_various_popularities():
    #Work flow:
    #1. Assign manually popularity to each node
    #2. Choose as a default winner node, node with highest popularity (find its number)
    #3. Generate using binomial distribution in-degree for each node based on node's popularity  
    #4. Find node/s with max in-degree and their indices on the in-degree list
    #5. Compare in-degree of a default winner to a node with maximum in-degree for each popularity 
    #6. Return error 
    
    
    #Assign popularity to each node manually
    list2=[]
    for i in list1:
        z="popularity of a node number"+" "+str(i)+": "
        b=input(z)
        i += 1
        list2.append(b)
        list3 = [float(i) for i in list2]
    #print(list3)

    #Find highest popularity inserted 
    max_value = max(list3)
    
    #DEFAULT WINNER: Find index of highest popularity (index+1 is a dafault winner node number)
    max_index = list3.index(max_value) 

    
    print(f"AVD MECHANISM:\nThe default winner node is node number {max_index+1} with probability {max_value}")

    #Generate random in-degree for each node based on binomial distribution and nodes' popularities
    list4=[]
    for i in list3:
        #generate random in-degree for each node with different probability using binomial distribution binom(l,p,size)
        #where l- max possible number of links a graph can have, p-succes probability, size- number of repeats
        rnd_values = binom.rvs(l, i, size=1)
        v=rnd_values.item() #takes vale from each array
        list4.append(v)
    print(f"Node number: in-degree:  {dict(zip(list1, list4))}")


    #default winner node in-degree
    dwd=list4[max_index] #
    
    #find indices of nodes with highest in-degree
    max_indegree = max(list4)
    indices=[i for i, j in enumerate(list4) if j == max_indegree] 
    #print(indices)

    #Conditions of winning:
    
    #check if default winner has also max in-degree value, if yes, it wins 
    if max_index in indices: 
        print(f"The winner node is  a default winner node number {max_index+1} with in-degree {max_indegree}")
        return(max_indegree-max_indegree)
    #if defaault winner does not have highest degree:
    elif max_index not in indices: 
        #check if there is more than one node with max in-degree (checks for duplicates), if no, node with max in-degree wins
        if len(set(list4)) == len(list4): 
            print(f"node with highest in-degree is node number: {indices[0]+1} with in-degree of {max_indegree}")
            return(max_indegree-max_indegree)
        #if there's a draw between other nodes (at max in-degree level), default winner wins
        elif len(set(list4)) != len(list4):
            if list4.count(max_indegree)>1:
                print(f"The winner node is a default winner node number {max_index+1} with in-degree {dwd}")
                return(max_indegree-dwd)
            #if there is only one node with max in-degree and is NOT a default winner, this node wins
            else:
                print(f"The winner node is node number: {indices[0]+1} with in-degree of {max_indegree}")
                return(max_indegree-max_indegree)

#----------------------------------------------------------------------------------------------------
# AVD mechanism with automatically generated uniform popularities in 0.1 intervals
def AVD_mechanism_assigned_uniform_popularities():
    
    #Work flow:
    #1. Assign the same popularity to each node, for all popularities in the range 0 and 1, with intervals of 0.1 (e.g.0, 0.1, 0.2)
    #2. Generate degree for each node and each probability based on binomial distribution
    #3. Choose random default winner node from generated nodes and their corresponding in-degrees
    #4. Find node/s with max in-degree and their indices on the list of in-degree list
    #5. Compare in-degree of default winner to node with maximum in-degree for each popularity (0,0.1,0.2 etc)
    #6. Return error 
    
    
    #generate values of popularities in intervals of 0.1 (in range 0-1)
    popularities=np.linspace(0,1,11)

    # 1d array to list
    #arr = np.array(popularities)
    #convert array of popularities for nodes to the list of lists 
    list_popularities = popularities.tolist()
    
    #round all popularities to 1 decimal place
    round_to_tenths = [round(num, 1) for num in list_popularities]

    #print list to check if generated correctly
    print(round_to_tenths)

    
    #Generate list of lists of popularities 
    #(each sublist contains number of nodes n, with the same popularity of 0, 0.1, 0.2 etc)
    list5=[]
    for i in round_to_tenths: 
        nodes_popularities=[i]*n
        list5.append(nodes_popularities)       
    #print(f"nodes popularities: {list5}")
    
    
    #Generate random in-degree for each node based on binomial distribution
    #(each sublist contains node in-degree (based on number of nodes n), with the same popularity of 0, 0.1, 0.2 etc)
    list6=[]
    for i in round_to_tenths:
        #generates degree for each node that has the same popularity (0.1, 0.2)
        rnd_values = binom.rvs(l, i, size=n) 
        v=rnd_values.tolist() 
        list6.append(v)
    #list with degrees for nodes, with popularity 0, 0.1, 0.2 etc   
    #print(f"nodes indegrees: {list6}") 

   
    #Choose random default winner node (and its degree and number), find node/s with max in-degree and their numbers, 
    #for each popularity
    list8=[]
    list9=[]
    list10=[]
    list11=[]
    for i in list6:
        for j in i:
            #choose random default winner node 
            default_winner = random.choice(i) 
            #obtain index of random default winner (index+1 will be a number of that node)
            default_index = i.index(default_winner) 
            #find maximum value/s of in-degree on each sublist
            max_indegree=max(i)
            #obtain index/indices of all node/s on each sublist that has/have max in-degree 
            indices=[x for x, y in enumerate(i) if y == max_indegree]
            
        #append all values to corresponding lists for further processing
        list8.append(default_winner)
        list9.append(default_index)
        list10.append(max_indegree)
        list11.append(indices)
        
    #print(f"default winners degrees: {list8}")
    #print(f"default winners index: {list9}")
    #print(f"max indegree: {list10}")
    #print(f"indices of nodes with max indegree: {list11}")
    
    
    
    #1.Check if default winner has also highest degree (if yes- it's a winner)
    #2.If default winner doesn't have max in-degree:
    #3. Check if there's draw between rest of the nodes (more than one has max in-degree):
      #If yes- default winner wins
      #if no- node with max in-degree wins
    #4.Calculate error
    a=0
    for i in list9:
        #checks if default winner has also max in-degree, if yes, it wins
        if i in list11[a]: 
            print(f"For probability {round_to_tenths[a]} The winner node is  a default winner node number {i+1} with in-degree {list10[a]}")
            print(f"error: {list10[a]-list10[a]}")
        # if default winner doesn't have max in-degree:    
        elif i not in list11[a]:
            #check if there is more than one node with max in-degree (checks for duplicates), if no, node with max in-degree wins
            if len(set(list6[a]))==len(list6[a]): 
                print(f"For probability {round_to_tenths[a]} node with highest in-degree is node number: {list11[a][0]+1} with in-degree of {list10[a]}")
                print(f"error: {list10[a]-list10[a]}")
            #if there's a draw between other nodes (at max in-degree level), default winner wins    
            elif len(set(list6[a]))!=len(list6[a]):
                if list6[a].count(max_indegree)>1:
                    print(f"For probability {round_to_tenths[a]} The winner node is a default winner node number {i+1} with in-degree {list8[a]}")
                    print(f"error: {list10[a]-list8[a]}")
                #if there is only one node with max in-degree and is NOT a default winner, this node wins
                else:
                    print(f"For probability {round_to_tenths[a]} The winner node is node number: {list11[a][0]+1} with in-degree of {list10[a]}")
                    print(f"error: {list10[a]-list10[a]}")
                    
        a+=1
    
#-----------------------------------------------------------------------------------------------------------------------------------
#AVD/constant mechanism with 
#-uniform popularity,
#-half uniform: (half nodes with the same high popularity, half with the same low popularity
#-one node high popularity, rest low(uniform)
#-one node low popularity, rest high (uniform)
def AVD_constant_mechanism_uniform_popularity():
    
    #General Work flow:
    #1. Assign manually either the same popularity to each node, or high and low popularities 
    #   (depending on the type of algorithm used- see below)
    #2. Choose as a default winner node random node with highest popularity and find its number
    #3. Generate using binomial distribution in-degree for each node  
    #4. Find node/s with max in-degree and their indices on the in-degree list
    #5. Carry out either constant or AVD mechanism (depending on user's input)
    #6. Compare in-degree of a default winner to a node with maximum in-degree for each popularity 
    #7. Return error 
    
    #Decide which scenario to use: 
    #A- first half of nodes has assigned high popularity (>0.7), the other half low popularity (<0.4)
    #B- random half of the nodes has assigned high popularity (>0.7), the remaining half has popularity(<0.4)
    #C- the same popularity for all nodes
    #D- one random node has high popularity, >0.7, rest nodes have low uniform popularity, <0.4
    #E- one random node has low popularity, <0.4, rest nodes have high uniform popularity, >0.7
    #F- random popularities in range o-1 are generated by the program and assigned to each node
    mechanism = input("constant/AVD: ").lower()
    type = input("A/B/C/D/E/F: ").lower()

    if type == "a":
        #High Popularity of >0.7
        high="uniform high popularity:"
        b=input(high)
        
        #Low Popularity of <0.4
        low="uniform low popularity:"
        c=input(low)
    
       
    elif type =="b":
        #Uniform high popularity assigned to random half of nodes in the network (value>0.7)
        high="high popularity:"
        b=input(high)

        #Uniform low popularity assigned to random half of nodes in the network (value<0.4)
        low="low popularity:"
        c=input(low)
    elif type=="c":
        #Popularity that is assigned to each node (enter value between 0-1 in increments of 0.1)
        z="uniform popularity:"
        b=input(z)
    
    elif type == "d":
        #High popularity (>0.7) assigned to one random node
        high="high popularity:"
        b=input(high)
        
        #Low popularity (<0.4) assigned rest of the nodes
        low="low popularity:"
        c=input(low)
    
        
    elif type=="e":
        #High popularity (>0.7) assigned to n-1 random nodes
        high="high popularity:"
        b=input(high)
        
        #Low popularity (<0.4) assigned to random one node only 
        low="low popularity:"
        c=input(low)
        
        
        
    elif type == "f":
        #generate random numbers between 0-1
       
        pass
        
       
    else:
        print("Invalid option.")
    

    #create list for storing additive approximation from trials
    list_additive_approx=[]
    
    # range can be adjusted depending how many trials for the same algorithm and with the same popularities we want to perform
    for i in range(25):
        if type == "a":
            if n%2==0:
            #if number of nodes even: split nodes into halves
                e=len(list1)//2
            else:
            #if number of nodes odd: split nodes into two parts (with 1 part containing 1 more node than another) 
                e=(len(list1)+1)//2
            
    
        #creating list of popularities
            list2=[]
            for i in list1[:e]:
                list2.append(b)    
            for i in list1[e:]:
                list2.append(c)    
            list3 = [float(i) for i in list2]
        #print(f"list of popularities: {list3}") 
      
    
        #pick random node as a default winner
            default_winner = random.choice(list1[:e]) 
            print(f"default winner node number: {default_winner}")
            
        #obtain index of random default winner (index+1 will be a number of that node)
            default_index = list1.index(default_winner)
        #print(default_index)

            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_index+1} with popularity {b}")
            
        elif type =="b":

        #Check if number of nodes is even to divide nodes into half or half+1(if odd)
            if n%2==0:
            #even number of nodes
                e=len(list1)//2
            else:
            #odd number of nodes
                e=(len(list1)+1)//2
        
        #chooses random half/half+1 (e) nodes that will be assigned high popularity
            rand=random.sample(list1, e)
        #print(rand)

        #Assign high popularity to random nodes (rand) and low popularity to rest of the nodes
            list2=[]
            for i in list1:
                if i in rand:
                    list2.append(b)
                else:
                    list2.append(c)    
            list3 = [float(i) for i in list2]
        #print(f"list of popularities: {list3}") 

        
        #pick random node with high popularity as a default winner
            default_winner = random.choice(rand) 
            print(f"default winner node number:{default_winner}")        
            
            #obtain index of random default winner (index+1 will be a number of that node)
            default_index = list1.index(default_winner)
            #print(f"default winner index:{default_index}")

            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_winner} with popularity {b}") 
    
        elif type =="c":
            #Create list with popularities for each node (for further processing)
            list2=[]
            for i in list1:
                list2.append(b)
                list3 = [float(i) for i in list2]
        #print(f"list of popularities: {list3}")
        #pick random node as a default winner
            default_winner = random.choice(list1) 
            print(f"default winner node number:{default_winner}")  
        #obtain index of random default winner (index+1 will be a number of that node)
            default_index = list1.index(default_winner)
        #print(default_index)

            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_index+1} with popularity {b}")
        elif type =="d":
            #choose a random node that will be assigned high popularity and get its index from the list of nodes
            rand=random.choice(list1)
            default_index=list1.index(rand)
        #print(f"default winner index: {default_index}")
   
        #Based on user input create list with popularities for each node (for further processing)
            list2=[]
            for i in range(len(list1)):
                #assign high popularity to chosen node
                if i==default_index:
                    list2.append(b)
            #assign low popularity to rest of the nodes
                else:
                    list2.append(c)    
            list3 = [float(i) for i in list2]
        #print(f"list of popularities: {list3}") 
    
    
            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_index+1} with popularity {b}")
        elif type =="e":
            #choose a random node that will be assigned a low popularity and get its index on list of nodes
            rand=random.choice(list1)
            rand_index=list1.index(rand)
   
        #Based on user input create list with popularities for each node (for further processing)
            list2=[]
            for i in range(len(list1)):
            #assign low popularity to chosen node
                if i==rand_index:
                    list2.append(c)
            #assign high popularity to rest of the nodes
                else:
                    list2.append(b)    
            list3 = [float(i) for i in list2]
        #print(f"list of popularities: {list3}") 
    

        #create list with all the nodes that have high degree
            d = [x for i,x in enumerate(list1) if i!=rand_index]
         
        #pick random node with high popularity as a default winner and find its index on list of nodes
            default_winner=random.choice(d)
            default_index = list1.index(default_winner)
                

            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_winner} with popularity {b}")
        elif type =="f":
            list2=[]
            for i in range(len(list1)):
                value=random.uniform(0, 1)
        #rounding popularity value to 1 decimal place
                value_1 = round(value, 1)
                list2.append(value_1)
        #generating list3 that will be used for further processing (to keep consistency of the program)
            list3 = [float(i) for i in list2]
            print(f"list of popularities: {list3}") 
            
        #Find highest popularity/popularities generated
            max_value=max(list3)
        #find indices of all the nodes with max values on the list3 (randomly generated popularities)
            indices_max_value = [index+1 for index, value in enumerate(list3) if value == max_value]
            print(indices_max_value)
       
        #pick random node as a DEFAULT WINNER from list of highest popularities (indices)
            default_winner = random.choice(indices_max_value)
        #print(default_winner)
        #FInd index of a deafult winner on list of nodes (to determine default winner node number: default index+1)
            default_index = list1.index(default_winner)
       
            print(f"AVD MECHANISM:\nThe DEFAULT WINNER node is node number {default_winner} with popularity {max_value}")
        else:
            print("Invalid option.")
        
    
        list4=[]
        for i in list3:
        #generate random in-degree for each node with different probability using binomial distribution binom(l,p,size)
        #where l- max possible number of links a graph can have, p-succes probability, size- number of repeats
            rnd_values = binom.rvs(l, i, size=1)
            v=rnd_values.item() #takes value from each array
            list4.append(v)
        #print(f"list of indegrees: {list4}") #list with degree for each node 

    #Constant mech: winner, AVD:default winner node in-degree
        dwd=list4[default_index] 
    #print(dwd)
    
    #Find maximum value of in-degree for the network
        max_indegree = max(list4)
    
    #find index/indices of all max in-degrees values
        indices=[i for i, j in enumerate(list4) if j == max_indegree] 
    #print(indices)
    
        #mechanism = input("constant/AVD: ").lower()
    
        if mechanism == "constant":
            print(f"Additive approximation: {max_indegree-dwd}")
            diff=max_indegree-dwd
       
               
        elif mechanism == "avd":
        #Conditions:
        #error(additive approximation): optimal(max) in-degree for a network - in-degree of a node that actually wins
        #check if DEFAULT WINNER has also max in-degree, if YES, it WINS 
            if default_index in indices: 
                print(f"The WINNER NODE is  a DEFAULT WINNER node number {default_index+1} with in-degree {max_indegree}")
                print(f"Additive approximation: {max_indegree-max_indegree}")
                diff=max_indegree-max_indegree
            
        #if DEFAULT WINNER does NOT have max in-degree:
            elif default_index not in indices:
            #check if there is MORE THAN ONE node with max in-degree (check for duplicates), 
            #if NO, NON-DEFAULT node with max in-degree wins
                if len(set(list4)) == len(list4): 
                    print(f"The WINNER NODE with highest in-degree is NODE NUMBER: {indices[0]+1} with in-degree of {max_indegree}")
                    print(f"Additive approximation: {max_indegree-max_indegree}")
                    diff=max_indegree-max_indegree
                
                
            #if there's a draw between NON-DEFAULT nodes (at max in-degree level), DAFAULT winner WINS
                elif len(set(list4)) != len(list4):
                    if list4.count(max_indegree)>1:
                        print(f"The WINNER NODE is a DEFAULT WINNER node number {default_index+1} with in-degree {dwd}")
                        print(f"Additive approximation: {max_indegree-dwd}")
                        diff=max_indegree-dwd
                    
                    
                #if there is ONLY ONE node with max in-degree and is NOT a default winner, this node wins
                    else:
                        print(f"The WINNER NODE with highest in-degree is NODE NUMBER: {indices[0]+1} with in-degree of {max_indegree}")
                        print(f"Additive approximation: {max_indegree-max_indegree}")
                        diff=max_indegree-max_indegree
        
        list_additive_approx.append(diff)
    mean_additive_approx=statistics.mean(list_additive_approx)
    print(f"Additive approximations: {list_additive_approx}")
    print(f"Average additive approximation for {mechanism.upper()} mechanism and algorithm {type.upper()} with {n} nodes and chosen popularities is: {mean_additive_approx}")
                    
        
        
AVD_constant_mechanism_uniform_popularity() 
#AVD_mechanism_various_popularities()


# #### 

# In[ ]:




