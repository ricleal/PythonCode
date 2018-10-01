from collections import OrderedDict
from datetime import datetime


class Log(OrderedDict):

    def append(self, value):
        '''
        Appends a string.
        The key will be the insertion time
        the value the string
        '''
        self[datetime.now()] = value
    
    def search(self, key):
        '''
        Searches for a string in the key
        if the key is datetime searches the value content
        '''
        found = OrderedDict()
        for k, v in self.items():
            if type(k) is not datetime:
                if key.lower() in k.lower():
                    found[k]=v
            else:
                if key.lower() in v['value'].lower():
                    found[k]=v
        return self._dump_dictionary(found)

    def __setitem__(self, key, value):
        '''
        The entry type will be:

        dict[key] = {
            "value": value,
            "timestamp": datetime.now()
        }
        '''
        OrderedDict.__setitem__(self, key, {
            "value": value,
            "timestamp": datetime.now()})
    
    def __getitem__(self,key):
        value = OrderedDict.__getitem__(self, key)
        return value['value']
    
    @staticmethod
    def _dump_dictionary(d):
        '''
        Return a string with a user friendly version of the dictionary
        '''
        s = [
            "{0:%Y-%m-%d %H:%M:%S} :: {1} = {2}".format(
                v['timestamp'], k, v['value']) if type(k) is not datetime \
            else "{0:%Y-%m-%d %H:%M:%S} :: {1}".format(
                v['timestamp'], v['value']) for k, v in d.items()
        ]
        return "\n".join(s)


    def __str__(self):
        return self._dump_dictionary(self)
    
    def workspace_to_log(self, ws):
        '''
        Adds workspace log into this log
        This only works for Mantid
        '''
        r = ws.getRun()
        l = r.getLogData()
        for i in l:
            if i.dtype().startswith('f'):
                self[i.name] = float(i.value)
            else:
                self[i.name] = i.value


l = Log()
l.append("Calling the beam center...")
# Calling the routine...
l['beam_center_x'] = 1.01212
l['beam_center_y'] = 2.32323

l.append("Printing the log contents...")
print(l)

print("** Searching for the beam center..")
res = l.search("beam_center")
print(res)

print("The beam center x,y is", l['beam_center_x'], l['beam_center_y'])

try:
    # Make sure you are in MantidPlot
    import mantid
    l = Log()
    l.append("Running LoadSpice2D..")
    LoadSpice2D(
        Filename="/HFIR/CG2/IPTS-0/exp205/Datafiles/CG2_exp205_scan0001_0002.xml",
        OutputWorkspace='ws')
    ws = mtd['ws']   
    l.workspace_to_log(ws)
    print("** Printing the Logs..")
    print(l)
except ImportError:
    pass # Nope