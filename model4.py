'''
Filip Szmid
Symulacja minuta po minucie dla skrzyżowania drogowego model 4 w języku Python.
Ważne założenia:
Ilość samochodow ktore moga przejechać przez skrzyzowanie na zielonym światłe maleje wraz ze
wzrostem ruchu drogowego
ilość przyjechanych samochodow zmienia się w czasie
prawdopodobieństwo ze skrzyżowanie zostanie zablokowane również zmienia sie w okresie sygnalizacji
wraz ze wzrostem ilość samochodow, ktore przyjezdzaja
 Jeśli samochod zablokuje skrzyzowanie, czas, przez który zostanie zablokowane moze się zmienic
 czyli nie blokuje się zawsze na ten sam czas (do końca cyklu jak w poprzednich modelach)

Wartości wejściowe 
 proporcja czasu, w którym jest zapalone zielone lub czerwone światlo (na minute)
 ilość samochodów, ktore nadjezdzaja
liczba samochodów ktore moga przejechac przez skrzyżowanie na sekunde
 prawdopodobieństwo ze skrzyzowanie jest zablokowane, kiedy zapalone jest zielone światło
 czas na który skrzyzowanie jest zablokowane podczas zielonego światła

Pseudokod:
wiele samochodów może przyjechać i dołączyć do kolejki samochodów
dla takiego okresu wylicz, ile samochodów może przejechać
oblicz nową kolejkę
oblicz średni czas oczekiwania dla tego okresu
Public Domain

'''
from trafficLight import Sygnalizacjaswietlna
from car import Samochod
import numpy as np
import matplotlib.pyplot as plt
import statistics

#proporcja zielonego światla
grProp = 0.5
grTime = grProp*60
rdTime = 60-grTime

#czestość przyjazdu samochodów dla niskiego, średniego oraz wysokiego ruchu
arriveRates = {'L':8, 'M':12, 'H':20}
#arriveRates = {'L':10, 'M':14, 'H':25}

#liczba samochodow, które mogą przejechać dla niskiego, średniego oraz wysokiego ruchu
passRates = {'L':1, 'M':0.9*1, 'H':0.9*0.8*1}
#passRates = {'L':1, 'M':0.5*1, 'H':0.2*1}


#prawdopodobieństwo, że skrzyżowanie zostanie zablokowane dla niskiego, średniego oraz wysokiego ruchu
#blockingProb = {'L':0.05, 'M':0.2, 'H':0.45}
blockingProb = {'L':0.07, 'M':0.3, 'H':0.5}

# % czasu kiedy skrzyżowanie jest zablokowane dla niskiego, średniego oraz wysokiego ruchu
#bloockingTime = {'L':0.05, 'M':0.2, 'H':0.5}
bloockingTime = {'L':0.07, 'M':0.3, 'H':0.5}


#drugi zestaw danych
arriveRates = {'L':10, 'M':14, 'H':25}
passRates = {'L':1, 'M':0.8*1, 'H':0.6*1}
blockingProb = {'L':0.05, 'M':0.2, 'H':0.45}
bloockingTime = {'L':0.07, 'M':0.3, 'H':0.4}



def calcPassTime(number, normalGreenTime, actualGreenTime):
  '''
  wyliczenie czasu potrzebnego do przejazdu w ciągu okresu dla samochodów którym uda sie przejechać.
  '''
  allWaitFor = normalGreenTime - actualGreenTime #czas, który każdy z samochodów musi czekać
  if number > 0:
    timeperCar = actualGreenTime/float(number)#wyliczenie czasu średniego dla każdego samochodu
  else:
    timeperCar = 0
  times = []
  for i in range(1,number+1,1):
    times.append(timeperCar*i+allWaitFor)
  return times

def runTraffic(queue, passedCars, tl, trafficType):
  '''
  Funkcja odpowiadająca za rozpoczęcie ruchu na skrzyżowaniu.
  '''
  p = np.random.uniform() #losujemy z rozkladu jednostajnego czy skrzyżowanie ulegnie blokadzie
  if p < blockingProb[trafficType]:
    czaszielonego = (tl.czaszielonego - bloockingTime[trafficType]*tl.czaszielonego) #jeśli ulega blokadzie to od czasu zielonego odejmujemy czaszablokowania * czas zielonego
  else:
    czaszielonego = tl.czaszielonego #jeśli nie to nic sie nie dzieje

  passableCars = int(czaszielonego*tl.perSecond) #ile samochodów może przejechać przez skrzyżowanie
  
  if len(queue) <= passableCars: #jeśli dlugość kolejki jest mniejsza niz liczba samochodów które mogą przejechać
    top = len(queue) 
  else:
    top = passableCars

  totalTime = 0
  times = calcPassTime(top,tl.czaszielonego,czaszielonego) #wlicz dla tych co moga przejechac 
  for j in range(top):
    samochod = queue[j]
    samochod.aktualizujczasczekania(times[j])
    totalTime += samochod.czasczekania
    passedCars.append(samochod)

  avg = 0
  if top > 0:
    avg = totalTime/float(top)

  for j in range(top,len(queue),1):
    samochod = queue[j] #podajemy dla, których obiektów mamy zaktualiozwać czas oczekwiania
    samochod.aktualizujczasczekania(tl.czaslaczny)
    

  del queue[0:passableCars] #usuń z kolejki te samochody co przejechały
  return queue, passedCars, top, avg

