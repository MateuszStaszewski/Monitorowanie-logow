#   Monitorowanie Logów 

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)

Prosty i skuteczny dashboard stworzony w technologii **Streamlit**, służący do monitorowania bezpieczeństwa serwera poprzez analizę plików logów (`access.log`). Narzędzie pozwala na szybką identyfikację prób nieautoryzowanego dostępu (błędy 401), wizualizację aktywności adresów IP oraz łatwe zarządzanie listą zablokowanych adresów.

##  Główne funkcje

* **Analiza logów w czasie rzeczywistym:** Automatyczne skanowanie pliku `access.log`.
* **Detekcja Brute-Force:** Wykrywanie adresów IP generujących podejrzaną liczbę błędów 401.
* **Zarządzanie bezpieczeństwem:** Możliwość blokowania i odblokowywania adresów IP bezpośrednio z poziomu panelu.
* **Wizualizacja:** Interaktywny wykres słupkowy prezentujący najaktywniejsze adresy IP.
* **Nowoczesny UI:** Ciemny motyw, czytelne metryki i intuicyjny interfejs.

##  Technologie
* **Python**
* **Streamlit** (Framework do aplikacji webowych)
* **Pandas** (Analiza danych)
* **Regex (re)** (Parsowanie logów)

##  Instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone \https://github.com/TWOJ\_LOGIN/TWOJE\_REPO.git
   cd "Monitorowanie logów"
2. Stwórz środowisko wirtualne: `python -m venv venv` , `venv\\Scripts\\activate`
3. **Zainstaluj zależności:** `pip install -r requirements.txt`

##  Uruchomienie
*  `streamlit run dashboard.py`

##  Struktura projektu
* dashboard.py – główny skrypt aplikacji.
* access.log – plik źródłowy z logami serwera.
* requirements.txt – lista bibliotek niezbędnych do działania.
* blocked\_ips.txt – baza zablokowanych adresów IP (generowana automatycznie).
* .gitignore – plik ignorujący dane wrażliwe i pliki tymczasowe.
