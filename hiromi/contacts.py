from dataclasses import dataclass


@dataclass
class Contact:
    pass


@dataclass
class EmailContact(Contact):
    name: str
    email: str
