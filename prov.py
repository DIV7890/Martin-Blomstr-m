# Martin Blomström
# Uppgift 1
a = float(input("Välj det första talet i listan ")) #input för de tre olika talen
b = float(input("Välj det andra talet i listan "))
c = float(input("Välj det tredje talet i listan "))

# Uppgift 2
list1 = [a, b ,c] # Skapar en lista innehållande de tre talen.
print(list1) # Printar ut de tre talen

# Uppgift 3 samt Uppgift 4
def jamfora(x, y, z):
    if x <= y and x <= z: # Jag kollar om x är det minsta talet, om inte går jag vidare till att kolla om y eller z är minst. Annars kollar jag vilken av y och z som är minst.
        if y <= z:
            return [z, y, x]
        else:
            return [y, z, x]
    elif y <= x and y <= z: # Jag kollar om y är det minsta talet, om inte går jag vidare till att kolla om x eller z är minst. Annars kollar jag vilken av y och z som är minst.

        if x <= z:
            return [z, x, y]
        else:
            return [x, z, y]
    elif x <= y: # här vet jag att z måste vara det minsta talet. Alltså jämför jag om x eller y är minst.
        return [y, x, z]
    else: return [x, y, z] # I och med att allt ovanstående är falskt så vet jag att z måste vara minst förljande av y och sedan x.
print("Storleksordnat " + str(jamfora(a, b, c)))
print(a, b, c)

# Uppgift 5
list3 = [list1 + jamfora(a, b, c)]

# Uppgift 6
for x in list3:
    print(x)