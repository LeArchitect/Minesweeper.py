import random
import re
import time
from operator import itemgetter
import sys
        
# Rakentaa miinakentän
def miinataul(kentta, leveys, korkeus, miinalkm):
    for i in range(int(miinalkm)):
        a, b = randomruutu(kentta, korkeus, leveys)
        arvo = itemgetter(a)(kentta[b])
        if arvo == "X":
            while arvo == "X":
                a, b = randomruutu(kentta, korkeus, leveys)
                arvo = itemgetter(a)(kentta[b])
        kentta[b][a] = "X"
    return kentta

# sattumanvaraisen ruudun valitseminen
def randomruutu(kentta, korkeus, leveys):
    leveys = len(kentta[0])
    korkeus = len(kentta)

    a = random.randint (0, leveys - 1)
    b = random.randint (0, korkeus -1)

    return (a, b)
    
#Rakentaa miinakentän, jossa ruutujen läheisten mminojen lkm
def naapurit(naapuri, korkeus, leveys, kentta, miinalkm):
    kentta = miinataul(kentta, leveys, korkeus, miinalkm)
    for j in range(korkeus):
        for i in range(leveys):
            if kentta[j][i] != "X":
                    if j == 0:
                        if i == 0:
                            naapurit = kentta[j][i+1], kentta[j+1][i], kentta[j+1][i+1]
                        elif i == leveys-1:
                            naapurit = kentta[j][i-1], kentta[j+1][i-1], kentta[j+1][i]
                        else:
                            naapurit = kentta[j][i-1], kentta[j][i+1], kentta[j+1][i-1], kentta[j+1][i], kentta[j+1][i+1]
                    elif j == korkeus-1:
                        if i == 0:
                            naapurit = kentta[j-1][i], kentta[j-1][i+1], kentta[j][i+1]
                        elif i == leveys-1:
                            naapurit = kentta[j-1][i-1], kentta[j-1][i], kentta[j][i-1]
                        else:
                            naapurit = kentta[j-1][i-1], kentta[j-1][i], kentta[j-1][i+1], kentta[j][i-1], kentta[j][i+1]
                    elif i == 0:
                        naapurit = kentta[j-1][i], kentta[j-1][i+1], kentta[j][i+1], kentta[j+1][i], kentta[j+1][i+1]
                    elif i == leveys-1:
                        naapurit = kentta[j-1][i-1], kentta[j-1][i], kentta[j][i-1], kentta[j+1][i-1], kentta[j+1][i]
                    else:
                        naapurit = kentta[j-1][i-1], kentta[j-1][i], kentta[j-1][i+1], kentta[j][i-1], kentta[j][i+1], kentta[j+1][i-1], kentta[j+1][i], kentta[j+1][i+1]
                    naapurit = naapurit.count("X")
                    if naapurit == 0:
                        naapuri[j][i] = "#"
                    else:
                        naapuri[j][i] = str(naapurit)
            elif kentta[j][i] == "X":
                    naapuri[j][i] = str("X")
    return naapuri
                 
# piirtää ja määrittää taulukon
def taulukko(taul, leveys, korkeus):

    hor = '   ' + (4 * leveys * '-') + '-'

    # Ylä numero rivi ja ensimmäinen katkoviiva
    vali = "    "
    for n in range(0, leveys):
        if n == 0:
            print(vali, n, end="   ")
        elif n <= 9:
            print(n, end="   ")
        elif n >= 10 and n <= 99:
            print(n, end="  ")
        else:
            print(n, end="   ")
    print()
    print(hor)

    # kaikki loput
    for idx, i in enumerate(taul):
        rivi = '{0:2} |'.format(idx)

        for j in i:
            rivi = rivi + ' ' + j + ' |'

        print(rivi + '\n' + hor)

    print('')           

#tallentaa pelitilaston
def tallenna_tilasto(tiedosto, pvm, kesto, vaikeusaste, vuorot, tulos):
    try:
        with open(tiedosto, "a") as kohde:
            kohde.write("{}, {:.2f} sekuntia, {}, {} vuoroa, {}\n".format(pvm, kesto, vaikeusaste, vuorot, tulos))
    except:
        pass    
    
# lukee tilaston
def lue_tilasto(tiedosto):
    try:
        with open(tiedosto) as lahde:
            for rivi in lahde:
                rivi = rivi.strip("\n")
                pvm, kesto, vaikeusaste, vuorot, tulos = rivi.split(",")
                print("{}, {}, {}, {}, {}".format(pvm, kesto, vaikeusaste, vuorot, tulos))
    except:
        pass
        
