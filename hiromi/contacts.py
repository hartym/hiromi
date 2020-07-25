from dataclasses import dataclass


@dataclass
class Contact:
    pass


@dataclass
class EmailContact(Contact):
    name: str
    email: str

    def __str__(self):
        return f"{self.name} <{self.email}>"
