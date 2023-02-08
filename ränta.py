summa = 0
index = 0
varje_manad = 400
ranta = 1.07
while index < 12*40:
    summa += 400
    if index % 12 == 0:
        summa = summa * 1.07
    index += 1
    print(summa)
print(summa)
print(400 *(12*40))