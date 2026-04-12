from tabulate import tabulate

_RESET  = "\033[0m"
_YELLOW = "\033[33m"
_GREEN  = "\033[32m"
_RED    = "\033[31m"


def print_table(headers: list, rows: list) -> None:
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_alert(message: str) -> None:
    print(f"{_YELLOW}⚠  ALERTA: {message}{_RESET}")


def print_success(message: str) -> None:
    print(f"{_GREEN}✔  {message}{_RESET}")


def print_error(message: str) -> None:
    print(f"{_RED}✘  Erro: {message}{_RESET}")


def print_separator() -> None:
    print("─" * 50)
