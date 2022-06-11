
# KODA- Projekt

  

Koder i dekoder wykładniczego kodu Golomba


## Zaspół

Damian Łysomirski

Rafał Wiercioch

Marcin Skinder

Robert Kaczmarski

  

## Pobranie i instalacja

```

# Klonowanie repozytorium

git clone https://github.com/hornisslaw/exponencial-golomb-coding.git

cd exponencial-golomb-coding

  

# Stworzenie i aktywacja wirtualnego środowiska

python -m venv venv

source ./venv/bin/activate

  

# instalacja potrzebnych bibliotek

pip install -r requirements.txt

```

  

## Opis parametrów i przykład wywołania programu

Parametry wywołania programu:

`-k` rząd

`-f` relatywna ścieżka do pliku z danymi

`-d` wstępne kodowanie różnicowe wartością średnią obrazu z mapowaniem wartości

  

```
python main.py -k 2 -f "resources\\data\\geometr_09.pgm"
```