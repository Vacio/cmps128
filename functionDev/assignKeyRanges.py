import string
alphabet = string.ascii_lowercase
keys = ['a','c','e','g','i','j','l','n','p','r','t','v','x','z']
k = 3


clusterArr = [['locahost:8000', 'locahost:8001', 'locahost:8002'], ['locahost:8003', 'locahost:8004', 'locahost:8005'], ['locahost:8006', 'locahost:8007']]

def assignKeyRanges(clusterArr, k):

    keyArr = []
    numClusters = 0

    if len(clusterArr) == 0:
        return keyArr

    for i in clusterArr:
        if len(i) == k:
            numClusters = numClusters + 1

    keyRange = 26//numClusters

    if numClusters == 0:
        print("No Clusters")

    elif numClusters == 1:
        keyArr.append(['a','z'])
        keyArr.append(['',''])

    else:
        for i in range(0, len(clusterArr)):
            if i == numClusters-1:
                keyArr.append([alphabet[keyRange*i], alphabet[25]])
            elif i >= numClusters:
                keyArr.append(['',''])
            else:
                keyArr.append([alphabet[keyRange*i], alphabet[keyRange*(i+1)-1]])
                # keyArr[i] = ['a', 'b']


    # print('Number of clusters: ' + str(numClusters) + '\nKey Range: ' + str(keyRange) + '\nKey Array: ' + str(keyArr))

    return keyArr


result = assignKeyRanges(clusterArr, 3)

print("RESULT: ", result)
