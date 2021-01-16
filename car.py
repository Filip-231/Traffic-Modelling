import numpy as np


class Samochod(object):  
  '''
  Obiekt samochód odzwierciedla prawdziwy samochód, 
  ma on określone takie parametry jak czas przyjazdu, czas przejazdu.
  Jest wykorzystywany w modelu 4.
  '''

  def __init__(self, start=0, end=60, czasprzyjazdu=0, czasczekania=-1):
    self.czasprzyjazdu = np.random.randint(start,end)
    self.czasczekania=-1

  def czasprzyjazdu(self):
    return self.czasprzyjazdu

  def czasprzyjazdu(self):
    return self.czasczekania

  def __str__(self):
    return "Samochód przyjeżdza w:" % (self.czasprzyjazdu)
   
  def aktualizujczasczekania(self,A):
     self.czasczekania=A+self.czasczekania
     return self.czasczekania
