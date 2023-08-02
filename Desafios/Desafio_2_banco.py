import textwrap
import datetime
import re
 
# Constantes

NAME = "WORLD BANK"
WITHDRAW_COUNTER_MAX_LIMIT = 3
AGENCY = "0001"
WITHDRAW_VALUE_LIMIT = 500


def menu(NAME):
    menu = f"""

    ><$$$$$$$$$$$$$>>>> WORLD BANK <<<<$$$$$$$$$$$$$><
    $$                                              $$
    $$                    WELCOME                   $$
    $$                      TO                      $$
    $$              {NAME.center(17)}               $$
    $$                                              $$
    $$                                              $$
    $$           [ U ] - Cadastrar Usuario          $$
    $$           [ C ] - Cadastrar Conta            $$
    $$           [ M ] - Mostrar Contas             $$         
    $$           [ D ] - Depositar                  $$
    $$           [ S ] - Sacar                      $$
    $$           [ E ] - Extrato                    $$
    $$           [ Q ] - Sair                       $$
    $$                                              $$
    ><$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$><

    ---------<[ Selecione a opcao desejada ]>---------        
    
    => """
    return input(textwrap.dedent(menu)).upper()

def float_integer_validation(answer):
    
    while True:
        value = input(f"\n[ 0 ] - Sair\n{answer}\n=> ")
        
        if value == "0":
            return 0

        if not value.replace('.', '', 1).isdigit():
            print("\n      >>> Entrada inválida <<<\n\nDigite apenas valores numéricos.\n")
            continue

        partes = value.split('.')
        if len(partes) == 1:
            number = int(value)
        elif len(partes) == 2:
            if len(partes[1]) <= 2:
                number = float(value)
            else:
                print("\n      >>> Entrada inválida <<<\n\nDigite apenas valores numéricos.\n")
                continue
        else:
            print("\n      >>> Entrada inválida <<<\n\nDigite apenas valores numéricos.\n")
            continue

        if number >= 0:
            return number
        else:
            print("\n      >>> Entrada inválida <<<\n\nDigite apenas valores numéricos.\n")
          
def validate_cpf(cpf):
    # Remover caracteres não numéricos do CPF
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Verificar se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Verificar se todos os dígitos do CPF são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcular os dígitos verificadores
    cpf_digits = cpf[:-2]
    sum_1 = sum(int(digit) * (10 - index) for index, digit in enumerate(cpf_digits))
    remainder_1 = sum_1 % 11
    if remainder_1 < 2:
        digit_1 = 0
    else:
        digit_1 = 11 - remainder_1

    cpf_digits += str(digit_1)

    sum_2 = sum(int(digit) * (11 - index) for index, digit in enumerate(cpf_digits))
    remainder_2 = sum_2 % 11
    if remainder_2 < 2:
        digit_2 = 0
    else:
        digit_2 = 11 - remainder_2

    # Verificar se os dígitos verificadores são válidos
    if cpf[-2:] != str(digit_1) + str(digit_2):
        return False

    return True

def create_user(users):
    while True:
        cpf = input("\n[ Informe os numeros do CPF ]\n\n[ 0 ] - Sair\n\n=> ")

        if cpf == '0':
            print("\n      $$$ Voltando ao menu principal $$$\n")
            return

        if not cpf.isdigit():
            print("\n       >>> CPF inválido! <<<\n\nCPF deve conter apenas números!\n")
            continue

        if not validate_cpf(cpf):
            print("\n       >>> CPF inválido! <<<\n\nCPF deve conter apenas números!\n")
            continue

        user = find_user_by_cpf(cpf, users)

        if user:
            print("\n       >>> CPF inválido! <<<\n\nJá existe usuário com esse CPF!\n")
            return

        break

    full_name = input("\n[ Informe o nome completo ]\n\n=> ")
    birth_date = input("\n[ Informe a data de nascimento (dd-mm-aaaa) ]\n\n=> ")
    address = input("\n[ Informe o endereço (logradouro, nº - bairro - cidade/estado) ]\n\n=> ")

    users.append({"nome": full_name, "data_nascimento": birth_date, "cpf": cpf, "endereco": address})

    print("\n     $$$ Usuário criado com sucesso! $$$\n")