#taulukon leveyden valinta
def width():
    while True:
        try:
            leveys = int(float(input("\n Choose Width: ")))
        except ValueError:
            print("\n Not Valid Choice Try again")
            continue
        else:
            if leveys > 1:
                print("\n OK")
                return leveys
            elif leveys == 0 or leveys == 1:
                print("Thats too small to play on")
                continue
            else:
               print("\n Not Valid Choice Try again")
               return width()
       
#taulukon korkeuden valinta   
def height():
    while True:
        try:
            korkeus = int(float(input("\n Choose Height: ")))
        except ValueError:
            print("\n Not Valid Choice Try again")
            continue
        else:
            if korkeus > 1:
                print("\n OK")
                return korkeus
            elif korkeus == 0 or korkeus == 1:
                print("Thats too small to play on")
                continue
            else:
               print("\n Not Valid Choice Try again")
               return height()

    while True:
        try:
            korkeus = int(float(input("\n Choose Height: ")))
        except ValueError:
            print("\n Not Valid Choice Try again")
            continue
        else:
            if korkeus > 1:
                print("\n OK")
                return korkeus
            elif korkeus == 0 or korkeus == 1:
                print("Thats too small to play on")
                continue
            else:
               print("\n Not Valid Choice Try again")
               return height()
        
# Vaikeusasteen valinta eli samalla minojen lukumäärät
def minekpl(leveys, korkeus):
    maksimimiinat = (leveys * korkeus)
    Helppo = maksimimiinat * 0.2
    Keskitaso = maksimimiinat * 0.4
    Vaikea = maksimimiinat * 0.6                                    
    while True:
        print("""
        1. Helppo
        2. Keskitaso
        3. Vaikea
        4. Custom
        """)
        try:
            kysely = input("Valitse vaikeusaste: ")
        except ValueError:
            print("Virheellinen syöte, yritä uudelleen.")
            continue
        else:
            if kysely == "1":
                print("Vaikeusasteeksi valittu helppo.")   
                vaikeusaste = "Helppo"
                return Helppo, vaikeusaste
            elif kysely == "2":
                print("Vaikeusasteeksi valittu keskitaso.")
                vaikeusaste = "Keskitaso"
                return Keskitaso, vaikeusaste
            elif kysely == "3":
                print("Vaikeusasteeksi valittu vaikea.")
                vaikeusaste = "Vaikea"
                return Vaikea, vaikeusaste
            elif kysely == "4":
                print("Vaikeusasteeksi valittu custom.")
                vaikeusaste = "Custom"
                while True:
                        try:
                            miinakpl = int(input("Anna miinojen määrä(1 - {}): ".format (maksimimiinat - 1)))
                        except ValueError:
                            print("Syötä miinojen lukumäärä kokonaislukuna.")
                            continue
                        else:
                            if miinakpl <= 0 or miinakpl > maksimimiinat - 1:
                                print("Virheellinen miinojen määrä.")
                                continue
                            return miinakpl, vaikeusaste

# main valikko
def main():
    while True:
        print("""
        1. Uusi peli
        2. Tilastot
        3. Lopeta
        """)
        ans = input("Valitse toiminto: ")
        if ans == "1":
            print("Uusi peli")
            return
        elif ans == "2":
            print("Näytetään tilastot:")
            lue_tilasto("tilasto.txt")   
        elif ans == "3":
            print("Lopetetaan...")
            sys.exit("Kiitos näkemiin. ")
        elif ans == None:
            print("Virheellinen syöte, yritä uudelleen.")
        else:
            print("Virheellinen syöte, yritä uudelleen.")

#arvojen alustus  ja main menu
def alustus():
    main()
    leveys = width()
    korkeus = height()
    miinalkm, vaikeusaste = minekpl(leveys, korkeus)
    taul = [["o" for i in range(leveys)] for i in range(korkeus)]
    kentta = [[" " for i in range(leveys)] for i in range(korkeus)]
    naapuri = [[" " for i in range(leveys)] for i in range(korkeus)]
    miinakentta = naapurit(naapuri, leveys, korkeus, kentta, miinalkm)
    vuoro = 0
    aloitusaika = time.time()
    tulos = 0
    return leveys, korkeus, miinalkm, miinakentta, vuoro, taul, aloitusaika, tulos, vaikeusaste
   
