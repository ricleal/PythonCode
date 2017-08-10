'''

Trying to run multiprocessing inside Mantidplot

It works!

'''
import psutil
import os
from multiprocessing import Pool
from glob import glob
from pprint import pprint
def f(file_path):
    out_ws_name = os.path.basename(file_path)
    LoadEventNexus(
        Filename=file_path,
        OutputWorkspace=out_ws_name,
        MetaDataOnly=True
    )
    out_ws = mtd[out_ws_name]
    events = out_ws.getNEvents()
    DeleteWorkspace(out_ws_name)
    return {'name': out_ws_name, 'events': events }

data_dir = "/SNS/EQSANS/IPTS-19574/nexus"
number_of_cores = psutil.cpu_count()
p = Pool(number_of_cores)

files = glob(os.path.join(data_dir, "EQSANS_862*.nxs.h5"))
results = p.map(f, files)
pprint(results)
