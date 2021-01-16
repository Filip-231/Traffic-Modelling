class Sygnalizacjaswietlna(object):
  '''
  Obiekt sygnalizacji świetlnej wykorzystywany w modelu 4, w celu modelowania ruchu na skrzyżowaniu
  Posiada takie atrybuty jak czas światła zielonego, czas światła czerwonego a także funkcje jak zmień stan lub aktualizuj światło
  '''
  def __init__(self, czaszielonego, czasczerwonego, perSecond=0.1, czaslaczny=60, stan=''):
    self.czaszielonego = czaszielonego
    self.czasczerwonego = czasczerwonego
    self.czaslaczny = czaszielonego+czasczerwonego
    self.stan = 'Green'
    self.perSecond = perSecond

  def czaszielonego(self):
    return self.greenTime

  def czasczerwonego(self):
    return self.redTime

  def czaslaczny(self):
    return self.totalTime

  def czaslaczny(self):
    return self.perSecond

  def aktualizujswiatlo(self,czaszielonego=None,czasczerwonego=None,perSecond=None):
    if czaszielonego:
      self.czaszielonego = czaszielonego
    if czasczerwonego:
      self.czasczerwonego = czasczerwonego
    if perSecond:
      self.perSecond = perSecond

  def zmienstan(self):
    if self.stan == 'Czerwone':
      self.stan = 'Zielone'
    else:
      self.stan = 'Czerwone'

  def __str__(self):
    return "Zielone światło stanowi  %s, Czerwone światło stanowi %s, Częstotliwość przejazdu to %s" % (self.czaszielonego, self.czasczerwonego, self.perSecond)

  