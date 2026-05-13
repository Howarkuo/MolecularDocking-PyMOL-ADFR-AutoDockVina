#Writes a PyMOL script to remove unwanted structures, executes it, and runs prepare_receptor from the ADFR suite to generate the .pdbqt file.
import subprocess
from config import conf

def main():
    print("Writing PyMOL preprocess script...")
    pymol_script = f"""reinitialize everything
load {conf['receptor_unzip_path']}
remove polymer.nucleic
remove solvent
remove P/*/*
remove */EDO/*
remove */PEG/*
sele */*/CL
alter sele,name='MG'
alter sele,resn='MG'
alter sele,elem='MG'
save {conf['receptor_preprocess_path']}
quit
"""
    with open(conf['receptor_preprocess_script'], "w") as f:
        f.write(pymol_script)

    print("Running PyMOL to preprocess receptor...")
    subprocess.run(["pymol", "-c", conf['receptor_preprocess_script']])

    print("Transforming to .pdbqt format...")
    # Make sure prepare_receptor is in your PATH
    subprocess.run([
        "prepare_receptor", 
        "-r", conf['receptor_preprocess_path'], 
        "-o", conf['receptor_vina'], 
        "-A", "hydrogens"
    ])

if __name__ == "__main__":
    main()
