from random import randint, sample
from itertools import chain, combinations
import time
import sys

class SSP():
    def __init__(self, S=[], t=0, worst=0, best=100):
        self.S = S
        self.t = t
        self.n = len(S)
        self.best = best
        self.worst = worst
        self.TotalTime = 0
        self.myMax = []
        #
        self.decision = False
        self.total    = 0
        self.selected = []

    def __repr__(self):
        return "SSP instance: S="+str(self.S)+"\tt="+str(self.t)
    
    def random_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = randint(0,n*max_n_bit_number)
        self.n = len( self.S )

    def random_yes_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = sum( sample(self.S, randint(0,n)) )
        self.n = len( self.S )

    ###

    def try_at_random(self):
        candidate = []
        total = 0
        startTime = time.time()
        while total != self.t:
            candidate = sample(self.S, randint(0,self.n))
            total     = sum(candidate)
           ## print( "Trying: ", candidate, ", sum:", total )
        endTime = time.time()
        TimeTaken = endTime - startTime
        print(TimeTaken)


    def resetvars(self):
        self.best = sys.maxsize
        self.worst = 0.0
        self.TotalTime = 0.0
        self.myMax = []

    def exhaustive_search(self):
        
       # t0 = time.clock()
        StartTime = time.time()
        for subset in chain.from_iterable(combinations(self.S, r) for r in range(len(self.S)+1)):
            ##print ("Subset didnt match ",subset)
            
            if sum(subset)==self.t:
                ##print("", end ='')
                EndTime = time.time()
                TimeTaken = EndTime - StartTime
                ##print(TimeTaken,self.t,subset)
                self.TotalTime += TimeTaken

                if self.worst < TimeTaken:
                    self.worst = TimeTaken
                
                if self.best > TimeTaken:
                    self.best = TimeTaken
                    ##print(subset,self.t,self.best)
                return self.best,self.worst,self.TotalTime
                ##print("Subset did match ", subset)
               # print(time.clock() - t0, "seconds")
        
    def Dynamic_Programming(self):
        StartTime = time.time()
        subset = [[ False for x in range(self.n+1)] for y in range(self.t+1)] 
        i = 0
        for i in range(self.n):
            
            subset[0][i] = True
            ##print(i,subset[0][i])
        
        for i in range(1,self.t):
            
            subset[i][0] = False


        for i in range(1,self.t+1):
            
            for j in range(1,self.n+1):
                
                subset[i][j] = subset[i][j-1]
                
                if (i >= self.S[j-1]):
                    ##print("before",subset[i+1][j+1])
                    subset[i][j] = subset[i][j] or subset[i-self.S[j-1]][j-1]
                    ##print("after",subset[i+1][j+1])
        
        
