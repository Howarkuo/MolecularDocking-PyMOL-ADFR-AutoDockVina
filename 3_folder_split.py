#Splits the large .pdbqt file into individual files and sets up the SLURM bash script. Note: The actual Vina execution requires setting the correct path to your local Autodock Vina binary.  

import os
import subprocess
from config import conf

def main():
    print("Writing Slurm script...")
    slurm_script = f"""#!/bin/bash
#SBATCH --partition=xeon
#SBATCH --job-name=docking_test
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task={conf['cpu']}
#SBATCH --time=0-24:00:00

mkdir -p input output log

for ligand in `ls input/`
do
    echo "Docking $ligand..."
    # IMPORTANT: Update this path to your actual vina executable
    vina --receptor receptor.pdbqt \\
         --ligand input/$ligand \\
         --config autodock.conf \\
         --out output/$ligand \\
         --seed 1 --cpu {conf['cpu']} > log/${{ligand}}.log
done
"""
    with open(conf['slurm_script_path'], "w") as f:
        f.write(slurm_script)

    print("Splitting ligands...")
    os.makedirs("ligands", exist_ok=True)
    subprocess.run(["obabel", conf['ligand_vina'], "-opdbqt", "-O", f"./ligands/{conf['ligand_vina']}", "-m"])

    # At this point in the notebook pipeline, files are copied to specific 
    # parallel directories (dock_00, dock_01, etc.) to be submitted.
    print("Ligands split successfully into /ligands/ directory. Ready for docking submission.")

if __name__ == "__main__":
    main()
