# config.py

conf = {
    # 0_Input
    'receptor_link': 'https://files.rcsb.org/download/5DFF.pdb1.gz',
    'ligand_link': 'https://zinc20.docking.org/substances/subsets/fda.sdf', # FDA subset
    'receptor_out': 'receptor.pdb',
    'ligand_out': 'ligands_download.sdf',
    'vina_config_path': 'autodock.conf',
    
    # 1_ReceptorPreprocess
    'receptor_unzip_path': 'receptor.pdb',
    'receptor_preprocess_script': 'receptor_preprocess.pml',
    'receptor_preprocess_path': 'receptor_preprocess.pdb',
    'receptor_vina': 'receptor.pdbqt',
    
    # 2_LigandPrepare
    'ligand_download': 'ligands_download.sdf',
    'ligand_title': 'ligands_title.sdf',
    'ligand_filter': 'ligands_filter.sdf',
    'ligand_duplicate': 'ligands_duplicate.sdf',
    'ligand_addh': 'ligands_addh.sdf',
    'ligand_optimized': 'ligands_opti.sdf',
    'ligand_conformer': 'ligands_conf.sdf',
    'ligand_vina': 'ligands.pdbqt',
    'zinc2smiles': 'zinc2smiles.csv',
    'max_size': 500,
    'nconf': 8,
    
    # 3_FolderSplit & 4_RunDocking
    'cpu': 48,
    'slurm_script_path': 'dock.slurm',
    'folder': 10, # Number of folders to split into
    
    # 5_DockingFilter
    'merge_poses_path': 'merge_poses.sdf',
    'filter_poses_path': 'filter_poses.sdf',
    'vina_score_table': 'vina_score.csv',
    'pla_path': 'ligands.sdf',
    'max_pose': 1,
    'max_score': 0,
    
    # 6_PliAnalysis
    'h5file_filepath': 'score.h5',
    'log_zip_path': 'pli_log.zip'
}

vina_config_content = """size_x = 28.0
size_y = 21.0
size_z = 32.0
center_x = 13.0
center_y = -51.5
center_z = 6.0
exhaustiveness = 16"""
