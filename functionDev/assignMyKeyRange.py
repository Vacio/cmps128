def assignMyKeyRange(myIpPort, clusterArr, keyRangeArr):
    myKeyRange = ['not in cluster array']
    print("TEST CLUSTER ARRAY ---->", myIpPort)
    for i in range(0, len(clusterArr)):
        if myIpPort in clusterArr[i]:
            myKeyRange = keyRangeArr[i]

    return myKeyRange
