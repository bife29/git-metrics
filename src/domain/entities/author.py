from typing import Optional

class Author:
    """
    Representa um autor de commits no repositório.
    
    Attributes:
        name (str): Nome do autor
        email (str): Email do autor
    """
    def __init__(self, name: str, email: Optional[str] = None):
        """
        Inicializa um autor.
        
        Args:
            name: Nome ou email do autor
            email: Email do autor (opcional)
        """
        # Se apenas o email for fornecido no name, usa ele como identificador
        if '@' in name and not email:
            self.email = name
            self.name = name.split('@')[0]  # Usa parte antes do @ como nome
        else:
            self.name = name
            self.email = email or name  # Se não tiver email, usa o nome como identificador
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return NotImplemented
        # Considera igual se o email for o mesmo ou se o nome for o mesmo e não houver email
        return (self.email == other.email) or (self.name == other.name and not self.email and not other.email)

    def __hash__(self) -> int:
        # Usa o email para hash se disponível, senão usa o nome
        return hash(self.email if self.email else self.name)
    
    def __str__(self) -> str:
        if self.email and self.email != self.name:
            return f"{self.name} <{self.email}>"
        return self.name
    
    def __repr__(self) -> str:
        if self.email and self.email != self.name:
            return f"Author(name='{self.name}', email='{self.email}')"
        return f"Author(name='{self.name}')" 