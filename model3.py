'''
Filip Szmid
Modelowanie ruchu miejskiego w Python model 3
Zakladamy że swiatlo jest na skrzyzowaniu ktore z prawdopodobientwem p zostanie zablokowane.
czyli nawet jak bedzie zapalone swiatlo zielone to samochody nie beda mogly przejechać.
zacznijmy od prawdopodobieństwa zablokowania wynąszącego 10%.
W tym modelu zakładam że wszystkie samochody przyjeżdzają w momencie startu każdego przedziału czasu.
Public Domain
'''
from trafficLight import Sygnalizacjaswietlna
import numpy as np
import matplotlib.pyplot as plt

#Definiuje dwie osobne funkcje, jedna dla rozblokowanego skrzyżowania
#Druga w przypadku gdy skrzyżowanie będzie zablokowane

def wyliczczysteczekanie(numcars,tl,prob):
  '''
  Przejazd przez nie zablokowane skrzyzowanie.
  '''
  limit = tl.perSecond * tl.czaszielonego #limit samochodów ktore mogą przejechać wynosi ilość samochodów które przejadą na sekundę * ilość czasu swiatla zielonego
  if numcars <= limit:
    return numcars*0 #jeśli samochodów jest mniej niż jakis ustalony limit to wszystkie przejeżdżają
  else: # przejezdżają tylko te samochody które mieszczą sie w limicie
    t = ((numcars-limit)*tl.czasczerwonego) #nadwyzka samochodow ponad limit musi czekac czas czerwoengo
    p = np.random.uniform()
    if p <= prob:
      return t + wyliczzablokowaneczekanie(numcars-limit,tl,prob) # przypadek kiedy skrzyzowanie sie blokuje
    else:
      return  t + wyliczczysteczekanie(numcars-limit,tl,prob) # jeśli skrzyzwoanei jest rozblokowane


def wyliczzablokowaneczekanie(numcars,tl,prob):
  ''' 
  Przejazd przez zblokowane skrzyzowanie.
  Jeżeli skrzyżowanie ulegnie zablokowaniu, wszystkie samochody musza czekać pełne 60 sekund zamin będą miały kolejną szansę przejechać.
  '''
  limit = tl.perSecond * tl.czaszielonego
  #Wszystkie samochody muszą czekać pełen cykl= czaszielonego+ czas czerwonego
  t = numcars*(tl.czaszielonego+tl.czasczerwonego) #kazdy samochod musi czekac czas zielonego oraz czerwonego
  p = np.random.uniform()
  if p <= prob:
    return t+wyliczzablokowaneczekanie(numcars,tl,prob) # jeśli nadal jest zblokowane
  else:
    return t+wyliczczysteczekanie(numcars,tl,prob) # jeśli skrzyżowanie się rozblokuje

#Porównujemy czestotliowść przyjazdu z prawdopodobieństwem zablokowania
#Wartości częstotliwosci przyjazdu samochodów
rateVals = [x for x in range(2,40,1)]
#Prawdopodobieństwa zablokowania
pVals = [0,0.3,0.6,0.7,0.9]

for g in range(20,50,5): #ustalam dla różnych czasów światla zielonego 20, 30 ,40 dla kazdego osobny wykres
  gyVals = []
  for pr in pVals: #dla roznego prawdopodobieństwa zablokowania
    tl = Sygnalizacjaswietlna(g,60-g)

    yVals = []

    for x in rateVals: #dla różnej czestotliwości przyjazdu

      waitTimes = []
      for _ in range(100):
        numCars = np.random.poisson(x)
        if numCars == 0:
          waitTimes.append(0)
        else:
          p = np.random.uniform()
          if p <= pr:
            waitTimes.append(wyliczzablokowaneczekanie(numCars,tl,pr)/float(numCars))
          else:
            waitTimes.append(wyliczczysteczekanie(numCars,tl,pr)/float(numCars))

      yVals.append(sum(waitTimes)/float(len(waitTimes)))

    gyVals.append(yVals)

  i=0
  colors = ['g','m','b','r','c']
  for y, c in zip(gyVals, colors):
    z = np.polyfit(rateVals, y, 1)
    p = np.poly1d(z)
    plt.plot(rateVals,y,'.',color=c)
    plt.plot(rateVals,p(rateVals),'-',color=c,label=("p = %s" % pVals[i]))
    i+=1
  plt.legend(fontsize=9,loc=0)
  plt.xlabel('Częstotliwość przyjazdu samochodów na minutę', fontsize=12)
  plt.ylabel('Średni czas czekania w sekundach', fontsize=12)
  plt.suptitle("Średni czas czekania: Swiatło zielone: %s seconds" % g)
  plt.show()
  #plt.savefig("images/model_3_%s.png" % g)
  plt.clf()
  
  
  
  
  
  
  
  
  