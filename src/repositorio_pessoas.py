"""Contrato para repositórios de armazenamento de pessoas."""

from abc import ABC, abstractmethod
from typing import List, Optional

from pessoa import Pessoa

class RepositorioPessoas(ABC):
    """Define as operações de armazenamento de pessoas."""

    @abstractmethod
    def cadastrar(self, pessoa: Pessoa) -> None:
        pass

    @abstractmethod
    def buscar(self, nome: str) -> Optional[Pessoa]:
        pass

    @abstractmethod
    def listar(self) -> List[Pessoa]:
        pass

    @abstractmethod
    def alterar(self, nome: str, nova_pessoa: Pessoa) -> bool:
        pass
