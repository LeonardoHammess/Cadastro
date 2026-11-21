"""Implementação do repositório de pessoas utilizando MySQL."""

import os

from typing import List, Optional

import mysql.connector
from mysql.connector.constants import ClientFlag

from pessoa import Pessoa
from repositorio_pessoas import RepositorioPessoas


class RepositorioPessoasMySQL(RepositorioPessoas):
    """Persiste pessoas na tabela pessoa do MySQL principal."""

    def __init__(self, host, port, usuario, senha, banco):
        self._config = {
            "host": host,
            "port": port,
            "user": usuario,
            "password": senha,
            "database": banco,
            "client_flags": [ClientFlag.FOUND_ROWS],
        }

    @classmethod
    def a_partir_do_ambiente(cls):
        """Lê a configuração das variáveis de ambiente."""
        return cls(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ["DB_PORT"]),
            usuario=os.environ["DB_USER"],
            senha=os.environ["DB_PASSWORD"],
            banco=os.environ.get("DB_NAME", "cadastro"),
        )

    def _conectar(self):
        """Abre uma nova conexão com o MySQL principal."""
        return mysql.connector.connect(**self._config)

    def _executar(self, sql, valores):
        """Executa INSERT/UPDATE em transação; devolve linhas afetadas."""
        conexao = self._conectar()
        try:
            cursor = conexao.cursor()
            try:
                cursor.execute(sql, valores)
                conexao.commit()
                return cursor.rowcount
            finally:
                cursor.close()
        except mysql.connector.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def _consultar(self, sql, valores=()):
        """Executa um SELECT e devolve todas as linhas."""
        conexao = self._conectar()
        try:
            cursor = conexao.cursor()
            try:
                cursor.execute(sql, valores)
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            conexao.close()

    def cadastrar(self, pessoa: Pessoa) -> None:
        sql = (
            "INSERT INTO pessoa (nome, idade, email) "
            "VALUES (%s, %s, %s)"
        )
        valores = (
            pessoa.getNome(),
            pessoa.getIdade(),
            pessoa.getEmail(),
        )
        self._executar(sql, valores)

    def buscar(self, nome: str) -> Optional[Pessoa]:
        sql = (
            "SELECT nome, idade, email FROM pessoa "
            "WHERE nome = %s ORDER BY id LIMIT 1"
        )
        linhas = self._consultar(sql, (nome,))
        return self._para_pessoa(linhas[0]) if linhas else None

    def listar(self) -> List[Pessoa]:
        sql = "SELECT nome, idade, email FROM pessoa ORDER BY id"
        linhas = self._consultar(sql)
        return [self._para_pessoa(linha) for linha in linhas]

    @staticmethod
    def _para_pessoa(linha) -> Pessoa:
        nome, idade, email = linha
        return Pessoa(nome, idade, email)

    def alterar(self, nome: str, nova_pessoa: Pessoa) -> bool:
        sql = (
            "UPDATE pessoa SET nome = %s, idade = %s, email = %s "
            "WHERE nome = %s"
        )
        valores = (
            nova_pessoa.getNome(),
            nova_pessoa.getIdade(),
            nova_pessoa.getEmail(),
            nome,
        )
        return self._executar(sql, valores) > 0
    
