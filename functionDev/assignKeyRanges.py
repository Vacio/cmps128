import string
alphabet = string.ascii_lowercase
keys = ['a','c','e','g','i','j','l','n','p','r','t','v','x','z']
k = 3

keyArr = []

view = ['locahost:8000', 'locahost:8001', 'locahost:8002', 'locahost:8003', 'locahost:8004', 'locahost:8005', 'locahost:8006', 'locahost:8007']

#create clusters

clusterArr = [['locahost:8000', 'locahost:8001', 'locahost:8002'], ['locahost:8003', 'locahost:8004', 'locahost:8005'], ['locahost:8006', 'locahost:8007']]

numClusters = 0
for i in clusterArr:
    if len(i) == k:
        numClusters = numClusters + 1

keyRange = 26//numClusters

if numClusters == 0:
    print("No Clusters")

elif numClusters == 1:
    keyArr[0] = ['a','z']

else:
    for i in range(0, len(clusterArr)):
        if i == numClusters-1:
            keyArr.append([alphabet[keyRange*i], alphabet[25]])
        elif i >= numClusters:
            keyArr.append(['',''])
        else:
            keyArr.append([alphabet[keyRange*i], alphabet[keyRange*(i+1)-1]])
            # keyArr[i] = ['a', 'b']


print('Number of clusters: ' + str(numClusters) + '\nKey Range: ' + str(keyRange) + '\nKey Array: ' + str(keyArr))
