from enum import Enum, auto

class EnvironmentType(Enum):
    """
    Enum para classificação de ambientes.
    """
    PRODUCTION = auto()  # PRD
    HOMOLOGATION = auto()  # HML

    @classmethod
    def from_branch(cls, branch_name: str) -> 'EnvironmentType':
        """
        Classifica o ambiente com base no nome da branch.
        
        Args:
            branch_name (str): Nome da branch
            
        Returns:
            EnvironmentType: Tipo do ambiente
        """
        if branch_name.lower() in ['main', 'master']:
            return cls.PRODUCTION
        return cls.HOMOLOGATION

    def __str__(self) -> str:
        return 'PRD' if self == self.PRODUCTION else 'HML' 