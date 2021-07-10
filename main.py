import pprint
import requests
import json
import os
from urllib.parse import urljoin


class Jogador:
    def __init__(self, data):
        self.data = data

    @property
    def apelido(self):
        return self.data['apelido']

    @property
    def finalizacoes(self) -> int:
        return sum([self._scout(k) for k in ['FT', 'FD', 'FF']])

    def _scout(self, key) -> int:
        return self.data['scout'].get(key, 0)
        
    def __repr__(self):
        return f"Jogador['{self.apelido}',f={self.finalizacoes}]"

    def __str__(self):
        return self.__repr__()


class Jogadores:
    def __init__(self, jogadores):
        self.jogadores = jogadores

    def finalizadores(self, top=20):
        return self._top(20, 'finalizacoes')

    def _top(self, n, attr):
        return sorted(self.jogadores, key=lambda x: getattr(x, attr), reverse=True)[:n]


class CachedCartolaApi:
    def __init__(self):
        if not os.path.isdir("cache"):
            os.makedirs("cache")
            
    def mercado(self):
        return self._cached("/atletas/mercado", key="mercado")

    def _cached(self, path, key): 
        cache_path = f"cache/{key}.json"
        if not os.path.isfile(cache_path):
            response = requests.get(urljoin("https://api.cartolafc.globo.com", path))
            with open(cache_path, "w") as f:
                f.write(response.text)
        with open(cache_path, "r") as f:
            return json.load(f)


api = CachedCartolaApi()

jogadores = Jogadores([Jogador(p) for p in api.mercado()['atletas']])

top_twenty_finalizacoes = jogadores.finalizadores()

pprint.pprint(top_twenty_finalizacoes)

