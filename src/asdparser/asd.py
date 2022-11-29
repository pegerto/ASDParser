import os 
import untangle
import pandas as pd

from .model import ASDProtein

class AsdDB: 
    def __init__(self, directory):
        self.dir = directory
        self.proteins = {}

        for file in os.listdir(self.dir ):
            file_path = f'{self.dir }/{file}'
            obj = untangle.parse(file_path)
            protein = ASDProtein.from_xml_obj(obj)
            self.proteins[protein.id] = protein
    
    def get(self,id):
        return self.proteins[id]
    
    def to_df(self):
        data = [[iid, 
                 self.proteins[iid].organism, 
                 self.proteins[iid].uniprot_id,
                 len(self.proteins[iid].allosteric_sites),
                 len(self.proteins[iid].inhibitors),
                 len(self.proteins[iid].activators),
                 len(self.proteins[iid].regulator),
                 len(self.proteins[iid].pdbs),
                 len(self.proteins[iid].ptms)] for iid in self.proteins]
        
        return pd.DataFrame(data, 
                            columns=['id','organism', 'uniprot', 'n_allosteric_sites','inihibitors', 'activators', 'regulators', 'pdbs', 'ptms']) 