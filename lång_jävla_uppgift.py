#Martin Blomström

#Uppgift 1.1

#Ett: String
#a: String
#4 : Integer
#3.6 : Float
#True : Boolean
#'True' : String

#Uppgift 1.2

#variabel1 = 'a, b, c': String
#a = 10 : Integer
#alpha = True : Boolean
#variabel2 = a : Integer
#variabel3 = 1 : Integer
#variabel4 = b :
#variablel5 = alpha : Boolean

#variabel1 = 'a, b, c'
#a = 10
#alpha = True
#variabel2 = a
#variabel3 = 1
#variabel4 = "b" # Åtgärd (+ "")
#variable5 = alpha # Åtgärd
#print(variabel1)
#print(variabel2)
#print(variabel3)
#print(variabel4)
#print(variable5) # Åtgärd

# Uppgift 1.3

#print(1/3) # Printar resultatet av 1/3 d.vs 0.3333...
#print('1/3') # Printar 1/3 som en string
#a = 1/3
#print(a) # Samma som första
#print('a') # Printar "a" som en string

# Uppgift 2.1
# Funktionerna tar in integers eller floats som inputs och ger integers eller floats som outputs
# Funktionen tar in två värden, multiplicerar de och får därmed en "area"
#def beräknaArea(sida1, sida2):
   #area = sida1*sida2
   #return area
#beräknaArea(2, 4)
#def alternativtBeräknaArea(sida1, sida2):
   #print(sida1*sida2)
#alternativtBeräknaArea(3, 15)
#def adderaSiffror(siffra1, siffra2):
   #summa = siffra1+siffra2
   #return summa
#def funktion(x, y):
   #a = x*y+y
   #return a
#def funktion(x, y):
   #print(x+y)
#import numpy as np #låt denna vara, återkommer till import
#def funktion(a, b):
   #c = np.sqrt(a*a + b*b)
   #return c

# Uppgift 2.2
#def beräknaArea(sida1, sida2):
   #area = sida1*sida2
   #return area
#beräknaArea(2, 4)
#def alternativtBeräknaArea(sida1, sida2):
   #print(sida1*sida2)
#alternativtBeräknaArea(3, 15)
#def adderaSiffror(siffra1, siffra2):
   #summa = siffra1+siffra2
   #return summa
#def x_ggr_y_pluss_y(x, y):
   #a = x*y+y
   #return a
#def x_pluss_y(x, y):
  #print(x+y)

# Uppgift 2.3
#x = float(input("Välj ett tal")) # Tar in ett tal (antingen heltal eller decimaltal)
#y = float(input("Välj ett till tal")) # Tar in ett tal (antingen heltal eller decimaltal)
#def multiplikation(x, y) # Tar in två värden till funktionen
   #print(x*y) # Multiplicerar de två värderna
#multiplikation(x, y) # Kallar på funktionen och får resultatet av x*y utskrivet

#Uppgift 3.1 a)
#a = "a"
#b = "b"
#print(a+b) # Resultatet blir att de två strängarna slås ihop

#Uppgift 3.1 b)
#x = float(input("Välj ett tal "))
#y = float(input("Välj ett till tal "))
#z = float(input("Välj ett till tal "))
#def volym(x,y,z):
   #return(x*y*z)

#Uppgift 3.2
ans = 0

#def minus(a,b):
   #print("\n")
   #return("Svaret är " + str(a - b))

#def pluss(a,b):
   #print("\n")
   #return ("Svaret är " + str(a + b))

#def gånger(a,b):
   #print("\n")
   #return ("Svaret är " + str(a * b))

#def delat(a,b):
   #print("\n")
   #if b == 0:
       #return ("Du försöker dela på 0, vilket inte går... ")

   #else:
    #return ("Svaret är " + str(a / b))

#färdig = "n"
#while färdig == "n":
   #print("\n")
   #y = str(input("Välj term för opperation. Skriv valfritt tal: "))
   #x = str(input("Välj opperatör genom att skriva (- ; + ; * ; /): "))
   #z = str(input("Välj andra term för opperation. Skriv valfritt tal: "))

   #y = float(y)

   #z = float(z)

   #if x == "-":
       #print(minus(y,z))
   #if x == "+":
       #print(pluss(y,z))

   #if x == "*":
       #print(gånger(y,z))

   #if x == "/":
       #print(delat(y,z))
   #print("\n")

   #färdig = str(input("Är du färdig med din uträkning? Om ja, skriv \"y\" annars skirv \"n\" "))

