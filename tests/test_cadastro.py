"""Teste das operações de cadastro"""

from cadastro import CadastroPessoas

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
    alterada = cadastro.alterar("Ana", "Ana Maria", 21, "anamaria@example.com")
    assert alterada is not None
    assert cadastro.buscarPorNome("Ana") is None
    encontrada = cadastro.buscarPorNome("Ana Maria")
    assert encontrada is not None
    assert encontrada.getIdade() == 21
    assert encontrada.getEmail() == "anamaria@example.com"

def test_alterar_pessoa_inexistente():
    """Retorna None ao alterar quem não está cadastrado."""
    cadastro = CadastroPessoas()
    assert cadastro.alterar("Bia", "Bia", 30, "bia@example.com") is None
