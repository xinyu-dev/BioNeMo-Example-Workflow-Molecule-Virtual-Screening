from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class NIM(ABC):
    """
    Abstract class for a protein folding model in NIM
    """
    # init
    def __init__(self, base_url: str, **kwargs):
        """
        Initialize the protein folding model
        base_url: str, the base url of the protein folding model, e.g. "http://localhost:8000"
        """
        self.base_url = base_url
        self.health_check_url = None # each model has its own health check url
        self.kwargs = kwargs


    def clean_url(self, url: str) -> str:
        """Remove the trailing slash from the url"""
        if url[-1] == "/": # remove trailing slash
            url = url[:-1]
        return url

    @abstractmethod
    def check_health(self, **kwargs):
        """Check the health of the protein folding model.
        return True if the health check passed, False otherwise
        """
        assert self.health_check_url is not None, "Health check URL is not set"
        response = requests.get(self.health_check_url)
        if response.text == "true":
            print("Health check passed")
            return True
        else:
            print("Health check failed")
            return False

    @abstractmethod
    def predict(self, sequence: str, **kwargs) -> str:
        """Predict the structure of a given protein sequence. Extends functionality of submit_job."""
        pass




class ESMFoldNIM(NIM):
    def __init__(self, base_url: str, **kwargs):
        super().__init__(base_url, **kwargs)

        # intiate query and healthcheck url
        self.base_url = self.clean_url(self.base_url)
        self.query_url = self.base_url + "/protein-structure/esmfold/predict"
        self.health_check_url = self.base_url + "/health/ready"

    def predict(self, sequence: str, **kwargs):
        """
        Main function to run the molecular docking
        sequence: str, single aa sequence
        return JSON response
        """

        data = {
            "sequence": sequence,
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(self.query_url, headers=headers, json=data)

        if response.status_code == 200:
            print("Request successful")
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response:", response.text)

        return response.json()


class DiffDockNIM(NIM):

    def __init__(self, base_url: str, **kwargs):
        super().__init__(base_url, **kwargs)
        self.base_url = self.clean_url(self.base_url)
        self.query_url = self.base_url + "/molecular-docking/diffdock/generate"
        self.health_check_url = self.base_url + "/v1/health/ready"

    def predict(self, protein_file_path: str, ligand_file_path: str, **kwargs):
        """Predict the structure of a given protein sequence. Extends functionality of submit_job."""
        pass


    # def run_diffdock(query_url, protein_file_path, ligand_file_path):
    #     """
    #     Main function to run the molecular docking
    #     :param query_url: str, the url to send the request to
    #     :param protein_file_path: str, path to the protein file
    #     :param ligand_file_path: str, path to the ligand file
    #     return JSON response
    #     """

    #     protein_bytes = file_to_json_compatible_string(protein_file_path)
    #     ligand_bytes = file_to_json_compatible_string(ligand_file_path)

    #     data = {
    #         "ligand": ligand_bytes,
    #         "ligand_file_type": "sdf",
    #         "protein": protein_bytes,
    #         "num_poses": 20,
    #         "time_divisions": 20,
    #         "steps": 18,
    #         "save_trajectory": False,  # diffusion trajectory
    #         "is_staged": False
    #     }

    #     headers = {"Content-Type": "application/json"}

    #     response = requests.post(query_url, headers=headers, json=data)

    #     if response.status_code == 200:
    #         print("Request successful, output saved to output.json")
    #     else:
    #         print(f"Request failed with status code {response.status_code}")
    #         print("Response:", response.text)

    #     return response.json()


class AlphaFoldNIM(NIM):
    def __init__(self, base_url: str, healthcheck_url: str, submit_job_url: str, **kwargs):
        super().__init__(base_url, healthcheck_url, submit_job_url, **kwargs)
        raise NotImplementedError("AlphaFold is not implemented yet.")  



