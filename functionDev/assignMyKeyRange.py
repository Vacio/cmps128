def assignMyKeyRange(myIpPort, clusterArr, keyRangeArr):
    myKeyRange = ['not in cluster array']
    for i in range(0, len(clusterArr)):
        if myIpPort in clusterArr[i]:
            myKeyRange = keyRangeArr[i]

    return myKeyRange
