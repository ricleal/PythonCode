'''


'''

from pymongo import MongoClient


class DB(object):
    '''
    '''
    def __init__(self,instrument_name, db_name = 'temp'):
        '''
        '''
        client = MongoClient() # localhost
        self.db = client[db_name]
        self.track = self.db[instrument_name] # collection
    
    def find(self,**params):
        result = self.track.find_one(params)
        if result is not None:
            return  result.get('output_file')
        else:
            return None
    
    def insert (self,**params):
        self.track.insert_one(params)

    def __del__(self):
        '''
        Drop the collection on exit just for testing
        '''
        self.track.drop()

db = DB(instrument_name='seq', db_name = 'temp')


def process(input_file, param1, param2, param3):
    '''
    Original processing routine
    '''
    print 'Processing:', locals()
    return "output_file"+str(param1)+str(param2)+str(param3)


def process_wrapper(input_file, param1, param2, param3):
    '''
    Wrapper to the original routine
    '''
    params =  locals()
    res = db.find(**params)
    if res is not None:
        print 'Already in the DB: ', params, res
        return res
    else:
        print 'Does not exist in the DB', params
        output_file = process(**params)
        params.update({'output_file':output_file})
        db.insert(**params)
        return output_file


if __name__ == '__main__':
    
    print '1st processing:'
    output_file1 = process_wrapper(input_file='input_file1', param1=1, param2=2, param3=3)
    output_file2 = process_wrapper(input_file='input_file1', param1=3, param2=4, param3=5)
    print  output_file1, output_file2
    
    print '2nd processing:'
    output_file1 = process_wrapper(input_file='input_file1', param1=1, param2=2, param3=3)
    output_file2 = process_wrapper(input_file='input_file1', param1=3, param2=4, param3=5)
    print  output_file1, output_file2
    
    
    
    
    