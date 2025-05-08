from dataclasses import dataclass

from model.country import Country


@dataclass
class Arco:
    country1:Country
    country2: Country
