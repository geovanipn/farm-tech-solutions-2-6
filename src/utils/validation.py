import datetime


def read_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        entrada = input(prompt)
        try:
            valor = float(entrada)
        except ValueError:
            print("Erro: entrada inválida. Digite um número.")
            continue
        if min_val is not None and max_val is not None and (valor < min_val or valor > max_val):
            print(f"Erro: o valor deve estar entre {min_val} e {max_val}.")
            continue
        if min_val is not None and valor < min_val:
            print(f"Erro: o valor deve ser maior ou igual a {min_val}.")
            continue
        if max_val is not None and valor > max_val:
            print(f"Erro: o valor deve ser menor ou igual a {max_val}.")
            continue
        return valor


def read_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        entrada = input(prompt)
        try:
            valor = int(entrada)
        except ValueError:
            print("Erro: entrada inválida. Digite um número inteiro.")
            continue
        if min_val is not None and max_val is not None and (valor < min_val or valor > max_val):
            print(f"Erro: o valor deve estar entre {min_val} e {max_val}.")
            continue
        if min_val is not None and valor < min_val:
            print(f"Erro: o valor deve ser maior ou igual a {min_val}.")
            continue
        if max_val is not None and valor > max_val:
            print(f"Erro: o valor deve ser menor ou igual a {max_val}.")
            continue
        return valor


def read_date(prompt: str) -> datetime.date:
    while True:
        entrada = input(prompt)
        try:
            return datetime.datetime.strptime(entrada.strip(), "%d/%m/%Y").date()
        except ValueError:
            print("Erro: data inválida. Use o formato DD/MM/AAAA.")


def read_non_empty(prompt: str) -> str:
    while True:
        entrada = input(prompt)
        if entrada.strip():
            return entrada.strip()
        print("Erro: o campo não pode estar vazio.")
