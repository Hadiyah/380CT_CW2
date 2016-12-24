from random import randint, sample
from itertools import chain, combinations
import time

class SSP():
    def __init__(self, S=[], t=0):
        self.S = S
        self.t = t
        self.n = len(S)
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
        while total != self.t:
            candidate = sample(self.S, randint(0,self.n))
            total     = sum(candidate)
            print( "Trying: ", candidate, ", sum:", total )






    def exhaustive_search(self):

       # t0 = time.clock()
        
        for subset in chain.from_iterable(combinations(self.S, r) for r in range(len(self.S)+1)):
            #print (subset)
            if sum(subset)==self.t:
            
                print(subset)
               # print(time.clock() - t0, "seconds")
        

                
count = 0 
      
           

instance = SSP()
for n in range(5,30): # start the search with 5 elements in array, stop when there are 29 elements

    time.clock() # start the clock
    for i in range(5): # After 5 iterations the loop ends. Loop starts again when new element is added to the array.
        instance.random_yes_instance(n)
        print( instance ) 
        instance.exhaustive_search()
    
    
    print(time.clock(), "seconds LAST") # I was testing here, I think this prints the total time it took for all 5 searches 
    print(time.clock()/5, "seconds AVERAGE") # Because the search is run amongst arrays of the same size 5 times, before incrementing the array size by 1, the avg would be the total clock time divided by 5. (Again just testing here)
    

