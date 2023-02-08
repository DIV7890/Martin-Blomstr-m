import random
import gtts
from gtts import gTTS
import os


filename = "glosor.txt"
lista = []

with open(filename, "rb") as file:
    lines = file.readlines()

for line in lines:
    line_decoded = line.decode("utf-8")
    words = line_decoded.split()
    for word in words:
            lista.append(word)

print(lista)
antal_rätta_gissningar = 1
r = random.randint(0,12-antal_rätta_gissningar)
rätt_svar = lista[r]
antal_bokstäver = 1
numbers = list(range(1, 13))
antal_fel = 0
höra_igen = False
def HöraIgen(a):
    if a == "y":
        return True
    elif a == "n":
        return False
    else:
        print("Du har valt att svara med ett tecken som inte kan hanteras... ")
        a = input("Vill du höra glosan igen? (svara med y/n) ")
        HöraIgen(a)
while len(numbers) >= 1:
    print("\n")
    selected = random.choice(numbers)
    tts = gTTS(lista[selected-1], lang='sv')
    tts.save('glosor.mp3')
    print("Output:", selected)
    os.system("glosor.mp3")
    höra_igen = HöraIgen(input("Vill du höra glosan igen? (svara med y/n) "))
    while höra_igen == True:
        os.system("glosor.mp3")
        höra_igen = HöraIgen(input("Vill du höra glosan igen? (svara med y/n) "))
    svar = input("Skriv: ")
    if str(svar) == lista[selected-1]:
        numbers.remove(selected)
    else:
        antal_fel += 1
        print("Rätt svar var " + lista[selected-1])
print("\n")
if antal_fel == 0:
    print("Du fick alla rätt!!!")
else:
    print("Du fick " + str(antal_fel) + " fel.")