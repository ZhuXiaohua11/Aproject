import csv
def läs_kommuneskattable_nr (filnamn):
    kommunskattable={}
    with open ( filnamn, mode ='r', encoding = "utf-8") as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)
        for rad in csv_reader:
            kommunskattable [rad[0]] = rad[1]
    return kommunskattable
filnamn=r"C:\Users\riddl\Desktop\python lektion\python\kommun_skatt_nr.csv"
kommunskatttable=läs_kommuneskattable_nr(filnamn)

def läs_skattetable (filnamnskatt):
    skattetable=[]
    with open (filnamnskatt, mode = 'r', encoding= "ISO-8859-1") as file:
        csv_reader=csv.reader(file, delimiter=';')
        next (csv_reader)
        for rad in csv_reader:
            skattetable.append({
                'tablenr':rad[2] ,
                'Inkomst Från':rad[3],
                'Inkomst t.o.m':rad[4],
                'skatt':rad[5] #anser alla använder Kolumn1
            })
    return skattetable
def hitta_avdragskatt(skattetable, skattetable_nr, månadslön):
    for rad in skattetable:
        if rad['tablenr']== skattetable_nr and float(rad['Inkomst Från'])<= månadslön <= float(rad['Inkomst t.o.m']):
            return rad['skatt']
    return 0
filnamnskatt = r"C:\Users\riddl\Desktop\python lektion\python\Skattetabell månadslön 2024.csv"
skattetable = läs_skattetable(filnamnskatt)


class Anställd:
    def __init__(self, namn, anställd_nr,kommunnamn):
        self.namn = namn
        self. anställd_nr = anställd_nr
        self.kommunnamn = kommunnamn
    def beräkna_månadslön(self):
        pass
    def skattetable_nr(self):
        self.skattetable_nr = kommunskatttable[self.kommunnamn]
        skatteavdrag = hitta_avdragskatt(skattetable, self.skattetable_nr, self.månadslön)
        nettolön = self.månadslön-float(skatteavdrag)
        print ( f"{self.namn} använder skattetabell {self.skattetable_nr}, och enligt skattetabellen är skatteavdraget {skatteavdrag}. Nettolönen är {nettolön:.2f} SEK" )
    
class Månadsanställd(Anställd):
    def __init__(self, namn, anställd_nr, kommunnamn, veckotimmar=40,):
        self.veckotimmar = veckotimmar
        super().__init__(namn, anställd_nr, kommunnamn)
    def beräkna_månadslön(self,månadslön, tjänstledigdgr, sjukdgr, semesterdgr):
        percent = self.veckotimmar/40
        if tjänstledigdgr > 5:
            tjänstledigavdrag = månadslön * 12 / 365 * tjänstledigdgr
        else:
            tjänstledigavdrag = månadslön / 21 * tjänstledigdgr
        sjukavdrag1_14 = månadslön * 12 / ( 52 * self.veckotimmar ) * sjukdgr
        sjuklön1_14 = 0.8 * månadslön * 12 / ( 52 * self.veckotimmar ) * sjukdgr
        Karensavdrag = sjuklön1_14 * 0.2
        semesterlöntillägg = månadslön * 0.008 * semesterdgr
        if sjukdgr <= 14:
            self.månadslön = ( månadslön - tjänstledigavdrag - sjukavdrag1_14 + sjuklön1_14 - Karensavdrag + semesterlöntillägg ) * percent
        else:
            sjukavdrag15_90= månadslön * 12 / 365 * ( sjukdgr - 14)
            self.månadslön=( månadslön - tjänstledigavdrag - sjukavdrag1_14 - sjukavdrag15_90 + sjuklön1_14 - Karensavdrag + semesterlöntillägg ) * percent
        print (f"{self.namn} har anställningsnummer {self.anställd_nr}, arbetar {self.veckotimmar} timmar per vecka, och månadslönen är {self.månadslön: .2f} SEK")

class Timanställd(Anställd):
    def __init__(self, namn, anställd_nr, kommunnamn, timmar):
        self.timmar = timmar
        super().__init__( namn, anställd_nr, kommunnamn )
    def beräkna_månadslön(self, timlön, sjuktimmar):
        sjuklön1_14 = timlön * 0.8 * sjuktimmar
        Karensavdrag = 0.2 * 0.8 * self.timmar * 12/52 * timlön #0.2*0.8*veckoarbetstid*timlön
        semersättning = (timlön * self.timmar + timlön * sjuktimmar ) * 0.13
        self.månadslön = (timlön * self.timmar + sjuklön1_14-Karensavdrag + semersättning )
        print (f"{self.namn} är en timanställd och har anställningsnummer {self.anställd_nr}. Hon arbetade {self.timmar} timmar den här månaden. Månadslön är {self.månadslön:.2f} SEK")
anställd1=Månadsanställd("Tina", 1 ,"Täby kommun")
anställd2=Timanställd("Jenny", 2, "Karlstads kommun", 100 )
anställd3=Månadsanställd("Noah", 3, "Stockholms kommun", 37 )
anställd1.beräkna_månadslön(40000, 3, 4, 5 )
anställd1.skattetable_nr()
anställd2.beräkna_månadslön(200,10)
anställd2.skattetable_nr()
anställd3.beräkna_månadslön(35000, 2, 1, 0 )
anställd3.skattetable_nr()












        