yValsA = []
yValsB = []
yValsC = []
yValsD = []

for z in range(1000):

  tl = Sygnalizacjaswietlna(grTime,rdTime,passRates['L'])
  carQueue = []
  passedCars = []

  numWaitingCars = []
  numPassedCars = []
  avgWaitTime = []

  for i in range(5):
    for _ in range(np.random.poisson(arriveRates['L'])): #dla rożnych wartości częstości przyjazdu losujemy z rozkładu Poissona ile samochodów ma nadjechać
      carQueue.append(Samochod()) # dodajemy do kolejki obiekty

    carQueue, passedCars, numCars, avgTime = runTraffic(carQueue,passedCars,tl,'L')
    numWaitingCars.append(len(carQueue))
    numPassedCars.append(numCars)
    avgWaitTime.append(avgTime)

# dla różnej liczby samochodów, które mogą przejechać dla niskiego średniego i wysokiego natężenia
  for i in range(5,20,1):
    tl.aktualizujswiatlo(40,20,passRates['H'])
    for _ in range(np.random.poisson(arriveRates['H'])):
      carQueue.append(Samochod())

    carQueue, passedCars, numCars, avgTime = runTraffic(carQueue,passedCars,tl,'H')
    numWaitingCars.append(len(carQueue))
    numPassedCars.append(numCars)
    avgWaitTime.append(avgTime)

  for i in range(20,40,1):
    tl.aktualizujswiatlo(30,30,passRates['M'])
    for _ in range(np.random.poisson(arriveRates['M'])):
      carQueue.append(Samochod())

    carQueue, passedCars, numCars, avgTime = runTraffic(carQueue,passedCars,tl,'M')
    numWaitingCars.append(len(carQueue))
    numPassedCars.append(numCars)
    avgWaitTime.append(avgTime)

  for i in range(40,55,1):
    tl.aktualizujswiatlo(40,20,passRates['H'])
    for _ in range(np.random.poisson(arriveRates['H'])):
      carQueue.append(Samochod())

    carQueue, passedCars, numCars, avgTime = runTraffic(carQueue,passedCars,tl,'H')
    numWaitingCars.append(len(carQueue))
    numPassedCars.append(numCars)
    avgWaitTime.append(avgTime)

  for i in range(55,60,1):
    tl.aktualizujswiatlo(30,30,passRates['L'])
    for _ in range(np.random.poisson(arriveRates['L'])):
      carQueue.append(Samochod())

    carQueue, passedCars, numCars, avgTime = runTraffic(carQueue,passedCars,tl,'L')
    numWaitingCars.append(len(carQueue))
    numPassedCars.append(numCars)
    avgWaitTime.append(avgTime)

  yValsA.append(numWaitingCars)
  yValsB.append(numPassedCars)
  yValsC.append(avgWaitTime)
  yValsD.append([samochod.czasczekania for samochod in passedCars])

x = [i+1 for i in range(60)]


#plt.figure(figsize=((10,8)))
plt.plot(x,[sum(e)/len(e) for e in zip(*yValsA)],'-y.',label="Długość kolejki")
plt.plot(x,[sum(e)/len(e) for e in zip(*yValsB)],'-r.',label="Liczba samochodów, które przejechały")
plt.legend(fontsize=10,loc=0)
plt.xlabel('Minuta', fontsize=12)
plt.ylabel('Liczba samochodów', fontsize=12)
plt.suptitle("Liczba czekających i przejeżdżających samochodów w danym przedziale czasu")
#plt.savefig("images/model4_numCars.png")
#plt.clf()
plt.show()


plt.plot(x,[sum(e)/len(e) for e in zip(*yValsC)],'-y.',label="Średnia ze średnich czasów oczekiwania dla 1000 symulacji")
plt.plot(x,[max(e) for e in zip(*yValsC)],'-r.',label="Maxymalna ze średnich czasów oczekiwania dla 1000 symulacji")
plt.plot(x,[statistics.median(e) for e in zip(*yValsC)],'-b.',label="Mediana ze średnich czasów oczekiwania dla 1000 symulacji")
plt.legend(fontsize=10,loc=0)
plt.xlabel('Minuta', fontsize=12)
plt.ylabel('Liczba sekund', fontsize=12)
plt.suptitle("Średni czas oczekiwania w danym przedziale")
#plt.savefig("images/model4_avgTime.png")
#plt.clf()
plt.show()



allWaitTimes = []
for r in yValsD:
  for t in r:
    allWaitTimes.append(t)

plt.hist(allWaitTimes,bins=40,normed=True,alpha=0.5,color='b')
plt.suptitle("Rozkład czasów oczekiwania samochodów")
plt.xlabel('Czas oczekiwania samochodu (sekundy)', fontsize=12)
plt.ylabel('%', fontsize=12)
#plt.savefig("images/model4_hist.png")
#plt.clf()
plt.show()

plt.hist(allWaitTimes,bins=40,normed=True,alpha=0.5,color='y',cumulative=True)
plt.suptitle("Rozkład czasów oczekiwania samochodów")
plt.xlabel('Czas oczekiwania samochodu (sekundy)', fontsize=12)
plt.ylabel('Skumulowany %', fontsize=12)
#plt.savefig("images/model4_hist_cum.png")



