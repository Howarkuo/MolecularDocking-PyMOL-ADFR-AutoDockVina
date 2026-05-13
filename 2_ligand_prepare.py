#Uses openbabel to label zinc IDs, filter by weight, remove duplicates, add hydrogens at pH 7.0, generate conformers, minimize geometry, and export to .pdbqt and a SMILES mapping CSV.  

import subprocess
import pandas as pd
from openbabel import pybel
from config import conf

def main():
    print("Adding zinc_id to title...")
    with pybel.Outputfile("sdf", conf['ligand_title'], overwrite=True) as out_sdf:
        for m in pybel.readfile("sdf", conf['ligand_download']):
            m.title = m.data.get('zinc_id', m.title)
            out_sdf.write(m)

    print("Filtering molecular weight < 500...")
    subprocess.run(["obabel", conf['ligand_title'], "-O", conf['ligand_filter'], "--filter", f"MW<{conf['max_size']}"])

    print("Removing duplicates...")
    subprocess.run(["obabel", conf['ligand_filter'], "-O", conf['ligand_duplicate'], "--unique"])

    print("Adding hydrogens (pH 7.0)...")
    subprocess.run(["obabel", conf['ligand_duplicate'], "-O", conf['ligand_addh'], "-p", "7.0"])

    print("Generating conformers...")
    subprocess.run(["obabel", conf['ligand_addh'], "-O", conf['ligand_conformer'], "--conformer", "--nconf", str(conf['nconf']), "--score", "energy"])

    print("Optimizing geometry / Minimizing energy...")
    with open(conf['ligand_optimized'], "w") as out:
        subprocess.run(["obminimize", "-o", "sdf", conf['ligand_addh']], stdout=out)

    print("Converting to .pdbqt...")
    subprocess.run(["obabel", conf['ligand_optimized'], "-O", conf['ligand_vina']])

    print("Creating zinc_id to smiles map...")
    zinc2smiles = {'zinc_id': [], 'smiles': []}
    for m in pybel.readfile("sdf", conf['ligand_optimized']):
        zinc2smiles['zinc_id'].append(m.data.get('zinc_id'))
        zinc2smiles['smiles'].append(m.data.get('smiles'))
    pd.DataFrame(zinc2smiles).to_csv(conf['zinc2smiles'], index=False)

if __name__ == "__main__":
    main()
