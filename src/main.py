#!/usr/bin/env python3

import random
from time import sleep

class Spiller:
    def __init__(self, navn, samling, helse=20, mana = 10, naaverende_miljo=None):
        self.navn = navn
        self.samling = samling
        self.helse = helse
        self.mana = mana
        self.handlinger = []
        self.naaverende_miljo = naaverende_miljo

    def spiller_angrep(self):
        #Rulle for angrep og for skade
        paafortSkade = random.randint(1,5)
        angrep_gjenstand = [item for item in self.samling if item.type == "angrepsvåpen"]
        våpen_styrke = sum(gjenstand.egenskap for gjenstand in angrep_gjenstand)
        paafortSkade = paafortSkade + våpen_styrke
        sleep(2)
        print(f"Du angriper monsteret og tar {paafortSkade} i skade")
        self.naaverende_miljo.monster.ta_skade(paafortSkade)
    
    def ta_skade(self, skade):
        # Man tar skade basert på angrepet minus det man har som beskyttelse
        forsvar_gjenstand = [item for item in self.samling if item.type == "forsvar"]
        beskyttelse = sum(gjenstand.egenskap for gjenstand in forsvar_gjenstand)
        self.helse -= (skade - beskyttelse)
        self.helse = self.helse - beskyttelse
        sleep(2)
        print(f"Din helse er nå {self.helse}")

    def utforsk(self, miljo):
        #Gi en beskrivelse av miljøet man er i
        gjenstand = self.naaverende_miljo.gjenstand
        if gjenstand == None:
            sleep(2)
            print("Du utforsker området du er i men du finner ingenting nyttig")
        else:
            sleep(2)
            print(self.naaverende_miljo.beskrivelseAvGjenstand)
            for item in gjenstand:
                print(f"Du legger til i samlingen din: {item.navn}, {item.beskrivelse}")
                self.samling.append(item)

 
    
    def gaa(self, retning):
        #Gå fra et miljø til et annet
        if retning in self.naaverende_miljo.utganger:
            self.naaverende_miljo = self.naaverende_miljo.utganger[retning]
            sleep(2)
            print(self.naaverende_miljo.beskrivelse)

        else:
            sleep(2)
            print("Du kan ikke gå den veien!")
    
    def handling(self, spillerInput):
        deler = spillerInput.split(" ")
        verb = deler[0]
        if verb == "gå":
            if len(deler) == 2:
                self.gaa(deler[1])
            else:
                sleep(2)
                print("Gå hvor?")
        elif verb == "utforsk":
            self.utforsk(self.naaverende_miljo)
        else: 
            print(f"Jeg forstår ikke '{spillerInput}'")

    
class Miljo:
    def __init__(self, beskrivelse, type, monster=None, gjenstand=None, utganger=None, beskrivelseAvGjenstand=None):
        self.beskrivelse = beskrivelse
        self.type = type
        self.monster = monster
        self.gjenstand = gjenstand
        self.utganger = {} 
        self.beskrivelseAvGjenstand = beskrivelseAvGjenstand
    
    def legg_til_utgang(self, retning, miljo):
        self.utganger[retning] = miljo

class Monster:
    def __init__(self, navn, plassering, helsepoeng, handling):
        self.navn = navn
        self.plassering = plassering
        self.helsepoeng = helsepoeng
        self.handling = handling

    def monsterAngrep(self, spiller):
        #Påfører spiller et visst antall skade om den ruller bra
        paafortSkade = random.randint(1,5)
        sleep(2)
        print(f"Monsteret påfører deg {paafortSkade} i skade!")
        spiller.ta_skade(paafortSkade)


    def ta_skade(self, skade):
        self.helsepoeng -= skade
        if self.helsepoeng >= 1:
            sleep(2)
            print(f"Monsterets helse er nå {self.helsepoeng}")   
        else:
            sleep(2)
            print("Du har drept monsteret!")

class Gjenstand:
    def __init__(self, navn, type, beskrivelse, egenskap):
        self.navn = navn
        self.type = type
        self.beskrivelse = beskrivelse
        #Forsvar gir x i egenskap som gjelder forsvar, mens angrepsvåpen gir x i egenskap som gjelder skade-påført
        self.egenskap = egenskap

