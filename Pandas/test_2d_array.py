import pandas as pd
import numpy as np

'''

d.main.values[i,j]
d.main.errors[i,j]
d.wing.values[i,j]

'''
class Array(object):
    def __init__(self,df,detector_name,field,shape):
        v = df[("name"=detector_name)][field].values
        self.data = np.reshape(shape)
    def __getitem__(self, i,j):
        return self.data[i,j]



class Data(object):
    def __init__(self):
        self.df = None

    def setup(self):
        shape = (256,192)
        ny, nx = shape
        size = nx * ny
        data = np.random.rand(nx, ny)
        errors = np.sqrt(data)
        xv, yv = np.meshgrid(range(nx), range(ny))
        d = {'name' : np.full(size,"main",dtype=np.dtype((str, 4))), # detetor name
            'i' : xv.ravel(),
            'j' : yv.ravel(),
            'value' : data.ravel(),
            'errors' : errors.ravel()
        }
        self.df = pd.DataFrame(d)
        self.df.info()

        setattr(Data,)


def main():
    d = Data()
    d.setup()

if __name__ == '__main__':
    main()