##        for i in range(self.t+1):
##            j=0
##            print ("reulting grid1",i,j,subset[i][j])
##            
##            
##            for j in range(self.n+1):
##                
##                print ("reulting grid2",i,j,subset[i][j])
                
        ##print(self.t,self.n,subset[self.t][self.n])
        ##return subset[self.t][self.n]
        EndTime = time.time()
        TimeTaken = EndTime - StartTime
        
        ##print(TimeTaken,self.t,subset)
        self.TotalTime += TimeTaken
        if self.worst < TimeTaken:
            self.worst = TimeTaken
            
        if self.best > TimeTaken:
            self.best = TimeTaken
        return self.best,self.worst,self.TotalTime

    def HighestNumber(self,total):
        maxSoFar = 0
        
        for num in self.S:
            if maxSoFar < num  and (num + total) <= self.t and num not in self.myMax:
                maxSoFar = num
        if maxSoFar != 0:
            self.myMax.extend([maxSoFar])
        print("This is myMax",self.myMax)
        
    
    def Greedy(self):
        startTime = time.time()
        i = 0
        total = 0
        subset = []
        while [x for x in self.S if x not in subset]:
            if i == 0:
                 instance.HighestNumber(total)
                
            print(self.S[i],total)
            if (total +self.S[i] <= self.t and self.S[i] in self.myMax):
                subset.extend([self.S[i]])
                total += self.S[i]
                i = -1
            i+=1
            print(subset, " " ,i)
            if self.n <= i:
                self.myMax = []
                endTime = time.time()
                TimeTaken = endTime - startTime
                if self.worst < TimeTaken:
                    self.worst = TimeTaken
            
                if self.best > TimeTaken:
                    self.best = TimeTaken
                print("Found the solution and it is ", (self.t - total))
                return subset, self.t - total
    def f(self,s):
        return self.t - sum(s)
    def Greedy2(self):
        startTime = time.time()
        x = 0
        candidate = []
        total = 0
        newList = list(self.S)
        
        while len(newList) > 0 and newList[x] is not None and newList[x] not in candidate:
            print(self.t," ",sum(candidate))
            
            if self.t == sum(candidate):
                newList.remove(max(newList))
                break
            if max(newList) + total  <= self.t:
                total = total + max(newList)
                candidate.extend([max(newList)])
                newList.remove(max(newList))
                x=0
            else:
                newList.remove(max(newList))                
                x =0

        endTime = time.time()

        TimeTaken = endTime - startTime

        self.TotalTime += TimeTaken

        if self.worst < TimeTaken:
            self.worst = TimeTaken
    
        if self.best > TimeTaken:
            self.best = TimeTaken
        print(self.S," ", candidate, " ", self.t - total," ", total ," ",self.t)
        return self.best,self.worst,self.TotalTime,candidate,(self.t - total)

    def Iterative_Improvement(self, s):
        i=0
        s2 = [ s[x] for x in range(len(s))]
        print(len(s2))
        print("This is s2 ", s2, "This is s ",s)
        while sum(s) != self.t or i != self.S:
            for num in self.S:
                print(num," ", s)
                if num not in s:
                    print (len(s2),i)
                    if len(s2) <= i:
                        return "most optimum solution possible for this search",s," ",s2
                    s2[i] = num
                    i+=1
                    
                    print(instance.f(s2)," ",instance.f(s))
                    if instance.f(s2) < instance.f(s) and instance.f(s2) >= 0:
                        print("Found a better solution")
                        s = s2
        print("Solution ",s)
            #replace s with better solution
        #return s
count = 0 
q = 0   
 

instance = SSP()
time.clock()
instance.random_yes_instance(10)
bestcase,worstcase,TotalTime,Candidate,Closeness = instance.Greedy2()

##print(instance.Iterative_Improvement(best_candidate))
for n in range(10,500): # start the search with 5 elements in array, stop when there are 29 elements
    instance.resetvars()
    q += 1
     
# start the clock
    for i in range(80): # After 5 iterations the loop ends. Loop starts again when new element is added to the array.
        pass
        ##instance.random_yes_instance(n)
        ##instance.random_instance(n)
        ##instance.random_yes_instance(n)
        ##result = instance.Greedy()
        ##print( instance )
        ##bestcase,worstcase,TotalTime,best_candidate,result = instance.Greedy()
        #bestcase, worstcase , TotalTime = instance.exhaustive_search()
        ##bestcase,worstcase,TotalTime,Candidate,Closeness = instance.Greedy2()
        
        ##instance.Dynamic_Programming()
        ##instance.try_at_random()
        ##bestcase, worstcase, TotalTime = instance.Dynamic_Programming()
##        if n == 26:
##            print("Stop now",time.clock())
    
    ##print(time.clock(), "seconds LAST") # I was testing here, I think this prints the total time it took for all 5 searches 

    ##print((TotalTime/80)*10) # Because the search is run amongst arrays of the same size 5 times, before incrementing the array size by 1, the avg would be the total clock time divided by 5. (Again just testing here)
    ##print(worstcase*10)
    ##print("best time ",bestcase*10)

