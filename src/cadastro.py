"""Gerenciamento do cadastro de pessoas."""

from typing import List, Optional

from pessoa import Pessoa
from repositorio_pessoas import RepositorioPessoas
from repositorios.repositorios_pessoas_memoria import RepositorioPessoasMemoria


class CadastroPessoas:
    """Gerencia as operações de cadastro de pessoas."""

    def __init__(
        self, repositorio: Optional[RepositorioPessoas] = None
    ) -> None:
        if repositorio is None:
            repositorio = RepositorioPessoasMemoria()

        self.__repositorio = repositorio

    def cadastrar(self, nome, idade, email):
        pessoa = Pessoa(nome, idade, email)
        self.__repositorio.cadastrar(pessoa)
        return pessoa

    def buscarPorNome(self, nome):
        return self.__repositorio.buscar(nome)

    def listar(self) -> List[Pessoa]:
        return self.__repositorio.listar()

    def alterar(self, nome, novo_nome, nova_idade, novo_email):
        nova_pessoa = Pessoa(novo_nome, nova_idade, novo_email)

        if not self.__repositorio.alterar(nome, nova_pessoa):
            return None

        return nova_pessoa
