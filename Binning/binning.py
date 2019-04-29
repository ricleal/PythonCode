from __future__ import print_function

import math
import unittest

import numpy as np


'''
Tests for SASView Code Camp 2017 Grenoble

Implemented here:
https://github.com/SasView/sasview/blob/master/src/sas/sascalc/dataloader/manipulations.py

'''


class Binning(object):
    '''
    This class just creates a binning object
    either linear or log
    See tests for usage
    '''

    def __init__(self, min_value, max_value, n_bins, base=None):
        '''
        if base is None: Linear binning
        '''
        self.min = min_value
        self.max = max_value
        self.n_bins = n_bins
        self.base = base
        self.bins = self._compute_binning()

    def _compute_binning(self):
        '''
        '''
        if self.base is None:
            return np.linspace(self.min, self.max, self.n_bins)
        else:
            return np.logspace(
                np.log10(self.min),
                np.log10(self.max),
                self.n_bins, base=self.base)

    def get_bin_index(self, value):
        '''
        '''
        index = np.digitize(np.array(value), self.bins)
        return index

    def get_bin_index_log_manual(self, value):
        '''
        This is manual just for testing
        The general formula is:
        bin = floor(N * (log(x) - log(min)) / (log(max) - log(min)))
        '''
        temp_x = self.n_bins * \
            (math.log(value, self.base) - math.log(self.min, self.base))
        temp_y = math.log(self.max, self.base) - math.log(self.min, self.base)
        # Bin index calulation
        i_bin = int(math.floor(temp_x / temp_y))
        return i_bin


class TestBinning(unittest.TestCase):
    '''
    '''

    def test_linear(self):
        '''
        '''
        linear = Binning(0, 10, 11)
        # print(linear.bins)
        self.assertEqual(len(linear.bins), 11)
        self.assertTrue(
            np.array_equal(
                linear.bins,
                np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])
            ))
        # outside of the range
        self.assertEqual(linear.get_bin_index(-1), 0)
        self.assertEqual(linear.get_bin_index(0), 1)
        self.assertEqual(linear.get_bin_index(0.1), 1)
        self.assertEqual(linear.get_bin_index(1.9), 2)
        self.assertEqual(linear.get_bin_index(2.0), 3)
        self.assertEqual(linear.get_bin_index(2.1), 3)
        self.assertEqual(linear.get_bin_index(10), 11)
        # outside of the range
        self.assertEqual(linear.get_bin_index(10.1), 11)

    def test_log_10(self):
        logarithm = Binning(0.1, 1, 10, base=10)
        self.assertTrue(
            np.allclose(
                logarithm.bins,
                np.array(
                    [0.1, 0.12915497, 0.16681005, 0.21544347, 0.27825594,
                     0.35938137, 0.46415888, 0.59948425, 0.77426368, 1.])
            ))
        self.assertEqual(logarithm.get_bin_index(0.2), 3)
        self.assertEqual(logarithm.get_bin_index(0.22), 4)

        self.assertEqual(logarithm.get_bin_index_log_manual(0.00001), -41)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.1), 0)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.2), 3)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.22), 3)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.27), 4)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.5), 6)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.7), 8)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.8), 9)
        self.assertEqual(logarithm.get_bin_index_log_manual(0.9), 9)
        self.assertEqual(logarithm.get_bin_index_log_manual(1.0), 10)


if __name__ == '__main__':
    unittest.main()
