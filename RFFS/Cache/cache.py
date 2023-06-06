import os

class cache:
    def __init__(self, cache_name):
        self.evaluate_cache(cache_name)
        return 
    
    #Evaluates if cache exists. Otherwise it creates it
    #In the future, can send memory usage information object
    def evaluate_cache(self, cache_name):
        if os.path.exists(f"./{cache_name}"):
            return 
        else :
            return 

    #TODO: Implement!
    def create_cache(self, cache_name):
        #Make directory named "cache_name"
        #Create directories with dates
        #Create directories with hours
        return 