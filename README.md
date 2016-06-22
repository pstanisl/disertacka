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
