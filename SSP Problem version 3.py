from random import randint, sample
from itertools import chain, combinations
import time

class SSP():
    def __init__(self, S=[], t=0, worst=0, best=100):
        self.S = S
        self.t = t
        self.n = len(S)
        self.best = best
        self.worst = worst
        self.TotalTime = 0
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

    def random_yes_instance(self, n, bitlength):
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
        self.best = 100.0
        self.worst = 0.0
        self.TotalTime = 0.0

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
        return subset[self.t][self.n]
count = 0 
      
 

instance = SSP()
for n in range(10,40): # start the search with 5 elements in array, stop when there are 29 elements
    instance.resetvars()
 
# start the clock
    for i in range(10): # After 5 iterations the loop ends. Loop starts again when new element is added to the array.
        
        instance.random_yes_instance(n,i)
        
        ##print( instance )
        
        ##bestcase, worstcase , TotalTime = instance.exhaustive_search()
        ##instance.Dynamic_Programming()
        ##instance.try_at_random()
        if (instance.Dynamic_Programming()) == True:
            print("Found a subset")
        else:
            print("No subset found")
    
    ##print(time.clock(), "seconds LAST") # I was testing here, I think this prints the total time it took for all 5 searches 

    ##print(n," ",TotalTime/10, "seconds AVERAGE") # Because the search is run amongst arrays of the same size 5 times, before incrementing the array size by 1, the avg would be the total clock time divided by 5. (Again just testing here)
    ##print(n," ",worstcase, "worst case")
    ##print(n," ",bestcase, "seconds best case")
