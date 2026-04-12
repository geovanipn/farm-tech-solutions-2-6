import os

from tabulate import tabulate

from src.models.harvest_record import HarvestRecord
from src.services.harvest_service import group_by_harvester, group_by_field
from src.utils.display import print_alert
from src.utils.file_io import export_report_txt

LOSS_ALERT_THRESHOLD: float = 10.0  # % — acima disso dispara alerta


def report_by_harvester(records: list[HarvestRecord], export_dir: str = "data") -> str:
    groups = group_by_harvester(records)
    rows = []
    for code, recs in sorted(groups.items()):
        count = len(recs)
        avg_loss_pct = sum(r.loss_pct for r in recs) / count
        total_loss_ton = sum(r.loss_ton or 0.0 for r in recs)
        total_loss_brl = sum(r.loss_brl or 0.0 for r in recs)
        rows.append([
            code,
            count,
            f"{avg_loss_pct:.2f}",
            f"{total_loss_ton:.2f}",
            f"{total_loss_brl:.2f}",
        ])
        if avg_loss_pct > LOSS_ALERT_THRESHOLD:
            print_alert(f"Colhedora {code} com perda média de {avg_loss_pct:.2f}%")

    headers = ["Colhedora", "Qtd. Colheitas", "Perda Média (%)", "Perda Total (t)", "Perda Total (R$)"]
    table_str = tabulate(rows, headers=headers, tablefmt="grid")
    output = "=== Relatório por Colhedora ===\n" + table_str
    print(output)
    os.makedirs(export_dir, exist_ok=True)
    export_report_txt(output, os.path.join(export_dir, "relatorio_colhedora.txt"))
    return output


def report_by_field(records: list[HarvestRecord], export_dir: str = "data") -> str:
    groups = group_by_field(records)
    rows = []
    for field_name, recs in sorted(groups.items()):
        count = len(recs)
        avg_loss_pct = sum(r.loss_pct for r in recs) / count
        total_loss_brl = sum(r.loss_brl or 0.0 for r in recs)
        rows.append([
            field_name,
            "-",
            count,
            f"{avg_loss_pct:.2f}",
            f"{total_loss_brl:.2f}",
        ])
        if avg_loss_pct > LOSS_ALERT_THRESHOLD:
            print_alert(f"Talhão {field_name} com perda média de {avg_loss_pct:.2f}%")

    headers = ["Talhão", "Área (ha)", "Qtd. Colheitas", "Perda Média (%)", "Perda Total (R$)"]
    table_str = tabulate(rows, headers=headers, tablefmt="grid")
    output = "=== Relatório por Talhão ===\n" + table_str
    print(output)
    os.makedirs(export_dir, exist_ok=True)
    export_report_txt(output, os.path.join(export_dir, "relatorio_talhao.txt"))
    return output


def report_by_operator(records: list[HarvestRecord], export_dir: str = "data") -> str:
    groups: dict[str, list[HarvestRecord]] = {}
    for r in records:
        groups.setdefault(r.operator_name, []).append(r)

    rows = []
    for operator, recs in sorted(groups.items()):
        count = len(recs)
        avg_loss_pct = sum(r.loss_pct for r in recs) / count
        best = min(r.loss_pct for r in recs)
        worst = max(r.loss_pct for r in recs)
        rows.append([
            operator,
            count,
            f"{avg_loss_pct:.2f}",
            f"{best:.2f}",
            f"{worst:.2f}",
        ])

    headers = ["Operador", "Qtd. Colheitas", "Perda Média (%)", "Melhor Colheita (%)", "Pior Colheita (%)"]
    table_str = tabulate(rows, headers=headers, tablefmt="grid")
    output = "=== Relatório por Operador ===\n" + table_str
    print(output)
    os.makedirs(export_dir, exist_ok=True)
    export_report_txt(output, os.path.join(export_dir, "relatorio_operador.txt"))
    return output


def summary_report(records: list[HarvestRecord], export_dir: str = "data") -> str:
    total = len(records)
    total_yield_ton = sum(r.estimated_yield_ton for r in records)
    total_loss_ton = sum(r.loss_ton or 0.0 for r in records)
    avg_loss_pct = sum(r.loss_pct for r in records) / total if total else 0.0
    total_loss_brl = sum(r.loss_brl or 0.0 for r in records)
    alert_count = sum(1 for r in records if r.loss_pct > LOSS_ALERT_THRESHOLD)

    lines = [
        "=== Relatório Resumo ===",
        f"Total de registros        : {total}",
        f"Produção total estimada   : {total_yield_ton:.2f} t",
        f"Perda total               : {total_loss_ton:.2f} t  ({avg_loss_pct:.2f}% médio)",
        f"Perda total em R$         : R$ {total_loss_brl:,.2f}",
        f"Qtd. de alertas (>10%)    : {alert_count}",
    ]
    output = "\n".join(lines)
    print(output)
    os.makedirs(export_dir, exist_ok=True)
    export_report_txt(output, os.path.join(export_dir, "relatorio_resumo.txt"))
    return output
