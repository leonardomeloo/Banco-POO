from banco_classes import  PessoaFisica, ContaCorrente, Saque, Deposito


cliente = PessoaFisica(nome="João Silva", cpf="123.456.789-00", data_nascimento="01/01/1980", endereco="Rua A, 123")

conta_corrente = ContaCorrente(cliente=cliente, numero_conta="12345-6")

cliente.adicionar_conta(conta_corrente)

deposito1 = Deposito(valor=1000.0)
cliente.realizar_transacao(conta_corrente, deposito1)
print(f"Saldo após depósito: {conta_corrente.saldo}")


saque1 = Saque(valor=200.0)
cliente.realizar_transacao(conta_corrente, saque1)
print(f"Saldo após saque: {conta_corrente.saldo}")

saque2 = Saque(valor=1000.0)
cliente.realizar_transacao(conta_corrente, saque2)
print(f"Saldo após tentativa de saque excedendo saldo: {conta_corrente.saldo}")


saque3 = Saque(valor=100.0)
cliente.realizar_transacao(conta_corrente, saque3)

saque4 = Saque(valor=100.0)
cliente.realizar_transacao(conta_corrente, saque4)

saque5 = Saque(valor=100.0)
cliente.realizar_transacao(conta_corrente, saque5)
print(f"Saldo varios saques: {conta_corrente.saldo}")

saque6 = Saque(valor=100.0)
cliente.realizar_transacao(conta_corrente, saque6)
print(f"Saldo após tentativa de saque excedendo quantidade de saques: {conta_corrente.saldo}")

for transacao in conta_corrente._historico._transacoes:
    print(transacao)
