from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta


class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.__rendszam = rendszam
        self.__tipus = tipus
        self.__berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self.__rendszam

    @property
    def tipus(self):
        return self.__tipus

    @property
    def berleti_dij(self):
        return self.__berleti_dij

    @abstractmethod
    def adatok(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ferohely):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__ferohely = ferohely

    @property
    def ferohely(self):
        return self.__ferohely

    def adatok(self):
        return f"Személyautó - rendszám: {self.rendszam}, típus: {self.tipus}, díj: {self.berleti_dij} Ft/nap, férőhely: {self.ferohely}"


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__teherbiras = teherbiras

    @property
    def teherbiras(self):
        return self.__teherbiras

    def adatok(self):
        return f"Teherautó - rendszám: {self.rendszam}, típus: {self.tipus}, díj: {self.berleti_dij} Ft/nap, teherbírás: {self.teherbiras} kg"


class Berles:
    def __init__(self, auto, datum, berlo_neve):
        self.__auto = auto
        self.__datum = datum
        self.__berlo_neve = berlo_neve

    @property
    def auto(self):
        return self.__auto

    @property
    def datum(self):
        return self.__datum

    @property
    def berlo_neve(self):
        return self.__berlo_neve

    def adatok(self):
        return f"Bérlő: {self.berlo_neve}, autó: {self.auto.rendszam} - {self.auto.tipus}, dátum: {self.datum}, ár: {self.auto.berleti_dij} Ft"


class Autokolcsonzo:
    def __init__(self, nev):
        self.__nev = nev
        self.__autok = []
        self.__berlesek = []

    @property
    def nev(self):
        return self.__nev

    def auto_hozzaadas(self, auto):
        self.__autok.append(auto)

    def autok_listazasa(self):
        if len(self.__autok) == 0:
            print("Nincs autó a rendszerben.")
        else:
            print("\nAutók listája:")
            for auto in self.__autok:
                print(auto.adatok())

    def berlesek_listazasa(self):
        if len(self.__berlesek) == 0:
            print("Nincs aktuális bérlés.")
        else:
            print("\nAktuális bérlések:")
            for berles in self.__berlesek:
                print(berles.adatok())

    def auto_keresese(self, rendszam):
        for auto in self.__autok:
            if auto.rendszam == rendszam:
                return auto
        return None

    def foglalt_e(self, rendszam, datum):
        for berles in self.__berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                return True
        return False

    def auto_berlese(self, rendszam, datum, berlo_neve):
        auto = self.auto_keresese(rendszam)

        if auto is None:
            raise ValueError("Nincs ilyen rendszámú autó.")

        if datum < date.today():
            raise ValueError("Múltbeli dátumra nem lehet bérlést rögzíteni.")

        if self.foglalt_e(rendszam, datum):
            raise ValueError("Ez az autó ezen a napon már foglalt.")

        uj_berles = Berles(auto, datum, berlo_neve)
        self.__berlesek.append(uj_berles)

        return auto.berleti_dij

    def berles_lemondasa(self, rendszam, datum):
        for berles in self.__berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self.__berlesek.remove(berles)
                return True

        raise ValueError("Nem található ilyen bérlés.")


def datum_bekeres():
    datum_szoveg = input("Add meg a dátumot ÉÉÉÉ-HH-NN formátumban: ")

    try:
        datum = datetime.strptime(datum_szoveg, "%Y-%m-%d").date()
        return datum
    except ValueError:
        raise ValueError("Hibás dátum formátum. Példa: 2026-05-24")


def kezdo_adatok():
    kolcsonzo = Autokolcsonzo("Mobilauto+ Kft")

    auto1 = Szemelyauto("ABC-123", "Toyota Corolla", 15000, 5)
    auto2 = Szemelyauto("DEF-456", "Suzuki Swift", 12000, 5)
    auto3 = Teherauto("GHI-789", "Ford Transit", 25000, 1200)

    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)

    
    holnap = date.today() + timedelta(days=1)
    holnaputan = date.today() + timedelta(days=2)
    harmadik_nap = date.today() + timedelta(days=3)

    kolcsonzo.auto_berlese("ABC-123", holnap, "Teszt Elek")
    kolcsonzo.auto_berlese("DEF-456", holnap, "Kovács Géza")
    kolcsonzo.auto_berlese("GHI-789", holnaputan, "Polt Péter")
    kolcsonzo.auto_berlese("ABC-123", harmadik_nap, "Kovács Anna")

    return kolcsonzo


def menu():
    print("\n--- AUTÓKÖLCSÖNZŐ RENDSZER ---")
    print("1. Autók listázása")
    print("2. Autó bérlése")
    print("3. Bérlés lemondása")
    print("4. Bérlések listázása")
    print("0. Kilépés")


def main():
    kolcsonzo = kezdo_adatok()

    print("Üdvözöllek!")
    print("Kölcsönző neve:", kolcsonzo.nev)

    while True:
        menu()
        valasztas = input("Válassz egy menüpontot: ")

        try:
            if valasztas == "1":
                kolcsonzo.autok_listazasa()

            elif valasztas == "2":
                print("\nAutó bérlése")
                kolcsonzo.autok_listazasa()

                rendszam = input("Add meg a rendszámot: ").upper()
                datum = datum_bekeres()
                berlo_neve = input("Add meg a bérlő nevét: ")

                ar = kolcsonzo.auto_berlese(rendszam, datum, berlo_neve)
                print("Sikeres bérlés!")
                print("Fizetendő összeg:", ar, "Ft")

            elif valasztas == "3":
                print("\nBérlés lemondása")
                kolcsonzo.berlesek_listazasa()

                rendszam = input("Add meg a rendszámot: ").upper()
                datum = datum_bekeres()

                kolcsonzo.berles_lemondasa(rendszam, datum)
                print("A bérlés lemondása sikeres.")

            elif valasztas == "4":
                kolcsonzo.berlesek_listazasa()

            elif valasztas == "0":
                print("Kilépés...")
                break

            else:
                print("Nincs ilyen menüpont.")

        except ValueError as hiba:
            print("Hiba:", hiba)


main()