# varsinainen pelin käsittely alkaa jostain täältä
def peli(leveys, korkeus, miinalkm, miinakentta, vuoro, taul, aloitusaika, tulos):
        while True:
            if sum(x.count("o") for x in taul) == sum(x.count("X") for x in miinakentta):
                    print("Onneksi olkoon, voitit pelin!")
                    tulos = "Voitto"
                    taulukko(miinakentta, leveys, korkeus)
                    vaikeusaste = (miinalkm / (leveys * korkeus))
                    vuorot = vuoro
                    loppuaika = time.time()
                    kesto = loppuaika - aloitusaika
                    pvm = time.strftime("%d-%m-%Y %H:%M:%S")
                    return pvm, kesto, vuorot, tulos
            taulukko(taul, leveys, korkeus)
            koord = input("Anna koordinaatit muodossa X Y ").split(" ")
            if len(koord) == 2:
                try:
                    x, y = int(koord[0]),int(koord[1])  
                    if miinakentta[y][x] == "X":
                        print("BOOM!")
                        print("Hävisit pelin.")
                        taulukko(miinakentta, leveys, korkeus)
                        tulos = "Häviö"
                        vaikeusaste = (miinalkm / (leveys * korkeus))
                        vuorot = vuoro
                        loppuaika = time.time()
                        kesto = loppuaika - aloitusaika
                        pvm = time.strftime("%d-%m-%Y %H:%M:%S")
                        return pvm, kesto, vuorot, tulos
                    else:
                        if miinakentta[y][x] == "#":
                            lista = [(x, y)]
         
                            while len(lista) > 0:
         
                                p = lista.pop()
                                x, y = p[0], p[1]
                                if miinakentta[y][x] == "#":
                                        taul[y][x] = " "
                                        miinakentta[y][x] = " "  
                                if x-1 >= 0:
                                        if miinakentta[y][x-1] == "#":
                                                lista.append((x-1, y))
                                        else:
                                                arvo = miinakentta[y][x-1]
                                                taul[y][x-1] = str(arvo)
                          
                                if x-1 >= 0 and y-1 >= 0:
                                        if miinakentta[y-1][x-1] == "#":
                                                lista.append((x-1, y-1))
                                        else:
                                                arvo = miinakentta[y-1][x-1]
                                                taul[y-1][x-1] = str(arvo)
                                                                           
                                if y-1 >= 0:
                                        if miinakentta[y-1][x] == "#":
                                                lista.append((x, y-1))
                                        else:
                                                arvo = miinakentta[y-1][x]
                                                taul[y-1][x] = str(arvo)
                      
                                if y-1 >= 0 and x+1 < leveys:
                                        if miinakentta[y-1][x+1] == "#":
                                                lista.append((x+1, y-1))
                                        else:
                                                arvo = miinakentta[y-1][x+1]
                                                taul[y-1][x+1] = str(arvo)
                        
                                if x+1 < leveys:
                                        if miinakentta[y][x+1] == "#":
                                                lista.append((x+1, y))
                                        else:
                                                arvo = miinakentta[y][x+1]
                                                taul[y][x+1] = str(arvo)
                                                
                                if x+1 < leveys and y+1 < korkeus:
                                        if miinakentta[y+1][x+1] == "#":
                                                lista.append((x+1, y+1))
                                        else:
                                                arvo = miinakentta[y+1][x+1]
                                                taul[y+1][x+1] = str(arvo)
                       
                                if y+1 < korkeus:
                                        if miinakentta[y+1][x] == "#":
                                                lista.append((x, y+1))
                                        else:
                                                arvo = miinakentta[y+1][x]
                                                taul[y+1][x]= str(arvo)
                    
                                if x-1 >= 0 and y+1 < korkeus:
                                        if miinakentta[y+1][x-1] == "#":
                                                lista.append((x-1, y+1))
                                        else:
                                                arvo = miinakentta[y+1][x-1]
                                                taul[y+1][x-1] = str(arvo)
                            vuoro = vuoro + 1
                            continue
                                
                        else:
                            ruutu = itemgetter(x)(miinakentta[y])
                            taul[y][x] = str(ruutu)
                            vuoro = vuoro + 1
                            continue
                except(ValueError, TypeError):
                      print("Virheellinen syöte, yritä uudelleen.") 
                      continue
            
            else:
                    print("Virheellinen syöte, yritä uudelleen.")
                    continue
       
        vuorot = vuoro
        loppuaika = time.time()
        kesto = loppuaika - aloitusaika
        pvm = time.strftime("%d-%m-%Y %H:%M:%S")
        return pvm, kesto, vaikeusaste, vuorot, tulos

# Toiminnallinen looppi koko pelille          
while True:
    leveys, korkeus, miinalkm, miinakentta, vuoro, taul, aloitusaika, tulos, vaikeusaste = alustus()
    pvm, kesto, vuorot, tulos = peli(leveys, korkeus, miinalkm, miinakentta, vuoro, taul, aloitusaika, tulos)
    tallenna_tilasto("tilasto.txt", pvm, kesto, vaikeusaste, vuorot, tulos)
