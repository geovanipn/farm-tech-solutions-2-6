from src.utils.file_io import save_records_json, load_records_json, export_report_txt


def test_save_and_load_json(tmp_json):
    data = [{"id": 1, "name": "Talhão A"}, {"id": 2, "name": "Talhão B"}]
    save_records_json(data, tmp_json)
    loaded = load_records_json(tmp_json)
    assert loaded == data


def test_load_json_missing_file(tmp_path):
    path = str(tmp_path / "nao_existe.json")
    result = load_records_json(path)
    assert result == []


def test_export_report_txt(tmp_path):
    path = str(tmp_path / "report.txt")
    content = "Linha 1\nLinha 2\n"
    export_report_txt(content, path)
    with open(path, encoding="utf-8") as f:
        assert f.read() == content


def test_json_preserves_types(tmp_json):
    data = [{"int_val": 42, "float_val": 3.14}]
    save_records_json(data, tmp_json)
    loaded = load_records_json(tmp_json)
    assert loaded[0]["int_val"] == 42
    assert isinstance(loaded[0]["int_val"], int)
    assert loaded[0]["float_val"] == 3.14
    assert isinstance(loaded[0]["float_val"], float)
