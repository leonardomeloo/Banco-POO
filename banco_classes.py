from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Cliente:
    def __init__(self, endereco: str) -> None:
        self._endereco = endereco
        self._contas: List['Conta'] = []
    
    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao') -> None:
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: 'Conta') -> None:
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, endereco: str) -> None:
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self.data_nascimento = data_nascimento
    
    @property
    def nome(self) -> str:
        return self._nome


class Conta:
    def __init__(self, numero_conta: str, cliente: Cliente) -> None:
        self._saldo = 0
        self._numero = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: str) -> 'Conta':
        return cls(numero, cliente)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> str:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def historico(self) -> 'Historico':
        return self._historico
    
    def sacar(self, valor: float) -> bool:
        excedeu_valor_saldo = valor > self._saldo
        if excedeu_valor_saldo:
            print("Falha na operação. Saldo insuficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque feito com sucesso.")
            return True
        
        else:
            print("Falha na operação. Verificar valor digitado.")
        return False
    
    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("Deposito feito com sucesso.")
            return True
        else:
            print("Falha na operação. Verificar valor informado")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero_conta: str, cliente: Cliente, limite_valor_saque: float = 500, limite_qta_saque: int = 3) -> None:
        super().__init__(numero_conta, cliente)
        self._limite_valor_saque = limite_valor_saque
        self._limite_qta_saque = limite_qta_saque

    def sacar(self, valor: float) -> bool:
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_valor_limite = valor > self._limite_valor_saque
        excedeu_qta_limite = numero_saque >= self._limite_qta_saque

        if excedeu_valor_limite:
            print("Operação falhou. Valor do saque excede o limite")
        
        elif excedeu_qta_limite:
            print("Operação falhou. Quantidade de saque(s), chegou ao máximo.")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""
            Agência:\t {self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
            """


class Historico:
    def __init__(self) -> None:
        self._transacoes: List[dict] = []
    
    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes
    
    def adicionar_transacao(self, transacao: 'Transacao') -> None:
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass
    
    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        pass


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> None:
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> None:
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


