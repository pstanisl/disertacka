# Disertační práce

Repozitář obsahuje zdrojové kódy, které jsem použil při práci na mé disertaci.

## Instalace závislostí

Pro instalaci závislostí je doporučen balíčkovací systém [Miniconda](http://conda.pydata.org/miniconda.html).
V repozitáři je připraven soubor `environment.yml`, který obsahuje závislosti a
potřebná nastavení.

Po instalaci Minicondy se je potřeba vytvořit tzv. `conda environment`, k instalaci
k instalaci se použije následující příkaz:

```bash
$ cd path/to/disertacka/repository
$ conda env create -f environment.yml
```

Po nainstalování je nutné jej aktivovat:

```bash
# Linux or Mac OS X
$ source activate phd-thesis-env
```

Activate na Windows:

```cmd
rem Windows
activate phd-thesis-env
```

## Testování

Ke všem Python skriptům jsou připraveny unit testy. Testy je nutné spouštět ve složce modulu (podsložka).

```bash
$ cd path/to/disertacka/module
$ python -m unittest discover
```

Pro spuštění konrétního testu je potřeba specifikovat cestu k metodě s testem, viz ukázka

```bash
$ cd path/to/disertacka/module
$ python -m unittest test.jmeno_souboru_s_testy.TestCase.test
```

> Pokud cesta není specifikována až ke konrétní metodě jsou spuštěny všechny testy odpovídající této cestě.
