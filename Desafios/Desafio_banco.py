# float and integer input validation

def float_integer_validation():
    while True:
        value = input("\n[ 0 ] - Sair\n\nDigite o valor: R$ ")
        if 'E' not in value and value.replace('.', '', 1).isdigit():
            partes = value.split('.')
            if len(partes) == 1:
                number = int(value)
            elif len(partes) == 2:
                if len(partes[1]) <= 2:
                    number = float(value)
                else:
                    print("\nEntrada inválida. Digite apenas valores positivos com uma ou duas casas decimais.")
                    continue
            else:
                print("\nEntrada inválida. Digite apenas valores positivos com uma ou duas casas decimais.")
                continue

            if number >= 0:
                return number
            else:
                print("\nEntrada inválida. Digite apenas valores positivos com uma ou duas casas decimais.v")
        else:
                print("\nEntrada inválida. Digite apenas valores positivos com uma ou duas casas decimais.")
            

# variables and constants

name = "Felipe Manica"
balance = 0
limit = 500
extract = ""
withdrawal_counter_limit = 0
WITHDRAWAL_MAX_LIMIT = 3

# menu layout
 
menu = f"""

><$$$$$$$$$$$$$>>>> WORLD BANK <<<<$$$$$$$$$$$$$><
$$                                              $$
$$                   WELCOME                    $$
$$                                              $$
$$              {name.center(17)}               $$
$$                                              $$
$$               [ D ] - Depositar              $$
$$               [ S ] - Sacar                  $$
$$               [ E ] - Extrato                $$
$$               [ Q ] - Sair                   $$
$$                                              $$
$$                                              $$
><$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$><

Select: """

while True:

    op = input(menu).upper()
    
    if op == "D":

        deposit_value = float_integer_validation()
        if deposit_value > 0:
            balance += deposit_value
            extract += f" Depósito: R$ {deposit_value:>35.2f}\n"
            print(f"\nDepósito de R${deposit_value:.2f} realizado com sucesso.")
        
        elif deposit_value == 0:
            continue
        
        else:
            print("\nEntrada inválida. Digite um número válido.") 

    elif op == "S":
        
        withdraw_value = float_integer_validation()

        balance_exceeded = withdraw_value > balance

        withdrawal_limit_exceeded = withdraw_value > limit

        withdrawal_counter_limit_exceeded = withdrawal_counter_limit >= WITHDRAWAL_MAX_LIMIT

        if balance_exceeded:
            print(f"\nOperação falhou! Você não tem saldo suficiente. Saldo atual: R$ {balance:.2f}")

        elif withdrawal_limit_exceeded:
            print(f"\nOperação falhou! O valor excede o limite de R$ {limit:.2f} para cada saque.")

        elif withdrawal_counter_limit_exceeded:
            print(f"\nOperação falhou! Limite máximo de saques diários excedido. (Máx. {WITHDRAWAL_MAX_LIMIT})")

        elif withdraw_value > 0:
            balance -= withdraw_value
            extract += f" Saque: R$ {withdraw_value:>38.2f}\n"
            withdrawal_counter_limit += 1
            print(f"\nSaque no valor de R${withdraw_value:.2f} realizado com sucesso.\n\n>>>  Retire seu dinheiro!  <<< \n\n")
        
        elif withdraw_value == 0:
            continue 
        
        else:
            print("\nEntrada inválida. Digite um número válido.")
        
    elif op == "E":
        print("\n=================== WORLD BANK ===================")
        print(f"\n=               {name.center(17)}                =")
        print("\n===================== EXTRACT ====================\n")
        print("\n Não foram realizadas movimentações." if not extract else extract)
        print(f"\n Saldo: R$ {balance:>38.2f}")
        print("\n====================== END =======================")

    elif op == "Q":
        print("\n\n        > Obrigado por ser nosso cliente! < \n\n")
        break
        
    else:
        print("\nOperação inválida, por favor selecione novamente a operação desejada.")