def combat_sequence(spiller, monster):
    while spiller.helse > 0 and monster.helsepoeng > 0:
        spiller.spiller_angrep()
        if monster.helsepoeng >= 1:
            monster.monsterAngrep(spiller)
        else:
            spiller.naaverende_miljo.monster = None  # Remove the monster from the current environment
            break

    if spiller.helse <= 0:
        sleep(2)
        print("Du er død. Spillet er over.")
        return False  # Return False if the player died
    else:
        return True  # Return True if the player survived

def main():

    #Noen monstre
    goblin= Monster("Goblin", "På andre siden av rommet i høyre hjørne", 10, "Slå med sverd")
    boss_goblin = Monster("Goblin", "Midt i rommet", 20, "Slå med sverd")
    edderkopp = Monster("Edderkopp", "På andre siden av rommet ligger den på lur", 5, "Biter")

    #Noen gjenstander
    sverd= Gjenstand("Sverd +3","angrepsvåpen", "Et vanlig sverd som gjør dine angrep mer dødelige", 3)
    skjold=Gjenstand("Skjold +3", "forsvar", "Et vanlig skjold som gir beskyttelse i kamp", 3)

    # Noen rom
    korridor1 = Miljo("Du er i en mørk korridor som leder til en dør i andre enden \nI venstre hjørne ser du en haug med søppel. \nVil du se gjennom haugen (utforsk haugen) eller gå gjennom døren (gå vest)?", "rom", gjenstand=[sverd, skjold], beskrivelseAvGjenstand="Du graver gjennom søppelhauen og finner et sverd og et skjold. \nDu er nå klar for å forsvare deg om du må!")
    rom1 = Miljo("Du er i et stort mørkt rom. Det er to utganger i rommet (øst og vest). Foran deg står en Goblin","rom", monster=goblin )
    korridor2 = Miljo("Du er i enda en mørk korridor som leder til en dør i andre enden (sør)", "rom", None, None)
    rom2 = Miljo("Du er i et stort mørkt rom. Foran deg står en stor Goblin. Bak denne Goblinen ser du en dør (sør)","rom", monster=boss_goblin)
    korridor3 = Miljo("Du er i enda en mørk korridor som leder til en dør i andre enden (øst). \nForan deg ser du i et hjørne at det er en ganske stor edderkopp som lusker. \nDen hopper frem for å angripe. Du stiller deg klar og slår til! ", "rom", monster=edderkopp)
    rom3 = Miljo("Du er i et stort mørkt rom. Foran deg ser du mange skatter! Du plukker opp det du kan. Utgangen av hulen er rett frem (øst)","rom", monster=None)
    korridor4 = Miljo("Du er i enda en mørk korridor som leder til en dør i andre enden. Gratulerer du har vunnet spillet! \n(Avslutt spillet med å skrive 'exit')", "rom", None, None)


    #Koble sammen miljøene
    korridor1.legg_til_utgang("vest", rom1)
    rom1.legg_til_utgang("øst", korridor1)
    rom1.legg_til_utgang("vest", korridor2)
    korridor2.legg_til_utgang("øst", rom1)
    korridor2.legg_til_utgang("sør", rom2)
    rom2.legg_til_utgang("nord", korridor2)
    rom2.legg_til_utgang("sør", korridor3)
    korridor3.legg_til_utgang("nord", rom2)
    korridor3.legg_til_utgang("øst", rom3)
    rom3.legg_til_utgang("vest", korridor3)
    rom3.legg_til_utgang("øst", korridor4)

    #Første miljø
    naaverende_miljo = korridor1

    # Spilleren
    spiller = Spiller("Conan", samling=[], naaverende_miljo=naaverende_miljo)

    #Beskrivelse av miljøet

    print("Velkommen til dette spillet! Bli med på en reise, og se om du overlever til slutt")
    sleep(2)
    print(naaverende_miljo.beskrivelse)

    #Spill loop
    while spiller.helse >= 1:
        #Spør etter spillerinput
        spillerInput = input("> ")

        #Mulighet for spilleren å avslutte spillet
        if spillerInput.lower() in ["quit", "exit", "q"]:
            print("Takk for at du spilte! Ha det bra!")
            break  # This will exit the loop and end the game
        else:
            #Hvilken handling gjør spilleren?
            spiller.handling(spillerInput)

        #Monster? Kjemp eller flykt?
        if spiller.naaverende_miljo.monster is not None:
            still_alive = combat_sequence(spiller, spiller.naaverende_miljo.monster)
            if not still_alive:
                break
        

if __name__ == "__main__":
    main()