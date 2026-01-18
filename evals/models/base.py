from typing import Protocol, Dict, Any


class ModelClient(Protocol):
    name: str

    def generate(self, case_input: Dict[str, Any]) -> str:
        ...
