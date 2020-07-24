from typing import Dict, Set


class Message:
    name: str = None
    media: Set[str] = None
    schema: Dict = None

    def validate(self, parameters):
        return parameters
