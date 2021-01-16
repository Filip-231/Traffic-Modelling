'''
Filip Szmid 
Modelowanie ruchu miejskiego w Python model 1
Model nr. 1 skrzyżowania w ruchu drogowym
Prosty model w którym zakładam że swiatlo zielone trwa x sekund a czerwone 60-x sekund.
Rozpatruje przyjazdy samochodow w ciagu minutowych odstepów i obliczam ich sredni czas oczekiwania.
Public Domain 
'''

from trafficLight import Sygnalizacjaswietlna
import random
import numpy as np
import matplotlib.pyplot as plt

#ustawienie srodowiska plików w którym pracujemy
import os
print("Current Working Directory " , os.getcwd())
os.chdir("D:/Dokumenty/Nauka/Magisterka PG/Praca MGR/Program/Program")
# some_file.py
#D:\Dokumenty\Nauka\Magisterka PG\Praca MGR\Program\Program

def  Liczczasczekania(tl,car):
  '''
  Załóźmy, że swiatło jest koloru zielonego, jesli samochód przyjeżdża i swiatło nadal jest zielone, to nie czeka ani chwili.
  W przeciwnym wypadku musi poczekać czas zapalonego swiatła czerwonego przed tym kiedy będzie mógł przejechać.

  '''
  if car <= tl.czaszielonego:
    return 0
  else:
      
      return tl.czaslaczny - car

globalnesrednie = []

for j in range(1,100,1):
  #Sprawdzam różne proporcje światla zielonego do czerwonego
  gT = j*60/100
  tl = Sygnalizacjaswietlna(gT,60-gT)
  srednie = []
  
  for x in range(50):
      #powtarzam 20 razy symulacje w której przyjeżdża 20 samochodów
    czasczekania = []
    for _ in range(50):
      #czas przyjazdu samochodu jest wylosowany z przedzialu 0-60
      #car = random.randint(0,60)
      car=int(np.random.normal(0, 0.1, 1)*100+30)
      w =  Liczczasczekania(tl,car) #podaję czas czekania 
      czasczekania.append(w)
      
    srednie.append(sum(czasczekania)/float(len(czasczekania))) # suma z czasu czekania każdego samochodu podzielona przez ilosc czyli 20
    
  globalnesrednie.append(sum(srednie)/float(len(srednie))) # średnie z kazdych 20 symulacji
  

x = [y for y in range(1,100,1)]

plt.scatter(x,globalnesrednie,c='r',marker='.')
plt.suptitle("Średni czas czekania dla pojedyńczego samochodu")
plt.xlabel("Procentowy przedział okresu, w którym światlo jest zielone", fontsize=13)
plt.ylabel('Średni czas czekania w sekundach', fontsize=13)
plt.xlim([0,100])



#plt.savefig("blablablabla.pdf")
    

















