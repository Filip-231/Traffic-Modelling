'''
Filip Szmid 
Modelowanie ruchu miejskiego w Python model 2
Wiele samochodów przyjeżdzą w interwale 60 sekundowym z odpowiednia częstotliwoscia
W tym modelu zakładam, że wszystkie samochody przyjeżdżają w momencie startu każdego 60 sekundowego przedziału czasu.
Public Domain 
'''

from trafficLight import Sygnalizacjaswietlna
import numpy as np
import matplotlib.pyplot as plt

def wyliczsredniczas(numcars,limit,redTime):
  '''
  liczbasamochodu jest numerem samochodów, które nadjeżdzają. 
  Limit to maksymalna liczba samochodów które mogą przyjechać na sekunde pomnożone przez liczbę sekund zapalonego swiatła zielonego
  jesli nadjedzie mniej samochodów niż wynosi limit to wtedy żaden samochód nie czeka
  jesli nadjedzie wiecej samochodów niż wynosi limit, samochody ponad limit muszą poczekać przez okres zapalenia swiatla czerwonego+
  + sredni czas oczekiwania dla tych samochodow jesli swiatlo sie zmieni
  '''    
  if numcars <= limit:
    return numcars*0
  else:
    return ((numcars-limit)*redTime)+ wyliczsredniczas(numcars-limit,limit,redTime)

#3 typy zmiennych: czas zielonego, czestotliwość przyjazdu, ilość samochodów które mogą przejechać na sekundę
#Częstotliwość przyjazdu
rateVals = [x for x in range(2,100,2)]
#Ile samochodów może przejechać na sekundę
passVals = [0.1,0.15,0.2,0.25,0.5]
#Wartości proporcji światla zielonego
grVals = [0.1,0.12,0.15,0.2,0.3,0.4,0.5,0.6,0.7]


#Różna czestotliwość przyjazdu z różnym procentem swiatla zielonego
gyVals = []
#g=0.1
for g in grVals: #rozważam rozny stosunek światla zielonego do czerwonego
  tl = Sygnalizacjaswietlna(g*60,(1-g)*60)
  limit = tl.perSecond * tl.czaszielonego

  yVals = []

  for x in rateVals: # dla każdej czestotliwości przyjazdu samochodów
    waitTimes = []
    for _ in range(10):
      numCars = np.random.poisson(x) #przeprowadzam 20 symulacji dla kazdej losuje liczbę samochodów które nadjeżdżają
      if numCars == 0:
        waitTimes.append(0) #jeli nadjedzie 0 samochodow to czas czekania wyniesie 0
      else:
        waitTimes.append(wyliczsredniczas(numCars,limit,tl.czasczerwonego)/float(numCars))

    yVals.append(sum(waitTimes)/float(len(waitTimes)))

  gyVals.append(yVals) #wartości średniego czasu czekania zwiekszając czestotliwość przejazdu dla każdego stosunku zielonego światła do czerwonego


i=0
colors = ['b','r','g','c','m','k','y','m','c']
for y, c in zip(gyVals, colors):
  z = np.polyfit(rateVals, y, 1)
  p = np.poly1d(z)
  plt.plot(rateVals,y,'.',color=c)
  plt.plot(rateVals,p(rateVals),'-',color=c,label=("Stosunek= %s%%" % int(grVals[i]*100)))
  i+=1
plt.legend(fontsize=9, loc=0)
plt.xlabel('Czestotliwość przyjazdu samochodów na minutę', fontsize=12)
plt.ylabel('Średni czas czekania w sekundach', fontsize=12)
plt.suptitle("Porównanie częstotliwości przyjazdu samochodów \n z procentowym udziałem światła zielonego w cyklu sygnalizacji")
plt.xlim([0,100])
plt.show()
#plt.savefig("images/model_2A.png")
plt.clf()

##################################################################################################

# Inne natężenie przyjazdu wraz z liczbą samochodów, które przejeżdzają na sekundę przez skrzyżowanie
gyVals = []

for g in passVals:
  tl = Sygnalizacjaswietlna(30,30,g)
  limit = tl.perSecond * tl.czaszielonego

  yVals = []

  for x in rateVals:
    waitTimes = []
    for _ in range(20):
      numCars = np.random.poisson(x)
      if numCars == 0:
        waitTimes.append(0)
      else:
        waitTimes.append(wyliczsredniczas(numCars,limit,tl.czasczerwonego)/float(numCars))

    yVals.append(sum(waitTimes)/float(len(waitTimes)))

  gyVals.append(yVals)


i=0
#colors = ['b','r','g','c','m','k']
colors = ['m','c','y','k','r','b']
for y, c in zip(gyVals, colors):
  z = np.polyfit(rateVals, y, 1)
  p = np.poly1d(z)
  plt.plot(rateVals,y,'.',color=c)
  plt.plot(rateVals,p(rateVals),'-',color=c,label=("Częstotliwość przejazdu na sekundę = %s" % passVals[i]))
  i+=1
plt.legend(fontsize=9, loc=0)
plt.xlabel('Czestotliwość przyjazdu samochodów na minutę', fontsize=12)
plt.ylabel('Średni czas oczekiwania w sekundach', fontsize=12)
#plt.suptitle("Porównanie częstotliwosci przyjazdu z ruchem miejskim")
plt.xlim([0,100])
plt.show()
#plt.savefig("images/model_2B.png")




