import logging as log
import sys, string

# parse external file into dictionary
def filetodict(filename):
    adjective_dict = {}

    #look for an easier way to load the dictionary
    #for now parse the lines and eliminate the separators
    
    for x in open(filename):
        #split the file at the EOL
        x = x.replace('\n', '')    

        z = x[0:x.find(':')].replace(':', '')      
        w = x[x.find(':'):len(x)].replace(':', '').replace(' ', '') 
        #load each pair adjective: value from the parsed entry in the file    
        adjective_dict[z] = int(w)

    log.debug(adjective_dict)
                  
    return adjective_dict
