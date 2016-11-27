from __future__ import absolute_import

import numpy as np 
from .graphs import Graph, blocks


class ClusterGraph(Graph):
    """Returns the adjacency matrix for a cluster network via .create().

    The graph can be made fully connected using chaining assumption when 
    chain_blocks=True (default).

    Parameters
    ----------- 
    low : float (0, 1) (default=0.3)
        Lower bound for np.random.RandomState.uniform cluster values.

    high : float (0, 1) > low (default=0.7)
        Upper bound for np.random.RandomState.uniform vluster values.

    n_blocks : int (default=2)
        Number of blocks.  Returned matrix will be square with 
        shape n_block_features * n_blocks.

    chain_blocks : bool (default=True)
        Apply random lattice structure to chain blocks together.

    seed : int
        Seed for np.random.RandomState seed. (default=1)
    """
    def __init__(self, low=0.7, high=0.7, n_blocks=2, chain_blocks=True, 
                 **kwargs):
        self.low = low
        self.high = high
        self.n_blocks = n_blocks
        self.chain_blocks = chain_blocks
        super(ClusterGraph, self).__init__(**kwargs)

    def create(self, n_features, alpha=None):
        """Build a new graph.

        Parameters
        -----------        
        n_features : int 

        [alpha] : float (0,1) 
            Unused.

        Each graph will have a minimum of 
        
            (n_blocks * n_block_features**2 - n_blocks) / 2
        
        edges and exactly this amount if chain_blocks=False.
        
        TODO: We could use alpha to increase/decrease the number of blocks here
              to take advantage of the parameter and test for differing 
              complexity.

        Returns
        -----------  
        (n_features, n_features) matrices: covariance, precision, adjacency 
        """
        n_block_features = int(np.floor(1. * n_features / self.n_blocks))
        if n_block_features * self.n_blocks != n_features:
            raise ValueError(('Error: n_features {} not divisible by n_blocks {}.'
                              'Use n_features = n_blocks * int').format(
                            n_features,
                            self.n_blocks))
            return

        block_adj = (-np.ones((n_block_features, n_block_features)) * 0.5 + 
                     self.prng.uniform(
                        low=self.low,
                        high=self.high,
                        size=(n_block_features, n_block_features)))

        adjacency = blocks(self.prng,
                           block_adj,
                           n_blocks=self.n_blocks,
                           chain_blocks=self.chain_blocks)

        precision = self.to_precision(adjacency)
        covariance = self.to_covariance(precision)
        return covariance, precision, adjacency
