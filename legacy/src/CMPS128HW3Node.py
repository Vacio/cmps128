"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

import logging

"""
    Node object with class variables as identifiers for what the node is.
    :var IPPort: The IP:Port value for the associated Node
    :var status: The status of the Node (will be initialized to "up" or "down", dependent on pinging and network
        partitions
    :var role: The role, either a "replica" or "proxy", as 
    :var VC_value: The single digit vector clock value for this node (increment MY value position)
    
    Methods
    -----------
    set_IPPort()
    get_IPPort()
    set_proxy()
    set_replica()
    get_role()
    change_status_down()
    change_status_up()
    increment_vector()
    get_vector()
"""
# TODO: Create interface for this file
class CMPS128HW3Node:
    # Initialization of the IP:PORT value, declared globally for this node
    def __init__(self):
        self.IPPort = None
        self.status = "up"
        self.role = None

    """
        Set the IP:Port value as a string
        :return: void
    """
    def set_IPPort(self, IPPort):
        self.IPPort = IPPort
        logging.debug("Value of IP:PORT for this node: " + str(self.IPPort))

    """
        Return the IP:Port value as a string
        :return: IP:Port value
    """
    def get_IPPort(self):
        logging.debug("Value of IP:PORT for this node: " + str(self.IPPort))
        return self.IPPort

    """
        Set the role of this node to be a proxy.
        :return: void
    """
    def set_proxy(self):
        self.role = "proxy"
        logging.debug("Role of this node: " + self.role)

    """
        Set the role of this node to be a replica.
        :return: void    
    """
    def set_replica(self):
        self.role = "replica"
        logging.debug("Role of this node: " + self.role)

    """
        Get the role of this node.
        :return: "replica" or "proxy" as a string
    """
    def get_role(self):
        logging.debug("Role of this node: " + self.role)
        return self.role

    """
        Change the status of the node to be "down" when pinged.
        :return: void
    """
    def change_status_down(self):
        self.status = "down"
        logging.debug("Status of this node: " + self.status)

    """
        Change the status of the node to be "up" when pinged.
        :return: void
    """
    def change_status_up(self):
        self.status = "up"
        logging.debug("Status of this node: " + self.status)

    """
        Increment the single vector value when the state of the node is changed (when a PUT request is made).
        :return: void
    """
    def increment_vector(self):
        self.VC_value = self.VC_value + 1
        logging.debug("Incremented vector clock value for this node: " + str(self.VC_value))

    """
        Return the single value vector clock value of the node.
        :return: Single digit VC value
    """
    def get_vector(self):
        logging.debug("Current value of this node's vector clock: " + str(self.VC_value))
        return self.VC_value