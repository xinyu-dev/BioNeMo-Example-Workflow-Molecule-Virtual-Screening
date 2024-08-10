from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ProteinFoldingNIM(ABC):
    """
    Abstract class for a protein folding model in NIM
    """
    @abstractmethod
    def healthcheck(self, **kwargs):
        """Check the health of the protein folding model."""
        pass

    @abstractmethod
    def submit_job(self, sequence: str, **kwargs) -> str:
        """Submit a job to the protein folding model."""
        pass

    @abstractmethod
    def predict(self, sequence: str, **kwargs) -> str:
        """Predict the structure of a given protein sequence. Extends functionality of submit_job."""
        pass

class ESMFoldNIM(ProteinFoldingNIM):
    def __init__(self, base_url: str, healthcheck_url: str, submit_job_url: str):
        super().__init__()
        self.base_url = base_url
        self.healthcheck_url = healthcheck_url
        self.submit_job_url = submit_job_url

    def healthcheck(self, **kwargs):
        """Check the health of the protein folding model."""
        pass

    def submit_job(self, sequence: str, **kwargs) -> str:
        """Submit a job to the protein folding model."""
        pass

    def predict(self, sequence: str, **kwargs) -> str:
        """Predict the structure of a given protein sequence. Extends functionality of submit_job."""
        pass


class AlphaFoldNIM(ProteinFoldingNIM):
    def __init__(self, base_url: str, healthcheck_url: str, submit_job_url: str):
        super().__init__()
        raise NotImplementedError("AlphaFold is not implemented yet.")