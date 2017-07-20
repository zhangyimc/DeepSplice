from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow.python.platform import gfile
import collections
import csv
import os
import numpy as np

Dataset = collections.namedtuple('Dataset', ['data'])

def load_csv_with_header(filename, features_dtype):
	with gfile.Open(filename) as csv_file:
		data_file = csv.reader(csv_file)
		header = next(data_file)
		n_samples = int(header[0])
		n_features = int(header[1])
		data = np.zeros((n_samples, n_features), dtype=features_dtype)
		for i, row in enumerate(data_file):
			data[i] = np.asarray(row, dtype=features_dtype)

	return Dataset(data=data)
