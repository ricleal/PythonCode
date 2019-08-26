import toml
from pprint import pprint

parsed_toml = toml.load("example.toml")

pprint(parsed_toml, width=1)