# Uppgift 3.3
#mellanslag = " "
#understräck = "_"
#print(10*mellanslag + "O" + 6*mellanslag + "O")
#print(11*mellanslag + 6*understräck)

# Uppgift 3.4
#a = str(input("Skriv någonting: "))
#if len(a) > 7:
   #print("Det du vlade att skriva är för långt!")
#FörbjudnaTecken1 = "å"
#FörbjudnaTecken2 = "ä"
#FörbjudnaTecken3 = "ö"
#if FörbjudnaTecken1 or FörbjudnaTecken2 or FörbjudnaTecken3 in a:
   #print("Du valde att använda dig av förbjudna tecken!")

# Uppgift 4.1
#a = str(input("Skriv någonting: "))
#b = 0
#AntalNummer = 0
#AntalBokstäver = 0
#while b < len(a):
   #c = a[b]
   #if c.isdigit():
       #AntalNummer += 1
   #if c.isalpha():
       #AntalBokstäver += 1
   #b += 1
#print("Antal nummer var " + str(AntalNummer))
#print("Antal bokstäver var " + str(AntalBokstäver))

# Uppgift 4.2
#start1 = 0
#start2 = 1
#NästaTal = 0
#index = int(input("Välj för hur många index det ska hålla på: "))
#a = 0
#print("Index = 0" +"\t tal = " + str(start1))
#print("Index = 0" +"\t tal = " + str(start2))
#while a < index-2:
   #NästaTal = start1 + start2
   #start1 = start2
   #start2 = NästaTal
   #a += 1
   #print("Index = " + str(a+2) +"\t tal = " +str(NästaTal))

# Uppgift 5

# -

# Uppgift 6
#a = float(input("Hur lång sträcka färdades? (I meter) "))
#b = float(input("Hur lång tid passerade? (I sekunder) "))
#def MeterPerSekund(a, b):
   #return a / b
#print("Genomsnittshastigheten var " + str(MeterPerSekund(a, b)) + " m/s (meter per sekund)")

#def Area(a,b):
   #return(a*b)
#def Volym(a,b):
   #return(a**2*b)

#a = float(input("Hur snabbt färdades du under sträckan? (I genomsnitt och i enheten m/s (meter per sekund)) "))
#b = float(input("Hur lång tid tog det att färdas sträckan? (I sekunder) "))
#def Sträcka(a,b):
#    return(a*b)

#x1 = float(input("välj värde för den första x-kordinaten: "))
#y1 = float(input("välj värde för den första y-kordinaten: "))
#x2 = float(input("välj värde för den andra x-kordinaten: "))
#y2 = float(input("välj värde för den andra y-kordinaten: "))

#if x1 - x2 == 0:
   #print("De valda kordinaterna tyder på att din linje är lodrät och är deffinerad som x = " + str(x1))
#else:
   #k = (y1 - y2) / (x1 - x2)
   #print("K-värdet = " + str(k))

# resten av Uppgift 6

# -

# Uppgift 7
#elever = ['Axel', 'Johan', 'Johanna', 'Oscar', 'Bill']
#nummer = [1, 3, 4, 6, 2, 5]

#elever.sort()
#nummer.sort()
#print(elever)
#print(nummer)

#a = 0
#while a < len(elever):
   #print(elever[a])
   #a += 1

#a = 0
#while a < len(nummer):
   #print(nummer[a])
   #a += 1
#elever.append("a")
#elever.append("b")
#print(elever) # Man behöver sortera om listan

#elever2 = elever

#basgrupp1 = [ ]
#basgrupp2 = [ ]
#a = 0
#while a < 3:
   #basgrupp1.append(elever[a])
   #a += 1
#print(basgrupp1)
#a = 3
#while a < len(elever):
   #basgrupp2.append(elever[a])
   #a += 1
#print(basgrupp2)

#nummer.reverse()
#print(nummer)

#elever2 = ('Axel', 'Johan', 'Johanna', 'Oscar', 'Bill')
#elever2.append("a")
#print(elever2) # Traceback (most recent call last):
 #File "C:\Users\marti\PycharmProjects\pythonProject\temporär.py", line 235, in <module>
   #elever2.append("a")
#AttributeError: 'tuple' object has no attribute 'append'

#elever3 = ['Axel', 'Johan', 'Johanna', 'Oscar', 'Bill'] # Skillnaden är att en tupple inte kan ändras

# Uppgift 8

# -

# Uppgift 9

# -