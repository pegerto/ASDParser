from dataclasses import dataclass

@dataclass
class AllostericSite:
    modulator_name: str
    site_residues: str
    
    @staticmethod
    def from_xml_obj(xml):
        return AllostericSite(
            modulator_name = xml.Modulator_Name.cdata,
            site_residues = xml.Allosteric_Site_Residue.cdata
        )

@dataclass
class PDB:
    id: str
    pdb_url: str
    has_ligand: bool

    @staticmethod
    def from_xml_obj(xml):
        return PDB(
                id=xml.PDB_ID.cdata,
                pdb_url=xml.PDB_URL.cdata if 'PDB_URL' in xml else None,
                has_ligand=bool(xml.Has_Ligand.cdata))

@dataclass
class PTM:
    position: int
    type: str

    @staticmethod
    def from_xml_obj(xml):
        return PTM(
                position=int(xml.Position.cdata),
                type=xml.PTM_Type.cdata)
    
@dataclass
class ASDProtein:
    """Item on the ASD database"""
    id: str
    organism: str
    allosteric_sites: list
    uniprot_id: str
    inhibitors: list
    activators: list
    regulators: list
    pdbs: list
    ptms: list
        
    @staticmethod
    def from_xml_obj(xml):
        # Select allosteric sites
        allosteric_sites = []
        if 'Allosteric_Site_List' in xml.Organism_Record:
            allosteric_sites = [AllostericSite.from_xml_obj(item) for item in xml.Organism_Record.Allosteric_Site_List.children]
        
        # modulators
        modulators =  [(item.ASD_ID.cdata,item.Modulator_Feature.cdata) for item in  xml.Organism_Record.Modulator_List.children] if 'Modulator_List' in xml.Organism_Record else []
       
        # pdbs
        pdbs = [PDB.from_xml_obj(item) for item in xml.Organism_Record.PDB_List.children]
        
        # ptms
        ptms = []
        if 'PTM_List' in xml.Organism_Record:
            ptms = [PTM.from_xml_obj(item) for item in xml.Organism_Record.PTM_List.children]
        
        return ASDProtein(id = xml.Organism_Record.Organism_ID.cdata, 
                   organism = xml.Organism_Record.Organism.cdata,
                   uniprot_id = xml.Organism_Record.UniProt_ID.cdata if 'UniProt_ID' in xml.Organism_Record else None,
                   allosteric_sites = allosteric_sites,
                   inhibitors = [item[0] for item in modulators if item[1] == 'Inhibitor'],
                   activators = [item[0] for item in modulators if item[1] == 'Activator'],
                   regulators = [item[0] for item in modulators if item[1] == 'Regulator'],
                   pdbs=pdbs,
                   ptms=ptms)
