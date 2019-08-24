from multiprocessing import Pool, cpu_count
import numpy as np

'''
multiprocessing Pool.map with multiple input arguments
'''

N = 1000


def run(params):
    a, b = params
    return np.sin(a) * np.cos(b)


def run_in_parallel():
    a = np.arange(N*N).reshape(N, N)
    b = np.arange(N*N).reshape(N, N)
    with Pool(cpu_count()) as pool:
        ret = pool.map(run, zip(a, b))
    return np.array(ret)


if __name__ == "__main__":
    print("Starting...")
    ret = run_in_parallel()
    print(ret)
    print(ret.shape)
