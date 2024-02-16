import numpy as np


class KNNClassifier:
    """
    K-neariest-neighbor classifier using L1 loss
    """

    def __init__(self, k=1):
        self.k = k

    def fit(self, X, y):
        self.train_X = X
        self.train_y = y

    def predict(self, X, n_loops=0):
        """
        Uses the KNN model to predict clases for the data samples provided

        Arguments:
        X, np array (num_samples, num_features) - samples to run
           through the model
        num_loops, int - which implementation to use

        Returns:
        predictions, np array of ints (num_samples) - predicted class
           for each sample
        """

        if n_loops == 0:
            distances = self.compute_distances_no_loops(X)
        elif n_loops == 1:
            distances = self.compute_distances_one_loops(X)
        else:
            distances = self.compute_distances_two_loops(X)

        if len(np.unique(self.train_y)) == 2:
            return self.predict_labels_binary(distances)
        else:
            return self.predict_labels_multiclass(distances)

    def compute_distances_two_loops(self, X):
        """
        Computes L1 distance from every sample of X to every training sample
        Uses simplest implementation with 2 Python loops

        Arguments:
        X, np array (num_test_samples, num_features) - samples to run

        Returns:
        distances, np array (num_test_samples, num_train_samples) - array
           with distances between each test and each train sample
        """

        n_test = X.shape[0]
        n_train = self.train_X.shape[0]
        distances = np.zeros((n_test, n_train))

        for i in range(n_train):
            for j in range(n_test):
                distances[j][i] = sum(abs(self.train_X[i] - X[j]))

        return distances

    def compute_distances_one_loop(self, X):
        """
        Computes L1 distance from every sample of X to every training sample
        Vectorizes some of the calculations, so only 1 loop is used

        Arguments:
        X, np array (num_test_samples, num_features) - samples to run

        Returns:
        distances, np array (num_test_samples, num_train_samples) - array
           with distances between each test and each train sample
        """
        n_test = X.shape[0]
        n_train = self.train_X.shape[0]
        distances = np.zeros((n_test, n_train))

        for i in range(n_test):
            distances[i] = np.sum(np.abs(self.train_X - X[i]), axis=1)
        return distances

    def compute_distances_no_loops(self, X):
        """
        Computes L1 distance from every sample of X to every training sample
        Fully vectorizes the calculations using numpy

        Arguments:
        X, np array (num_test_samples, num_features) - samples to run

        Returns:
        distances, np array (num_test_samples, num_train_samples) - array
           with distances between each test and each train sample
        """


        
        raw = self.train_X[np.newaxis, :, :] - X[:, np.newaxis, :]

        distance = np.linalg.norm(raw, axis=2, ord=1)

        return distance

    def predict_labels_binary(self, distances):
        """
        Returns model predictions for binary classification case

        Arguments:
        distances, np array (num_test_samples, num_train_samples) - array
           with distances between each test and each train sample
        Returns:
        pred, np array of bool (num_test_samples) - binary predictions 
           for every test sample
        """

        n_train = distances.shape[1]
        n_test = distances.shape[0]
        prediction = np.zeros(n_test)

        for j in range(n_test):

            closest_n = []
            dist = np.argsort(distances[j])[:self.k]
            closest_n = self.train_y[dist]
            prediction = np.argmax(np.bincount(closest_n))

        return prediction

    def predict_labels_multiclass(self, distances):
        """
        Returns model predictions for multi-class classification case

        Arguments:
        distances, np array (num_test_samples, num_train_samples) - array
           with distances between each test and each train sample
        Returns:
        pred, np array of int (num_test_samples) - predicted class index 
           for every test sample
        """

        n_train = distances.shape[1]
        n_test = distances.shape[0]
        prediction = np.zeros(n_test)

        for j in range(n_test):

            closest_n = []
            closest_n = self.train_y[np.argsort(distances[j])[:self.k]]
            prediction[j] = np.argmax(np.bincount(closest_n))

        return prediction
