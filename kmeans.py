##################
# INITIALIZATION ##
##################

# dictionary containing the points in (D) - Key: point | Value: point coordinates
points = {}

# dictionary containing the clusters - Key: cluster | Value: dictionary of points in that cluster
clusters = {}

# dictionary containing the centroids - Key: centroid  | Value: centroid coordinates
centroids = {}


##################
# POINTS METHODS #
##################

def add_points (numPts) :
    for i in range(1, numPts + 1) :
        # reading a new point
        newPt = "A" + str(i)
        print(f"Enter the coordinates of {newPt}:")
        x = int(input("x: "))
        y = int(input("y: "))
        print("----------------------------")
        
        # checking if point already exits
        while point_exists(x, y) == True :
            print("Error: Point already exists!")
            print(f"Enter the coordinates of {newPt}:")
            x = int(input("x: "))
            y = int(input("y: "))
            print("----------------------------")
        
        # adding the point to the dictionary of points
        points[newPt] = [x, y]

def point_exists (x, y) :
    for point in points.values() :
        if point[0] == x and point[1] == y : return True
    return False

def print_points (pointsDict) :
    for key, value in pointsDict.items() :
        print(f"{key} = {value}")


#####################
# CENTROIDS METHODS #
#####################

def add_centroids(numC) :
    for i in range(1, numC + 1) :
        # reading a new centroid
        newCtrd = "M" + str(i)
        print(f"Enter the coordinates of {newCtrd}:")
        x = int(input("x: "))
        y = int(input("y: "))
        print("----------------------------")
        
        # checking if centroid exists in (D) or if centroid already chosen
        while point_exists(x, y) == False or centroid_chosen(x, y) == True :
            if point_exists(x, y) == False : print("Error: Centroid does not exist in (D)")
            else : print("Error: Centroid already chosen!")
            print(f"Enter the coordinates of {newCtrd}:")
            x = int(input("x: "))
            y = int(input("y: "))
            print("----------------------------")
        
        # adding the centroid to the dictionary of centroids
        centroids[newCtrd] = [x, y]

def centroid_chosen (x, y) :
    for centroid in centroids.values() :
        if centroid[0] == x and centroid[1] == y : return True
    return False

def print_centroids (centroidsDict) :
    for key, value in centroidsDict.items() :
        print(f"{key} = {value}")


####################
# CLUSTERS METHODS #
####################

def add_clusters (numClstr) :
    # creating numClstr clusters
    for i in range(1, numClstr + 1) :
        newClstr = "C" + str(i)
        clusters[newClstr] = {"" : []}

def print_clusters (clusterDict) :
    for keyC in clusterDict.keys() :
        print(f"({keyC}): [", end=" ")
        for keyP in clusterDict[keyC].keys() :
            print(keyP, end=" ")
        print("]")

def point_in_cluster (pointKey, clusterKey) :
    for key in clusters[clusterKey].keys() :
        if key == pointKey : return True
    return False

def average_of_cluster_points (clusterKey) :
    sumX = 0
    sumY = 0
    nbPoints = len(clusters[clusterKey].keys())
    for key in clusters[clusterKey].keys() :
        sumX += clusters[clusterKey][key][0]
        sumY += clusters[clusterKey][key][1]
    return [round(sumX / nbPoints, 2), round(sumY / nbPoints, 2)]


####################
# DISTANCE METHODS #
####################

def eucludian_dist (x1, y1, x2, y2) :
    # sqrt(n) is n^(1/2)
    return round( ( (x1 - x2) ** 2 + (y1 - y2) ** 2 ) ** (1/2), 2)

