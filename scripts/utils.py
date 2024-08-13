import os, shutil, requests
from rdkit.Chem import AllChem
from rdkit import Chem


def prepare_output_directory(output):
    """
    Prepare the output directory
    output: str, the output directory
    return: None
    """
    # overwrite the output directory
    # delete the output directory if it exists
    if os.path.exists(output):
        shutil.rmtree(output)
    os.makedirs(output)

def file_to_json_compatible_string(file_path):
    """
    Convert PDB file and sdf file to JSON
    """
    with open(file_path, 'r') as file:
        content_str = file.read()
    return content_str


def is_valid_smiles(smiles):
    """
    Check if the SMILES is valid
    :param smiles: str, SMILES
    :return: mol object if valid, False otherwise
    """
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=True)
        return mol
    except:
        return False


def convert_mols_to_canonical_smiles(mol_list):
    """
    Convert mol objects to canonical SMILES, and remove duplicates
    :param mol_list: list of mol objects
    :return: list of canonical SMILES
    """
    canonical_smiles = set()
    for mol in mol_list:
        canonical_smi = Chem.MolToSmiles(mol, canonical=True)
        canonical_smiles.add(canonical_smi)
    return list(canonical_smiles)


def convert_smiles_to_sdf(smiles_list, output_dir):
    """
    Convert SMILES to SDF
    :param smiles_list: list of smiles
    :param output_dir: str, output directory
    :return: list of sdf file paths
    """

    # get valid smiles
    mol_list = []
    for i, smiles in enumerate(smiles_list):
        mol = is_valid_smiles(smiles)
        if mol:
            mol_list.append(mol)
            print(f"Valid SMILES: {smiles}")
        else:
            print(f"Invalid SMILES: {smiles}")

    # convert to canonical smiles
    valid_canonical_smiles = convert_mols_to_canonical_smiles(mol_list=mol_list)

    if len(valid_canonical_smiles) < len(mol_list):
        print("Some SMILES are duplicates and removed")

    # convert to SDF
    output_files = []
    for i, smiles in enumerate(valid_canonical_smiles):
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        AllChem.UFFOptimizeMolecule(mol)

        # save the clean file to molmim_result

        w = Chem.SDWriter(f"{output_dir}/molecule_{i}.sdf")
        w.write(mol)
        w.close()
        print(f"Converted SMILES to SDF: {smiles}")
        output_files.append(f"{output_dir}/molecule_{i}.sdf")

    return output_files




