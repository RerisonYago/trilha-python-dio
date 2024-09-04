from datetime import date

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, saldo, numero, agencia, cliente):
        self._saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        self._saldo -= valor
        self.historico.adicionar_transacao(Saque(valor))
        print(f"Saque de R$ {valor:.2f} realizado.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor de depósito inválido.")
            return False
        self._saldo += valor
        self.historico.adicionar_transacao(Deposito(valor))
        print(f"Depósito de R$ {valor:.2f} realizado.")
        return True

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        for transacao in self.historico.transacoes:
            print(f"{transacao}")
        print(f"\nSaldo:\t\tR$ {self._saldo:.2f}")
        print("==========================================")


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, limite, limite_saques):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao:
    def registrar(self, conta):
        raise NotImplementedError


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f}"


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Saque: R$ {self.valor:.2f}"


def menu():
    menu_text = """
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """
    return input(menu_text)


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if any(usuario.cpf == cpf for usuario in usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = PessoaFisica(nome, cpf, date.fromisoformat(data_nascimento), endereco)
    usuarios.append(usuario)
    print("=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)

    if usuario:
        conta = ContaCorrente(0, numero_conta, agencia, usuario, 500.0, 3)
        contas.append(conta)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta.agencia} | C/C: {conta.numero} | Titular: {conta.cliente.nome}")


def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular da conta: ")
            conta = next((conta for conta in contas if conta.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular da conta: ")
            conta = next((conta for conta in contas if conta.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular da conta: ")
            conta = next((conta for conta in contas if conta.cliente.cpf == cpf), None)
            if conta:
                conta.exibir_extrato()
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
