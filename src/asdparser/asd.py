import os 
import untangle
import pandas as pd

from .model import ASDItem

class AsdDB: 
    def __init__(self, directory):
        self.dir = directory
        self.items = {}

        for file in os.listdir(self.dir ):
            file_path = f'{self.dir }/{file}'
            obj = untangle.parse(file_path)
            item = ASDItem.from_xml_obj(obj)
            self.items[item.id] = item
    
    def get(self,id):
        return self.items[id]
    
    def to_df(self):
        data = [[iid, 
                 self.items[iid].organism, 
                 self.items[iid].uniprot_id,
                 len(self.items[iid].allosteric_sites),
                 len(self.items[iid].inhibitors),
                 len(self.items[iid].activators),
                 len(self.items[iid].regulator)] for iid in self.items]
        
        return pd.DataFrame(data, 
                            columns=['id','organism', 'uniprot', 'n_allosteric_sites','inihibitors', 'activators', 'regulators']) 