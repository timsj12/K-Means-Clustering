
import math
from matplotlib import pyplot as plt

color = ["blue", "yellow", "orange", "green"]

filename = 'points2.txt'

# read in file
f = open(filename, 'r')

max_iterations = int(f.readline())
num_patients = int(f.readline())
k = int(f.readline())

initial_index = []
coordinates_str = []

# get index of initial covid patients in list
for i in range(k):
    initial_index.append(int(f.readline()))

# create a list of all patients; patient coordinates are strings
for i in range(num_patients):
    coordinates_str.append((f.readline().strip().split(",")))
print(coordinates_str)

# Convert coordinate string data to integer values
coordinates = []
for i in range(num_patients):
    xy_coord = []
    for j in range(2):
        xy_coord.append(int(coordinates_str[i][j]))
    coordinates.append(xy_coord)
print(coordinates)

# Initial covid patient coordinates
initial_patient = []
for i in range(k):
    centroids = []
    for j in initial_index:
        centroids.append(coordinates[j])
initial_patient = centroids

# initialize previous_cluster to be empty outside of iterating while loop
# 1st loop is empty; subsequent loops will not be
previous_cluster = []
for i in range(k):
    previous_cluster.append([])

counter = 0
while counter <= max_iterations:
    # initialize number of clusters based on number of initial covid patients
    clusters = []
    for i in range(k):
        clusters.append([])

    for i in range(len(coordinates)):
        dist_check = []

        # calculate the distance between centroids and all other points
        for j in range(len(centroids)):
            delta_x = (centroids[j][0] - coordinates[i][0])
            delta_y = (centroids[j][1] - coordinates[i][1])
            r = math.sqrt(delta_x ** 2 + delta_y ** 2)
            dist_check.append(r)

        # place point into cluster associated with its closest centroid
        min_distance = min(dist_check)
        min_distance_index = dist_check.index(min_distance)
        clusters[min_distance_index].append(coordinates[i])

    # check to see if convergence attained
    for i in range(k):
        if len(clusters[i]) == len(previous_cluster[i]):
            convergence = True
        else:
            convergence = False
            break

    # calculate new centroids using sum of x and y values
    if convergence is False:
        counter += 1
        centroids = []
        for i in range(k):
            sum_x = 0
            sum_y = 0
            for j in range(len(clusters[i])):
                sum_x += (clusters[i][j][0])
                sum_y += (clusters[i][j][1])

                mean_x = sum_x / len(clusters[i])
                mean_y = sum_y / len(clusters[i])

            new_centroid = [mean_x, mean_y]
            centroids.append(new_centroid)

        # save clusters to previous clusters for next iteration
        previous_cluster = clusters

        # plots 1st iteration of loop
        if counter == 2:
            for i in range(len(centroids)):
                plt.scatter(centroids[i][0], centroids[i][1], color="red", s=100)
                plt.xlabel("X Coordinates After 1st Iteration")
                plt.ylabel("Y Coordinates After 1st Iteration")

            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                    plt.scatter(clusters[i][j][0], clusters[i][j][1], color=color[i], s=30)

            plt.show()

    else:
        break

# Output
print(f'\nInitial Covid Patients: {initial_patient}\n')

print(f'Iterations to achieve stability: {counter}\n')

print(f'Final Centroids: ')
for i in range(k):
    print(f'{centroids[i]}')

for i in range(k):
    print(f'\n\nNumber of patients in cluster {i}: {len(previous_cluster[i])}')
    for j in range(len(previous_cluster[i])):
        if (j % 12) == 0 & (j != 0):
            print(f'\n{previous_cluster[i][j]}', end=' ')
        else:
            print(f'{previous_cluster[i][j]}', end=' ')
print()
# plot final centroids
for i in range(len(centroids)):
    plt.scatter(centroids[i][0], centroids[i][1], color="red", s=100)
    plt.xlabel("X Coordinates at Convergence")
    plt.ylabel("Y Coordinates at Convergence")

# plot final coordinates
for i in range(len(clusters)):
    for j in range(len(clusters[i])):
        plt.scatter(clusters[i][j][0], clusters[i][j][1], color=color[i], s=30)

plt.show()
