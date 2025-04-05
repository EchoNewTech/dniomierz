import tkinter as tk
from tkinter import messagebox
import re
from math import floor

# Funkcja sprawdzająca, czy rok jest przestępny
def czy_przestepny(rok):
    """Sprawdza, czy rok jest przestępny.
    Args:
        rok (int): Rok do sprawdzenia.
    Returns:
        bool: True, jeśli rok jest przestępny, False w przeciwnym razie.
    """
    return (rok % 4 == 0 and rok % 100 != 0) or rok % 400 == 0

# Funkcja obliczająca, który to dzień roku
def oblicz_dzien_roku(dzien, miesiac, rok):
    """Oblicza numer dnia w roku dla podanej daty.
    Args:
        dzien (int): Dzień miesiąca.
        miesiac (int): Miesiąc.
        rok (int): Rok.
    Returns:
        int: Numer dnia w roku.
    """
    dni_w_miesiacach = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if czy_przestepny(rok):
        dni_w_miesiacach[1] = 29
    return sum(dni_w_miesiacach[:miesiac - 1]) + dzien

# Funkcja obliczająca dzień tygodnia
def oblicz_dzien_tygodnia(dzien, miesiac, rok):
    """Oblicza dzień tygodnia dla podanej daty.
    Args:
        dzien (int): Dzień miesiąca.
        miesiac (int): Miesiąc.
        rok (int): Rok.
    Returns:
        str: Nazwa dnia tygodnia.
    """
    YY = (rok - 1) % 100
    C = (rok - 1) - YY
    G = floor(YY + YY / 4)
    dzien_tyg1 = int((((C / 100) % 4) * 5) + G) % 7
    dzien_tyg = (dzien_tyg1 + oblicz_dzien_roku(dzien, miesiac, rok) - 1) % 7
    dni_tygodnia = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    return dni_tygodnia[dzien_tyg]

# Funkcja obliczająca numer tygodnia
def oblicz_numer_tygodnia(dzien, miesiac, rok):
    """Oblicza numer tygodnia dla podanej daty.
    Args:
        dzien (int): Dzień miesiąca.
        miesiac (int): Miesiąc.
        rok (int): Rok.
    Returns:
        int: Numer tygodnia.
    """
    dzien_roku = oblicz_dzien_roku(dzien, miesiac, rok)
    pierwszy_dzien_tygodnia = (oblicz_dzien_roku(1, 1, rok) - 1) % 7
    return ((dzien_roku + pierwszy_dzien_tygodnia - 1) // 7) + 1

# Funkcja obsługująca sprawdzenie daty
def sprawdz_date():
    """Sprawdza datę wprowadzoną przez użytkownika i wyświetla wyniki."""
    data_wejsciowa = entry_data.get()
    wzorce = [
        re.compile(r"(\d{4})[./-](\d{1,2})[./-](\d{1,2})$"),  # yyyy-mm-dd
        re.compile(r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})$")  # dd-mm-yyyy
    ]
    dopasowanie = None
    for wzorzec in wzorce:
        dopasowanie = wzorzec.match(data_wejsciowa)
        if dopasowanie:
            break

    if dopasowanie:
        rok, miesiac, dzien = map(int, dopasowanie.groups()) if wzorce.index(wzorzec) == 0 else map(int, dopasowanie.groups()[::-1])

        if miesiac < 1 or miesiac > 12 or dzien < 1 or dzien > 31:
            messagebox.showerror("Błąd", "Nieprawidłowa data.")
            return
        if miesiac == 2 and ((czy_przestepny(rok) and dzien > 29) or (not czy_przestepny(rok) and dzien > 28)):
            messagebox.showerror("Błąd", "Nieprawidłowy dzień lutego.")
            return

        dzien_roku = oblicz_dzien_roku(dzien, miesiac, rok)
        dzien_tygodnia = oblicz_dzien_tygodnia(dzien, miesiac, rok)
        nr_tygodnia = oblicz_numer_tygodnia(dzien, miesiac, rok)
        przestepny_info = "Tak" if czy_przestepny(rok) else "Nie"

        # Ustaw kolor tła w zależności od dnia tygodnia
        if dzien_tygodnia == "Sobota" or dzien_tygodnia == "Niedziela":
            wynik_label.config(bg="lightblue")
        else:
            wynik_label.config(bg="lightgray")

        wynik_label.config(
            text=f"Dzień roku: {dzien_roku}\nNumer tygodnia: {nr_tygodnia}\nDzień tygodnia: {dzien_tygodnia}\nRok przestępny: {przestepny_info}",
        )
    else:
        messagebox.showerror("Błąd", "Nieprawidłowy format daty. Wprowadź w formacie yyyy-mm-dd lub dd-mm-yyyy")

# Tworzenie okna
root = tk.Tk()
root.title("Kalkulator daty")
root.geometry("350x250")

# Ramka
frame = tk.Frame(root)
frame.pack(pady=20)

# Etykieta
label_instrukcja = tk.Label(frame, text="Wprowadź datę (yyyy-mm-dd lub dd-mm-yyyy):")
label_instrukcja.pack()

# Pole tekstowe
entry_data = tk.Entry(frame)
entry_data.pack()

# Przycisk
button_sprawdz = tk.Button(frame, text="Sprawdź", command=sprawdz_date)
button_sprawdz.pack()

# Wynik
wynik_label = tk.Label(root, text="", bg="white")
wynik_label.pack(fill="both", expand=True, pady=10)

# Uruchomienie aplikacji
root.mainloop()