def manhattan_dist (x1, y1, x2, y2) :
    return round( float((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)

def minkowski_dist (x1, y1, x2, y2, q) :
    # qth root of n is n^(1/q)
    return round( ( abs((x1 - x2)) ** q + abs((y1 - y2)) ** q ) ** (1/q), 2)

def dist (x1, y1, x2, y2, q, calcMethod) :
    if calcMethod == 1 : return eucludian_dist(x1, y1, x2, y2)
    elif calcMethod == 2 : return manhattan_dist(x1, y1, x2, y2)
    else : return minkowski_dist(x1, y1, x2, y2, q)

def print_dist_table (pointsDict, centroidsDict, distTable) :
    pointsList = []
    centroidsList = []
    
    for point in pointsDict.values() :
        pointsList.append(point)
    for centroid in centroidsDict.values() :
        centroidsList.append(centroid)
    
    print("Distance Table:")
    print("- - - - - - - -")

    for i in range(-1, len(centroidsDict)) :
        for j in range(-1, len(pointsDict)) :
            if i == -1 :
                if j == -1 : print("##", end="   ")
                else : print(list(pointsDict)[j], end="   ")
            else :
                if j == -1 : print(list(centroidsDict)[i], end="   ")
                else : print(distTable[i][j], end="|")        
        print("")


#####################
# K-means Algorithm #
#####################

def resolve_algo (q, calcMethod, algoIterations) :
    # Algorithm number of iteration
    print("~ ~ ~ ~ ~ ~")
    print(f"Iteration {algoIterations}:")
    print("~ ~ ~ ~ ~ ~")
    print("")
    
    # saving the current cluster dictionary into oldClusters list to be checked if changed later on
    oldClusters = []
    for keyC in clusters.keys() :
        oldClusters.append(keyC)
        for keyP in clusters[keyC].keys() :
            oldClusters.append(keyP)

    # getting values of points and centroids for distance calculation
    pointsList = []
    centroidsList = []
    
    for point in points.values() :
        pointsList.append(point)
    for centroid in centroids.values() :
        centroidsList.append(centroid)

    rows = len(centroidsList)
    cols = len(pointsList)

    # filling the table of distances
    distTable = []
    for i in range(0, rows) :
        distTable.append([])
        for j in range(0, cols) :
            distTable[i].append(dist(pointsList[j][0], pointsList[j][1], centroidsList[i][0], centroidsList[i][1], q, calcMethod))
    
    # printing the table of distances
    print_dist_table(points, centroids, distTable)
    print("")

    # checking minimum distances and filling the minimum distance list: minDist [x,y]
    # which is initialized to the following: x as min dist set to 100 and y as cluster index set to -1
    minDist = [[100, -1]] * cols
    for i in range(0, rows) :
        for j in range(0, cols) :
            if distTable[i][j] < minDist[j][0] : 
                minDist[j] = [distTable[i][j], i]

    # using minDist list we get that the ith element of it represent the ith point in the pointsList which
    # will therefore be transfered to the cluster of index y
    for i in range(0, cols) :
        clusterIndex = minDist[i][1]
        cluster = "C" + str(clusterIndex + 1)
        point = "A" + str(i + 1)
        
        # updating clusters dictionary
        
        # removing point from old cluster
        for key in clusters.keys() :
            if point_in_cluster(point, key) == True :
                clusters[key].pop(point)
                #print(f"Point ({point}) removed from cluster ({key})")
        
        # adding point to new cluster
        clusters[cluster][point] = points[point]
        print(f"{point} --> ({cluster})")
    
    print("")

    print("Updated Clusters: ")
    print_clusters(clusters)
    
    print("")

    # updating centroids dictionary
    print("Updated Centroids:")
    for i in range(0, rows) :
        centroidKey = "M" + str(i + 1)
        clusterKey = "C" + str(i + 1)
        if "" in clusters[clusterKey].keys() : clusters[clusterKey].pop("")
        centroids[centroidKey] = average_of_cluster_points(clusterKey)
        print(f"{centroidKey} = {centroids[centroidKey]}")
    print("-----------------------------------")
    
    # checking if clusters dictionary saved into the list has changed. 
    # If yes: return true and continue | If not: return false and stop the algorithm.
    newClusters = []
    for keyC in clusters.keys() :
        newClusters.append(keyC)
        for keyP in clusters[keyC].keys() :
            newClusters.append(keyP)
    if oldClusters == newClusters :
        print("Nothing changed -> End of Algorithm")
        print("-----------------------------------", end="\n\n")
        print("~ ~ ~ ~ ~ ~ ~")
        print("Final Results:")
        print("~ ~ ~ ~ ~ ~ ~", end="\n\n")
        print("Obtained Clusters: ", end="\n\n")
        print_clusters(clusters)
        print(f"Number of Iterations: {algoIterations}")
        print("-----------------------------------")
        return False
    return True


###############
# MAIN METHOD #
###############

def main() :
    # requesting number of points
    nbPoints = int(input("Enter the number of points in (D): "))
    print("------------------------------------")
    add_points(nbPoints)
    print("Points in (D):")
    print_points(points)
    print("------------------------------------")
    print("")

    # requesting number of clusters
    nbClusters = int(input("Enter the number of clusters: "))
    print("-------------------------------")
    while 1 >= nbClusters or nbClusters > nbPoints : 
        print(f"Error - Condition not satisfied: 1 < Number of Clusters <= {nbPoints}")
        nbClusters = int(input("Enter the number of clusters: "))
        print("-------------------------------")
    add_clusters(nbClusters)

    # choosing the centroids
    print(f"Choose {nbClusters} points from (D) as centroids!")
    add_centroids(nbClusters)
    print("Centroids:")
    print_centroids(centroids)
    print("------------------------------------")
    print("")

    # choosing the distance calculation method
    print("Eucludian: 1 | Manhattan: 2 | Minkowski: 3")
    print("------------------------------------------")
    calcMethod = int(input("Choose the calculation method: "))
    while calcMethod not in [1, 2, 3] :
        print("Error: Invalid option!")
        calcMethod = int(input("Choose the calculation method: "))
    print("------------------------------------------")
    
    # requesting q in case of Minkoswski calculation method
    if calcMethod == 3 :
        q = int(input("Enter q for Minkowski calculation: "))
        while q <= 2 : 
            print("Error - Condition not satisfied: q > 2")
            q = int(input("Enter q for Minkowski calculation: "))
        print("------------------------------------------")
    else : 
        # will passed in the next methods but will not be used
        q = 0

    print("")

    # Kmeans algorithm
    print("---------------------------")
    print("Starting K-means algorithm:")
    print("---------------------------", end="\n\n")
    algoIterations = 1
    while resolve_algo(q, calcMethod, algoIterations) == True :
        algoIterations += 1
        input("Press Enter to continue...")
        print("-----------------------------------")
        print("")
    print("End of Program!")

main()