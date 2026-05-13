#Downloads the PDB file, extracts it, downloads the SDF file, and writes the AutoDock configuration.

import os
import subprocess
from config import conf, vina_config_content

def main():
    print("Downloading Ligands from ZINC20...")
    subprocess.run(["wget", "-nc", conf['ligand_link'], "-O", conf['ligand_out']])

    print("Downloading Receptor from PDB...")
    gz_file = conf['receptor_link'].split('/')[-1]
    subprocess.run(["wget", "-nc", conf['receptor_link']])
    
    # Unzip .gz file
    with open(conf['receptor_out'], "w") as outfile:
        subprocess.run(["gunzip", "-c", gz_file], stdout=outfile)

    print("Writing AutoDock Vina config...")
    with open(conf['vina_config_path'], "w") as f:
        f.write(vina_config_content)

if __name__ == "__main__":
    main()
