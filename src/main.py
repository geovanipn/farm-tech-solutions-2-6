import sys

from src.db.connection import get_connection
from src.models.harvest_record import HarvestRecord, VALID_VARIETIES
from src.services.field_service import create_field, list_fields
from src.services.harvester_service import create_harvester, list_harvesters
from src.services.harvest_service import create_record, list_records
from src.reports.report import (
    report_by_harvester,
    report_by_field,
    report_by_operator,
    summary_report,
)
from src.utils.validation import read_non_empty, read_float, read_int, read_date
from src.utils.display import print_success, print_error, print_alert
from src.utils.file_io import save_records_json

RECORDS_JSON_PATH = "data/records.json"


def _read_optional_date(prompt: str):
    """Lê uma data opcional; retorna None se o usuário pressionar Enter sem digitar nada."""
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            return None
        import datetime
        try:
            return datetime.datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("Erro: data inválida. Use o formato DD/MM/AAAA ou pressione Enter para pular.")


def _print_menu() -> None:
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   SISTEMA DE CONTROLE DE PERDAS NA COLHEITA DE CANA  ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("  1. Cadastrar talhão")
    print("  2. Cadastrar colhedora")
    print("  3. Registrar colheita")
    print("  ──────────────────────────────────────────────────────")
    print("  4. Relatório por colhedora")
    print("  5. Relatório por talhão")
    print("  6. Relatório por operador")
    print("  7. Resumo geral")
    print("  ──────────────────────────────────────────────────────")
    print("  8. Exportar todos os registros (JSON)")
    print("  0. Sair")
    print()


def _opcao_cadastrar_talhao(conn) -> None:
    nome = read_non_empty("Nome do talhão: ")
    area = read_float("Área (ha): ", min_val=0.01)

    print("\nVariedades de cana-de-açúcar disponíveis:")
    for i, v in enumerate(VALID_VARIETIES, start=1):
        print(f"  {i}. {v}")
    escolha = read_int("Escolha o número da variedade: ", min_val=1, max_val=len(VALID_VARIETIES))
    variedade = VALID_VARIETIES[escolha - 1]

    data_plantio = _read_optional_date("Data de plantio (DD/MM/AAAA) [Enter para pular]: ")

    field = create_field(conn, name=nome, area_ha=area, variety=variedade, plant_date=data_plantio)
    print_success(f"Talhão '{field.name}' cadastrado com sucesso! (ID: {field.id})")


def _opcao_cadastrar_colhedora(conn) -> None:
    codigo = read_non_empty("Código da colhedora (ex.: COL-01): ")
    modelo = read_non_empty("Modelo: ")
    harvester = create_harvester(conn, code=codigo, model=modelo)
    print_success(f"Colhedora '{harvester.code}' cadastrada com sucesso! (ID: {harvester.id})")


def _opcao_registrar_colheita(conn) -> None:
    talhoes = list_fields(conn)
    if not talhoes:
        print_error("Nenhum talhão cadastrado. Cadastre um talhão primeiro.")
        return

    print("\nTalhões disponíveis:")
    for i, t in enumerate(talhoes, start=1):
        print(f"  {i}. {t.name} ({t.area_ha:.2f} ha)")
    idx_talhao = read_int("Escolha o número do talhão: ", min_val=1, max_val=len(talhoes))
    talhao = talhoes[idx_talhao - 1]

    colhedoras = list_harvesters(conn)
    if not colhedoras:
        print_error("Nenhuma colhedora cadastrada. Cadastre uma colhedora primeiro.")
        return

    print("\nColhedoras disponíveis:")
    for i, c in enumerate(colhedoras, start=1):
        print(f"  {i}. {c.code} — {c.model}")
    idx_colhedora = read_int("Escolha o número da colhedora: ", min_val=1, max_val=len(colhedoras))
    colhedora = colhedoras[idx_colhedora - 1]

    operador = read_non_empty("Nome do operador: ")
    data_colheita = read_date("Data da colheita (DD/MM/AAAA): ")
    producao = read_float("Produção estimada (toneladas): ", min_val=0.1)
    perda = read_float("Perda medida (%): ", min_val=0.0, max_val=100.0)
    preco = read_float("Preço da tonelada (R$): ", min_val=0.01)

    record = HarvestRecord(
        field_id=talhao.id,
        harvester_id=colhedora.id,
        field_name=talhao.name,
        harvester_code=colhedora.code,
        operator_name=operador,
        harvest_date=data_colheita,
        estimated_yield_ton=producao,
        loss_pct=perda,
        ton_price_brl=preco,
    )

    record = create_record(conn, record)
    print_success(f"Colheita registrada com sucesso! (ID: {record.id})")

    if record.is_high_loss():
        print_alert("Perda acima de 10%! Verifique a regulagem da colhedora.")

    records = list_records(conn)
    save_records_json([r.to_dict() for r in records], RECORDS_JSON_PATH)


def _opcao_relatorio_colhedora(conn) -> None:
    records = list_records(conn)
    if not records:
        print_error("Nenhum registro encontrado.")
        return
    report_by_harvester(records)


def _opcao_relatorio_talhao(conn) -> None:
    records = list_records(conn)
    if not records:
        print_error("Nenhum registro encontrado.")
        return
    report_by_field(records)


def _opcao_relatorio_operador(conn) -> None:
    records = list_records(conn)
    if not records:
        print_error("Nenhum registro encontrado.")
        return
    report_by_operator(records)


def _opcao_resumo_geral(conn) -> None:
    records = list_records(conn)
    if not records:
        print_error("Nenhum registro encontrado.")
        return
    summary_report(records)


def _opcao_exportar_json(conn) -> None:
    records = list_records(conn)
    save_records_json([r.to_dict() for r in records], RECORDS_JSON_PATH)
    print_success(f"Arquivo exportado: {RECORDS_JSON_PATH}")


def main() -> None:
    try:
        conn = get_connection()
    except Exception as e:
        print_error(f"Não foi possível conectar ao banco de dados: {e}")
        sys.exit(1)

    opcoes = {
        1: _opcao_cadastrar_talhao,
        2: _opcao_cadastrar_colhedora,
        3: _opcao_registrar_colheita,
        4: _opcao_relatorio_colhedora,
        5: _opcao_relatorio_talhao,
        6: _opcao_relatorio_operador,
        7: _opcao_resumo_geral,
        8: _opcao_exportar_json,
    }

    while True:
        _print_menu()
        try:
            opcao = read_int("  Opção: ", min_val=0, max_val=8)
        except (KeyboardInterrupt, EOFError):
            print()
            print_success("Encerrando o sistema. Até logo!")
            break

        if opcao == 0:
            print_success("Encerrando o sistema. Até logo!")
            break

        try:
            opcoes[opcao](conn)
        except Exception as e:
            print_error(str(e))


if __name__ == "__main__":
    main()