def find_user_by_cpf(cpf, users):
    filtreds_users = [user for user in users if user["cpf"] == cpf]
    return filtreds_users[0] if filtreds_users else None

def create_account(AGENCY, users, accounts):
    while True:
        cpf = input("\n[ Informe o CPF do usuário ]\n\n[ 0 ] - Sair\n\n=> ")

        if cpf == '0':
            print("\n       $$$ Voltando ao menu principal $$$\n")
            return

        # Validar o CPF digitado pelo usuário
        if not validate_cpf(cpf):
            print("\n       >>> CPF inválido! <<<\n\nCPF deve conter apenas números!\n")
            continue

        user = find_user_by_cpf(cpf, users)

        if user:
            num_account = len(accounts) + 1
            account = {
                "agencia": AGENCY,
                "numero_conta": num_account,
                "usuario": user,
                "saldo": 0,
                "extrato": "",
                "limite_saque": 0
            }
            accounts.append(account)
            print("\n      $$$ Conta criada com sucesso! $$$")
        else:
            print("\n       >>> Operação falhou! <<<<\n\nUsuário não encontrado.\n")

        break

def show_accounts(accounts):
    if accounts:
        print("\n=============== WORLD BANK ACCOUNTS ==============")
        for account in accounts:
            show_acc = f"""
                Agência:\t{account['agencia']}
                C/C:\t\t{account['numero_conta']}
                Titular:\t{account['usuario']['nome']}
                CPF:\t\t{account['usuario']['cpf']}
                Saldo:\t\tR$ {account['saldo']:.2f}
            """
            print(textwrap.dedent(show_acc))
        print("====================== END =======================")
    else:
        print(f"\n       >>> Operação falhou! <<<<\n\nNenhuma conta cadastrada.\n")
    
def deposit(accounts, /):
    
    num_account = float_integer_validation("\n[ Digite o nº da conta que deseja depositar ]\n")
    if num_account == 0:
        print("\n       $$$ Voltando ao menu principal $$$\n")
        return
    
    account = check_account_exists(accounts, num_account)

    if account:
        deposit_value = float_integer_validation("\n[ Digite o valor que deseja depositar ]\n")

        if deposit_value == 0:
            print("\n       $$$ Voltando ao menu principal $$$\n")
            return
        elif deposit_value > 0:
            account['saldo'] += deposit_value
            account['extrato'] += f"= Depósito {('R$ ' + f'{deposit_value:.2f}' + ' =').rjust(39)}\n"
            print(f"\n$$$ Depósito de R$ {deposit_value:.2f} realizado com sucesso. $$$\n")
        
    else:
        print(f"\n       >>> Operação falhou! <<<\n\nConta {num_account} não encontrada.\n")
    
def check_account_exists(accounts, num_account):
    return next((acc for acc in accounts if acc['numero_conta'] == num_account), None)

def is_balance_exceeded(account, withdraw_value):
    return withdraw_value > account['saldo']

def is_withdrawal_limit_exceeded(withdraw_value, withdraw_value_limit):
    return withdraw_value > withdraw_value_limit

def is_withdrawal_counter_limit_exceeded(account, WITHDRAW_COUNTER_MAX_LIMIT):
    return account['limite_saque'] >= WITHDRAW_COUNTER_MAX_LIMIT

def perform_withdraw(account, withdraw_value):
    account['saldo'] -= withdraw_value
    account['extrato'] += f"= Saque {('R$ ' + f'{withdraw_value:.2f}' + ' =').rjust(42)}\n"
    account['limite_saque'] += 1

