"""Implementação em MySQL do repositório de pessoas."""

import os
from dataclasses import dataclass
from typing import List, Optional

import pymysql
from pymysql.constants import CLIENT

from pessoa import Pessoa
from repositorio_pessoas import RepositorioPessoas


@dataclass(frozen=True)
class ConfiguracaoMySQL:
    """Parâmetros de conexão com o servidor MySQL."""

    host: str = "127.0.0.1"
    porta: int = 3307
    usuario: str = "root"
    senha: str = ""
    banco: str = "cadastro"

    @classmethod
    def doAmbiente(cls) -> "ConfiguracaoMySQL":
        """Lê a configuração das variáveis de ambiente MYSQL_*."""
        padrao = cls()
        return cls(
            host=os.environ.get("MYSQL_HOST", padrao.host),
            porta=int(os.environ.get("MYSQL_PORT", str(padrao.porta))),
            usuario=os.environ.get("MYSQL_USER", padrao.usuario),
            senha=os.environ.get("MYSQL_PASSWORD", padrao.senha),
            banco=os.environ.get("MYSQL_DATABASE", padrao.banco),
        )


class RepositorioPessoasMySQL(RepositorioPessoas):
    """Armazena pessoas em uma tabela de um banco de dados MySQL."""

    _SQL_CRIAR_TABELA = (
        "CREATE TABLE IF NOT EXISTS pessoas ("
        " id INT AUTO_INCREMENT PRIMARY KEY,"
        " nome VARCHAR(100) NOT NULL,"
        " idade INT NOT NULL,"
        " email VARCHAR(255) NOT NULL,"
        " INDEX idx_pessoas_nome (nome)"
        ")"
    )

    def __init__(self, configuracao: Optional[ConfiguracaoMySQL] = None) -> None:
        if configuracao is None:
            configuracao = ConfiguracaoMySQL.doAmbiente()

        if not configuracao.banco.isidentifier():
            raise ValueError(f"Nome de banco inválido: {configuracao.banco!r}")

        self.__configuracao = configuracao
        self._criarEstrutura()

    def _conectar(self, usar_banco: bool = True) -> pymysql.connections.Connection:
        # FOUND_ROWS faz o UPDATE informar as linhas encontradas, e não apenas
        # as modificadas, para que alterar() retorne True mesmo sem mudanças.
        return pymysql.connect(
            host=self.__configuracao.host,
            port=self.__configuracao.porta,
            user=self.__configuracao.usuario,
            password=self.__configuracao.senha,
            database=self.__configuracao.banco if usar_banco else None,
            charset="utf8mb4",
            client_flag=CLIENT.FOUND_ROWS,
            autocommit=True,
        )

    def _criarEstrutura(self) -> None:
        with self._conectar(usar_banco=False) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{self.__configuracao.banco}`"
                )
                cursor.execute(f"USE `{self.__configuracao.banco}`")
                cursor.execute(self._SQL_CRIAR_TABELA)

    def cadastrar(self, pessoa: Pessoa) -> None:
        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pessoas (nome, idade, email) VALUES (%s, %s, %s)",
                    (pessoa.getNome(), pessoa.getIdade(), pessoa.getEmail()),
                )

    def buscar(self, nome: str) -> Optional[Pessoa]:
        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "SELECT nome, idade, email FROM pessoas"
                    " WHERE nome = %s ORDER BY id LIMIT 1",
                    (nome,),
                )
                linha = cursor.fetchone()

        if linha is None:
            return None

        return Pessoa(*linha)

    def listar(self) -> List[Pessoa]:
        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT nome, idade, email FROM pessoas ORDER BY id")
                linhas = cursor.fetchall()

        return [Pessoa(*linha) for linha in linhas]

    def alterar(self, nome: str, nova_pessoa: Pessoa) -> bool:
        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                linhas_afetadas = cursor.execute(
                    "UPDATE pessoas SET nome = %s, idade = %s, email = %s"
                    " WHERE id = (SELECT id FROM ("
                    "SELECT MIN(id) AS id FROM pessoas WHERE nome = %s) AS alvo)",
                    (
                        nova_pessoa.getNome(),
                        nova_pessoa.getIdade(),
                        nova_pessoa.getEmail(),
                        nome,
                    ),
                )

        return linhas_afetadas > 0
