# Vyhodnocení vysledků experimentů

Porovnání výstupu rozpoznávače a referenčního přepisu.

## Jupyter notebooky

K získání přehledových výsledků se slouží jupyter notebooky `postprocssing.ipnb` a `postprocssing_summary.ipnb`.

### postprocssing.ipnb

Kódy v tomto notebooku vytvoří souhrný výsledek pro jeden dílčí experiment v rámci testu. Pro získání
výsledků je potřeba nastavit cestu k výsledkům z rozpoznávače vyhodnocené nástrojem `pyeval`. Výstupem
je průběh přesnosti rozpoznávání v závislosti na *penalty insertion*. Dalším výsledkem je konfúzní tabulka.

### postprocssing_summary.ipnb

Kódy v tomto notebooku vytváří souhrný výsledek pro všechny dílčí experimenty v rámci testu. Pro získání
výsledků je potřeba nastavit adresář testu. V tomto adresáři se vyhledájí všechny dílčí experimenty a
vygeneruje se graf průběhů přesnosti pro všechny dílčí experimenty. Graf je uložen do složky testu.
