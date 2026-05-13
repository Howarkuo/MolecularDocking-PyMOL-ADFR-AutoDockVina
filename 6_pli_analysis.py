#Uses the custom PLI.analysis module (needs to be downloaded from GitHub ) to calculate the Protein-Ligand Interaction and generate the score.h5 HDF5 file.  
import warnings; warnings.filterwarnings('ignore')
import sys
import multiprocessing as mp
import pandas as pd
from config import conf

# Append module path to import PLI
sys.path.append('../module/')
try:
    from PLI import analysis
except ImportError:
    print("Error: PLI module not found. Please ensure it is cloned into the mydock/module/PLI directory.")
    sys.exit(1)

def main():
    print("Preparing Ligands and Receptor for PLI Analysis...")
    ligands, ligandlist = analysis.get_vina_result(conf['pla_path'])
    prot, segid = analysis.protein_initialize(conf['receptor_unzip_path'])
    
    atomlist = analysis.get_atomlist(prot)
    d_rid_table = analysis.get_rid_table(atomlist)

    # Note: On MacOS, python 3.8+ switched the default multiprocessing method to "spawn".
    # Ensure PLI/analysis.py uses mp.get_context('fork') to prevent ProcessPoolExecutor errors.
    print("Calculating interactions...")
    ligAtomList, interactionList = analysis.interaction_analysis(
        ligandlist, d_rid_table, prot, cpu=conf['cpu']
    )

    print("Generating score.h5...")
    analysis.write_h5file(
        conf['h5file_filepath'], 
        atomlist, 
        ligands, 
        ligAtomList, 
        interactionList
    )
    
    print("Analysis complete. HDF5 file generated.")

if __name__ == "__main__":
    main()
