"""Проверяет, что openapi.yaml — валидная спецификация OpenAPI 3.x, и печатает список операций."""

import sys
from pathlib import Path

import yaml
from openapi_spec_validator import validate

SPEC = Path(__file__).resolve().parent.parent / "openapi.yaml"


def main() -> int:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    validate(spec)
    operations = [
        (method.upper(), path)
        for path, item in spec["paths"].items()
        for method in item
        if method in {"get", "post", "put", "patch", "delete"}
    ]
    print(f"OpenAPI {spec['openapi']} валидна, операций: {len(operations)}")
    for method, path in operations:
        print(f"  {method:5} {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
