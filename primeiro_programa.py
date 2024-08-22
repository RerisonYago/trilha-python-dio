def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    valor = float(input("Informe o valor do saque: "))

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    while True:
        opcao = input(menu)

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
