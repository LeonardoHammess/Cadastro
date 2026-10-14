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
