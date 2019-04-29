
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from time import sleep

'''
K means algorithm
visualisation how it evolves with time
'''


class KMeans(object):

    def __init__(self, points, k):
        '''points - 2D np array
        k - number of clusters'''
        self.points = self._normalise_to_one(points)
        self.ks = np.random.rand(k, 2)
        self.k_map = {i: [] for i, _ in enumerate(self.ks)}
        self._init_plot()

    def __del__(self):
        plt.close()

    def _normalise_to_one(self, x):
        return (x - x.min()) / (np.ptp(x))

    def _init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.cluster_color = cm.rainbow(np.linspace(0, 1, len(self.ks)))
        plt.ion()
        plt.show()

    def update_plot(self):
        self.ax.clear()
        for (k_idx, points), c in zip(self.k_map.items(), self.cluster_color):
            x, y = np.array(points).T
            self.ax.scatter(x, y, c=c)
            x, y = self.ks[k_idx]
            self.ax.scatter(x, y, c=c, marker='^', edgecolors='black')
        # update the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def distance_to_k(self):
        '''distance between the centre of the clusters k and the points
        coumns are the centroids of the clusters'''
        distance_matrix = np.empty([len(self.points), len(self.ks)])
        for idx, k in enumerate(self.ks):
            dist = (self.points - k)**2
            dist = np.sqrt(np.sum(dist, axis=1))
            distance_matrix[:, idx] = dist
        return distance_matrix

    def find_belonging_k(self, distance_matrix):
        '''finds the cluster center closer to each point.
        return a list with the corresponding k index'''
        return np.argmin(distance_matrix, axis=1)

    def update_cluster_centroids(self, closest_clusters_idx):
        self.k_map = {i: [] for i, _ in enumerate(self.ks)}
        for point_idx, cluster_idx in enumerate(closest_clusters_idx):
            self.k_map[cluster_idx].append(list(self.points[point_idx]))

    def find_new_centroid_positions(self):
        for k_idx, points in self.k_map.items():
            new_k = np.average(points, axis=0)
            self.ks[k_idx] = new_k

    def run(self):
        '''
        while clusters are diferent
        '''

        while True:
            ks_old = self.ks.copy()

            distance_to_k = self.distance_to_k()
            closest_clusters_idx = self.find_belonging_k(distance_to_k)
            self.update_cluster_centroids(closest_clusters_idx)
            self.find_new_centroid_positions()

            self.update_plot()
            sleep(0.5)
            if (ks_old == self.ks).all():
                break

        plt.show()


if __name__ == "__main__":
    np.random.seed(2)

    # cluster are random points
    K = 5
    N = 50  # N points to cluster
    points = np.random.randint(1, high=7, size=(N, 2)) + np.random.rand(N, 2)
    km = KMeans(points, K)
    km.run()
    del km

    # define clusters as gaussian distributions
    points = np.empty([0, 2])
    points = np.append(points, np.random.multivariate_normal(
        [0.1, 0.1], [[0.01, 0], [0, 0.01]], 50), axis=0)
    points = np.append(points, np.random.multivariate_normal(
        [0.2, 0.9], [[0.01, 0], [0, 0.01]], 50), axis=0)
    points = np.append(points, np.random.multivariate_normal(
        [0.9, 0.9], [[0.005, 0], [0, 0.1]], 150), axis=0)
    km = KMeans(points, 3)
    km.run()
    del km
