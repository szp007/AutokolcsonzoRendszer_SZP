from abc import ABC, abstractmethod
from datetime import datetime

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def __str__(self):
        pass

class Szemelyauto(Auto):
    def __str__(self):
        return f"Személyautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap"

class Teherauto(Auto):
    def __str__(self):
        return f"Teherautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap"

class Berles:
    def __init__(self, auto, ugyfel_nev, datum):
        self.auto = auto
        self.ugyfel_nev = ugyfel_nev
        self.datum = datum

    def __str__(self):
        return f"Bérlés - Autó: {self.auto.rendszam}, Ügyfél: {self.ugyfel_nev}, Dátum: {self.datum}"

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def autok_hozzaadasa(self, auto):
        self.autok.append(auto)

    def auto_berlese(self, rendszam, ugyfel_nev, datum):
        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            print("Hiba: Ilyen autó nem található.")
            return

        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            print("Hiba: Érvénytelen dátum. A formátum helyesen: ÉÉÉÉ-HH-NN.")
            return

        if any(b.auto.rendszam == rendszam and b.datum == datum for b in self.berlesek):
            print("Hiba: Ez az autó már foglalt a megadott dátumon.")
            return

        self.berlesek.append(Berles(auto, ugyfel_nev, datum))
        print(f"A bérlés sikeres! Az ár: {auto.berleti_dij} Ft.")

    def berlesek_listazasa(self):
        if not self.berlesek:
            print("Nincs aktív bérlés.")
        for berles in self.berlesek:
            print(berles)

    def berles_lemondasa(self, rendszam, datum):
        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            print("Hiba: Érvénytelen dátum. A formátum helyesen: ÉÉÉÉ-HH-NN.")
            return

        berles = next((b for b in self.berlesek if b.auto.rendszam == rendszam and b.datum == datum), None)
        if not berles:
            print("Hiba: A megadott bérlés nem található.")
            return

        self.berlesek.remove(berles)
        print("A bérlés sikeresen le lett mondva.")

if __name__ == "__main__":
    kolcsonzo = Autokolcsonzo("Teszt Autókölcsönző")

    auto1 = Szemelyauto("KRH-245", "Toyota Corolla", 10000)
    auto2 = Szemelyauto("IEF-147", "Honda Civic", 12000)
    auto3 = Teherauto("AAA-007", "Ford Transit", 15000)
    kolcsonzo.autok_hozzaadasa(auto1)
    kolcsonzo.autok_hozzaadasa(auto2)
    kolcsonzo.autok_hozzaadasa(auto3)

    kolcsonzo.berlesek.append(Berles(auto1, "Farkas Péter", "2024-11-23"))
    kolcsonzo.berlesek.append(Berles(auto2, "Kiss Anna", "2024-11-27"))
    kolcsonzo.berlesek.append(Berles(auto3, "Szabó István", "2024-11-27"))
    kolcsonzo.berlesek.append(Berles(auto1, "NaHuncut Kata", "2024-11-28"))

    while True:
        print("\n=== Autókölcsönző Rendszer ===")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")

        valasztas = input("Válasszon egy lehetőséget: ")

        if valasztas == "1":
            rendszam = input("Adja meg az autó rendszámát: ")
            ugyfel_nev = input("Adja meg az ügyfél nevét: ")
            datum = input("Adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.auto_berlese(rendszam, ugyfel_nev, datum)
        elif valasztas == "2":
            rendszam = input("Adja meg az autó rendszámát: ")
            datum = input("Adja meg a lemondás dátumát (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.berles_lemondasa(rendszam, datum)
        elif valasztas == "3":
            kolcsonzo.berlesek_listazasa()
        elif valasztas == "4":
            print("Kilépés a rendszerből. Viszontlátásra!")
            break
        else:
            print("Hiba: Érvénytelen választás.")
