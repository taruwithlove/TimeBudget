"""Конвертер JSON -> CSV. Запуск: python scripts/csv_converter.py input.json output.csv"""
import csv, json, sys
from pathlib import Path

def json_to_csv(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list) or not rows:
        raise ValueError("Ожидается непустой список объектов JSON.")
    fields = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Готово: {output_path}; строк: {len(rows)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Использование: python scripts/csv_converter.py input.json output.csv")
    json_to_csv(Path(sys.argv[1]), Path(sys.argv[2]))
