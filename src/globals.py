"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

"""
    Global variables for the entire codebase are initialized here.
    
    Global variables
    --------------------
    :var localIPPort: The localIPPort for this specific instance in the form of IP:PORT (an identifier to query for objects)
    :var VCDict: All IP:PORT values and their associated vector clock values mapped in a global dictionary
    :var nodesList: All the node objects as a single list that exist globally
"""
class CMPS128HW3Settings:
    def __init__(self):
        global localIPPort

        global VCDict
        VCDict = dict()

        global nodesList
        nodesList = []