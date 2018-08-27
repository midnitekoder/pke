# -*- coding: utf-8 -*-

""" Abstract base class for Supervised models. """

from __future__ import division
from __future__ import absolute_import

import os
import pickle
import numpy as np
from pke.base import LoadFile
from sklearn.preprocessing import MinMaxScaler

class SupervisedLoadFile(LoadFile):
    """ The SupervisedLoadFile class that provides extra base functions for
        supervised models. """

    def __init__(self, input_file=None, language='english'):
        """ Redefining initializer. """

        super(SupervisedLoadFile, self).__init__(input_file=input_file,
                                                 language=language)

        self.instances = {}
        """ The instances container. """


    def feature_scaling(self):
        """ Scale features to [0,1]. """

        candidates = self.instances.keys()
        X = [np.array(self.instances[u]) for u in candidates]
        X = np.matrix(X)
        X = MinMaxScaler().fit_transform(X)
        for i, candidate in enumerate(candidates):
            self.instances[candidate] = X[i]


    def feature_extraction(self):
        """ Skeletton for feature extraction. """
        pass


    def classify_candidates(self, model=None):
        """ Classify the candidates as keyphrase or not keyphrase.

            Args:
                model (str): the path to load the model in pickle format,
                    default to None.
        """

        # set the default model if none provided
        if model is None:
            instance = self.__class__.__name__
            model = os.path.join(self._models, instance+"-semeval2010.pickle")

        # load the model
        with open(model, 'rb') as f:
            clf = pickle.load(f)

        # get matrix of instances
        candidates = self.instances.keys()
        X = [self.instances[u] for u in candidates]

        # classify candidates
        y = clf.predict_proba(X)

        for i, candidate in enumerate(candidates):
            self.weights[candidate] = y[i][1]


    def candidate_weighting(self):
        """ Extract features and classify candidates with default parameters."""
        
        self.feature_extraction()
        self.classify_candidates()

