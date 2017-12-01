import string
alphabet = list(string.ascii_lowercase)
lowerCase = list(string.ascii_lowercase)
upperCase = list(string.ascii_uppercase)
nums = list(string.digits)
charList = lowerCase + nums + ['_']

# keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B',]
# charSet = lowerCase + nums
k = 3


clusterArr = [['locahost:8000', 'locahost:8001', 'locahost:8002'], ['locahost:8003', 'locahost:8004', 'locahost:8005'], ['locahost:8006', 'locahost:8007','localhost:8008']]

def assignKeyRanges(clusterArr, k):

    keyArr = []
    numClusters = 0

    if len(clusterArr) == 0:
        return keyArr

    for i in clusterArr:
        if len(i) == k:
            numClusters = numClusters + 1

    keyRange = 37//numClusters

    if numClusters == 0:
        print("No Clusters")

    elif numClusters == 1:
        keyArr.append(charList[0:37])
        if (len(clusterArr) > 1):
            keyArr.append(['',''])

    else:
        for i in range(0, len(clusterArr)):
            if i == numClusters-1:
                keyArr.append(charList[keyRange*i:37])
            elif i >= numClusters:
                keyArr.append(['',''])
            else:
                keyArr.append(charList[keyRange*i:keyRange*(i+1)-1])
                # keyArr.append([alphabet[keyRange*i], alphabet[keyRange*(i+1)-1]])
                # keyArr[i] = ['a', 'b']


    # print('Number of clusters: ' + str(numClusters) + '\nKey Range: ' + str(keyRange) + '\nKey Array: ' + str(keyArr))

    return keyArr


result = assignKeyRanges(clusterArr, 3)

print("RESULT: ", result)
