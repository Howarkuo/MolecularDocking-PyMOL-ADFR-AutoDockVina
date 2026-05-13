#Reads the Vina .pdbqt output files, extracts scores and RMSD, filters the best poses (score <= 0), and writes to a summary table and a combined SDF file.
import os
import subprocess
import pandas as pd
import numpy as np
from openbabel import pybel
from config import conf

def main():
    print("Zipping log files...")
    subprocess.run(f"zip -r {conf['log_zip_path']} log/*", shell=True)

    print("Reading zinc2smiles table...")
    df = pd.read_csv(conf['zinc2smiles'])

    print("Merging poses into single SDF...")
    # This assumes output files are stored in an 'output/' folder
    output_files = [os.path.join("output", f) for f in os.listdir("output") if f.endswith(".pdbqt")]
    
    with pybel.Outputfile("sdf", conf['merge_poses_path'], overwrite=True) as poses:
        for path in output_files:
            for mode in pybel.readfile("pdbqt", path):
                res = mode.data["REMARK"].split('RESULT:')[1].split('\n')[0].split(' ')
                res = [x for x in res if x] # filter empty strings
                mode.data["Score"] = res[0]
                mode.data["RMSD_LB"] = res[1]
                mode.data["RMSD_UB"] = res[2]
                
                # Retrieve SMILES string
                smiles_match = df['smiles'][df['zinc_id'] == mode.title].to_list()
                if smiles_match:
                    mode.data["smiles"] = smiles_match[0]
                mode.data["zinc_id"] = mode.title
                poses.write(mode)

    print("Filtering best poses...")
    vina_score = {}
    with pybel.Outputfile("sdf", conf['filter_poses_path'], overwrite=True) as pose:
        for mode in pybel.readfile("sdf", conf['merge_poses_path']):
            zinc_id = mode.data['zinc_id']
            model = int(mode.data['MODEL'])
            score = float(mode.data["Score"])
            
            if model == conf['max_pose'] and score <= conf['max_score']:
                pose.write(mode)
                
            if zinc_id not in vina_score:
                vina_score[zinc_id] = [np.nan for _ in range(9)]
            vina_score[zinc_id][model-1] = score

    print("Generating score table...")
    vina_score_table = pd.DataFrame(vina_score, index=range(1, 10))
    vina_score_table.to_csv(conf['vina_score_table'], index=False)
    
    print("Copying to final ligand.sdf...")
    subprocess.run(["cp", conf['filter_poses_path'], conf['pla_path']])

if __name__ == "__main__":
    main()
