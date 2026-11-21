
"""Teste das operações de cadastro."""

import copy

import pytest

from cadastro import CadastroPessoas
from pessoa import Pessoa
from repositorios.repositorios_pessoas_memoria import (
    RepositorioPessoasMemoria,
)


class RepositorioDeCopias(RepositorioPessoasMemoria):
    """Devolve cópias, simulando objetos reconstruídos."""

    def buscar(self, nome):
        pessoa = super().buscar(nome)

        if pessoa is None:
            return None

        return copy.copy(pessoa)


def test_cadastrar_pessoa():
    """Confere armazenamento e quantidade."""
    cadastro = CadastroPessoas()
    cadastro.cadastrar("Ana", 20, "ana@example.com")
    pessoas = cadastro.listar()

    assert len(pessoas) == 1
    assert pessoas[0].getNome() == "Ana"
    assert pessoas[0].getIdade() == 20
    assert pessoas[0].getEmail() == "ana@example.com"


def test_buscar_por_nome():
    """Encontra uma pessoa já cadastrada."""
    cadastro = CadastroPessoas()
    cadastro.cadastrar("Ana", 20, "ana@example.com")
    encontrada = cadastro.buscarPorNome("Ana")

    assert encontrada is not None
    assert encontrada.getNome() == "Ana"
    assert encontrada.getIdade() == 20
    assert encontrada.getEmail() == "ana@example.com"


def test_alterar_pessoa():
    """Altera os dados e persiste no repositório."""
    cadastro = CadastroPessoas()
    cadastro.cadastrar("Ana", 20, "ana@example.com")

    alterada = cadastro.alterar(
        "Ana",
        "Ana Maria",
        21,
        "anamaria@example.com"
    )

    assert alterada is not None
    assert cadastro.buscarPorNome("Ana") is None

    encontrada = cadastro.buscarPorNome("Ana Maria")

    assert encontrada is not None
    assert encontrada.getIdade() == 21
    assert encontrada.getEmail() == "anamaria@example.com"


def test_alterar_pessoa_inexistente():
    """Retorna None ao alterar quem não está cadastrado."""
    cadastro = CadastroPessoas()

    assert cadastro.alterar(
        "Bia",
        "Bia",
        30,
        "bia@example.com"
    ) is None


@pytest.mark.parametrize(
    "fabrica",
    [RepositorioPessoasMemoria, RepositorioDeCopias]
)
def test_alterar_persiste(fabrica):
    """Confere a persistência da alteração nos dois repositórios."""
    repositorio = fabrica()

    repositorio.cadastrar(
        Pessoa("Ana Souza", 30, "ana@example.com")
    )

    cadastro = CadastroPessoas(repositorio)

    cadastro.alterar(
        "Ana Souza",
        "Ana Souza",
        31,
        "ana.s@example.com"
    )

    pessoa = repositorio.buscar("Ana Souza")

    assert pessoa is not None
    assert pessoa.getIdade() == 31
    assert pessoa.getEmail() == "ana.s@example.com"
