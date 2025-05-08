from dataclasses import dataclass

@dataclass
class Country:
    StateAbb:str
    CCode:int #chiave primaria
    StateNme:str

    def __hash__(self):
        return self.CCode

    def __str__(self):
        return f"{self.StateNme}"

    def __eq__(self, other):
        return self.CCode == other.CCode