import csv
def läs_kommuneskattable_nr (filnamn):
    kommunskattable={}
    with open ( filnamn, mode ='r', encoding = "utf-8") as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)
        for rad in csv_reader:
            kommunskattable [rad[0]]= rad[1]
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
                'skatt':rad[5] #anta att alla använder Kolumn1
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
    def __init__(self, namn,kommunnamn):
        self.namn = namn
        self.kommunnamn = kommunnamn
    def beräkna_månadslön(self):
        pass
    def skattetable_nr(self):
        self.skattetable_nr = kommunskatttable[self.kommunnamn]
        skatteavdrag = hitta_avdragskatt(skattetable, self.skattetable_nr, self.månadslön)
        nettolön = self.månadslön-float(skatteavdrag)
        print ( f"{self.namn} använder skattetabell {self.skattetable_nr}, och enligt skattetabellen är skatteavdraget {skatteavdrag}. Nettolönen är {nettolön:.2f} SEK" )
    
class Månadsanställd(Anställd):
    def __init__(self, namn, kommunnamn, veckotimmar=40):
        self.veckotimmar = veckotimmar
        super().__init__(namn, kommunnamn)
    def beräkna_månadslön(self,månadslön, tjänstledigdgr, sjukdgr, semesterdgr):
        percent = self.veckotimmar/40
        if tjänstledigdgr > 5:
            tjänstledigavdrag = månadslön * 12 / 365 * tjänstledigdgr
        else:
            tjänstledigavdrag = månadslön / 21 * tjänstledigdgr
        sjukavdrag1_14 = månadslön * 12 / ( 52 * self.veckotimmar ) * sjukdgr
        sjuklön1_14 = 0.8 * månadslön * 12 / ( 52 * self.veckotimmar ) * sjukdgr
        Karensavdrag = sjuklön1_14 * 0.2
        semesterlöntillägg = månadslön * 0.008 * semesterdgr #anta att alla anställda har betald semesterdagar 
        if sjukdgr <= 14:
            self.månadslön = ( månadslön - tjänstledigavdrag - sjukavdrag1_14 + sjuklön1_14 - Karensavdrag + semesterlöntillägg ) * percent
        else:
            sjukavdrag15_90= månadslön * 12 / 365 * ( sjukdgr - 14)
            self.månadslön=( månadslön - tjänstledigavdrag - sjukavdrag1_14 - sjukavdrag15_90 + sjuklön1_14 - Karensavdrag + semesterlöntillägg ) * percent
        print (f"{self.namn} arbetar {self.veckotimmar} timmar per vecka, och månadslönen är {self.månadslön: .2f} SEK")

class Timanställd(Anställd):
    def __init__(self, namn, kommunnamn, timmar):
        self.timmar = timmar
        super().__init__( namn,kommunnamn )
    def beräkna_månadslön(self, timlön, sjuktimmar):
        sjuklön1_14 = timlön * 0.8 * sjuktimmar
        Karensavdrag = 0.2 * 0.8 * self.timmar * 12/52 * timlön #0.2*0.8*veckoarbetstid*timlön
        semersättning = (timlön * self.timmar + timlön * sjuktimmar ) * 0.13 #anta att timanställd får semesterersättning13% 
        self.månadslön = (timlön * self.timmar + sjuklön1_14-Karensavdrag + semersättning )
        print (f"{self.namn} är en timanställd. Hon arbetade {self.timmar} timmar den här månaden. Månadslön är {self.månadslön:.2f} SEK")
namn = input("ditt namn:")

while True:
    kommunnamn = input("din kommun:") +" kommun"
    try:
        if kommunskatttable[kommunnamn]:
            break
    except KeyError:
        print (f"Kommun {kommunnamn} hittades inte i skattetabellen.")

while True:
    try:
        svar = int(input (' månadsanställd mata in "1", timanställd mata in "2"'))
        if svar == 1:
            månadslön = int(input( "din månadslön?" ))
            veckotimmar = int(input( "hur många timmar arbetar du varje vecka? mata in number." ))
            tjänstledigdgr = int(input( "hur många dagar har du varit tjänstledig den här månad?" ))
            sjukdgr = float(input( "hur många dagar har du varit sjukfrånvaro den här månad?" ))
            semesterdgr = int(input( "hur många dagar har du varit på semester den här månad?"))
            anställd = Månadsanställd(namn, kommunnamn, veckotimmar)
            anställd.beräkna_månadslön(månadslön, tjänstledigdgr,sjukdgr,semesterdgr )
            anställd.skattetable_nr()
            break
        elif svar == 2:
            timlön = int(input ( "din timlön?" ))
            arbetstimmar = float(input ( "hur många timmar arbetar du den månader? mata in number" ))
            sjuktimmar = float(input ( "hur många timmar har du varit sjukfrånvaro den här månad?" ))
            anställd=Timanställd(namn, kommunnamn,arbetstimmar)
            anställd.beräkna_månadslön (timlön, sjuktimmar )
            anställd.skattetable_nr ()
            break
        else:
            print ("felagikt svar, försöker igen." )
    except ValueError:
        print ("Vänligen mata in ett giltigt nummer.")