def withdraw(*, accounts, withdraw_value_limit, WITHDRAW_COUNTER_MAX_LIMIT):
    num_account = float_integer_validation("\n[ Digite o nº da conta que deseja retirar ]\n")
    if num_account == 0:
        print("\n       $$$ Voltando ao menu principal $$$\n")
        return
    
    account = check_account_exists(accounts, num_account)

    if account is None:
        print(f"\n       >>> Operação falhou! <<<<\n\nConta {num_account} não encontrada.\n")
        return

    reset_limite_saque_daily(accounts)

    withdraw_value = float_integer_validation("\n[ Digite o valor que deseja retirar ]\n")

    if withdraw_value == 0:
        print("\n       $$$ Voltando ao menu principal $$$\n")
        return

    if is_balance_exceeded(account, withdraw_value):
        print(f"\n       >>> Operação falhou! <<<<\n\nSaldo insuficiente. Saldo atual: R$ {account['saldo']:.2f}\n")

    elif is_withdrawal_limit_exceeded(withdraw_value, withdraw_value_limit):
        print(f"\n       >>> Operação falhou! <<<<\n\nLimite de R$ {withdraw_value_limit:.2f} para cada saque.\n")

    elif is_withdrawal_counter_limit_exceeded(account, WITHDRAW_COUNTER_MAX_LIMIT):
        print(f"\n       >>> Operação falhou! <<<<\n\nLimite máximo de saques diários excedido.\n(Máx. {WITHDRAW_COUNTER_MAX_LIMIT})\n")

    elif withdraw_value > 0:
        perform_withdraw(account, withdraw_value)
        print(f"\n$$$ Saque de R$ {withdraw_value:.2f} realizado com sucesso.\n")

    else:
        print("\n      >>> Entrada inválida <<<\n\nDigite um número válido.\n")

def centered_print(text, width):
    print(text.center(width))

def show_extract(NAME, accounts, /):
    num_account = float_integer_validation("\n[ Digite o nº da conta para visualizar o extrato ]\n")
    if num_account == 0:
        print("\n       $$$ Voltando ao menu principal $$$\n")
        return

    account = check_account_exists(accounts, num_account)

    if account:
        saldo = account['saldo']
        extrato_temp = account['extrato'].rstrip('\n')

        print("=================== WORLD BANK ===================")
        print("=                                                =")
        print(f"=               {NAME.center(17)}                =")
        print("=                                                =")
        print("================== BANK ACCOUNT ==================")

        # Ajuste de alinhamento para a linha da Conta nº
        account_num_str = f"Conta nº: {account['numero_conta']}"
        print(f"= {account_num_str.ljust(47)}=")

        # Ajuste de alinhamento para a linha do Titular
        titular_str = f"Titular:  {account['usuario']['nome']}"
        print(f"= {titular_str.ljust(47)}=")

        print("===================== EXTRACT ====================")
        print("=                                                =")
        print("= Não foram realizadas movimentações             =" if not extrato_temp else extrato_temp)
        print("=                                                =")
        print(f"= Saldo {('R$ ' + f'{saldo:.2f}' + ' =').rjust(42)}")
        print("====================== END =======================")
    else:
        print(f"\nConta {num_account} não encontrada.")
        
def reset_limite_saque_daily(accounts):
    current_date = datetime.date.today()
    last_checked_date = getattr(reset_limite_saque_daily, '_last_checked_date', None)
    
    if last_checked_date is None or current_date != last_checked_date:
        for account in accounts:
            account['limite_saque'] = 0

        reset_limite_saque_daily._last_checked_date = current_date

def main():

    users = []
    accounts = []
      
    while True:
        op = menu(NAME)

        if op == "U":
            create_user(users)

        elif op == "C":
            create_account(AGENCY, users, accounts)

        elif op == "M":
            show_accounts(accounts)
        
        elif op == "D":
            deposit(accounts)

        elif op == "S":
            withdraw(accounts=accounts, withdraw_value_limit=WITHDRAW_VALUE_LIMIT, WITHDRAW_COUNTER_MAX_LIMIT=WITHDRAW_COUNTER_MAX_LIMIT)
                               
        elif op == "E":
            show_extract(NAME, accounts)

        elif op == "Q":
            print("\n\n        > Obrigado e volte sempre! < \n\n")
            break
            
        else:
            print("\n      >>> Operação inválida <<< \n\nSelecione novamente a operação desejada.\n")

main()