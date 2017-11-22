"""
    Author: Shane Dalton
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

import logging

class CMPS128HW3Gossip:

    def __init__(self):
        pass

    """
        Precondition: two KVSDicts as two dictionaries to be compared and merged appropriately
        :param dict1: The first dictionary to be compared
        :param dict2: The second dictionary to be compared
        :return The dictionary merged
    """
    def merge(self, dict1, dict2):
        for key in dict1:
            logging.info("Value of key in dict1: " + str(key))
            if key in dict2:
                winner = self.compare(dict1[key], dict2[key])
                dict1[key] = winner
            else:
                dict2[key] = dict1[key]
        for key in dict2:
            if key in dict1:
                winner = self.compare(dict1[key], dict2[key])
                dict2[key] = winner
            else:
                dict1[key] = dict2[key]
        return dict1

    """
        Comparing the clock values of each corres[pmdom
        :param key1:
        :param key2:
        :return: The "winner" as a single value
    """
    def compare(self, key1, key2):
        clock1 = int(key1['clock'])
        clock2 = int(key2['clock'])
        if clock1 > clock2:
            return key1
        elif clock1 < clock2:
            return key2
        elif clock1 == clock2:
            # tie break timestamps
            if key1['timestamp'] > key2['timestamp']:
                logging.info("tie breaker", key1['timestamp'], key2['timestamp'])
                return key1
            else:
                return key2