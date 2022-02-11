from datetime import datetime

class ExamException(Exception):
  pass
  
class CSVTimeSeriesFile:
  def __init__(self, name):
    self.name = "data.csv"
    self.time_series = []

  def get_data(self):
    try:
      my_file= open(self.name, 'r')
    except IOError:
      raise ExamException('Errore, file non disponibile')
    lines = my_file.readlines()

    lastReadDate = "1900-01"

    for line in lines:
      element = line.split(",")
      
      try:
        dateObj= datetime.strptime(element[0],"%Y-%m")
      except ValueError:
        continue
      
      if(element[0]<lastReadDate):
        raise ExamException('Errore, date non ordinate')
      
      if(element[0]==lastReadDate):
        raise ExamException('Errore, date duplicate')

      lastReadDate = element[0]
       
      self.time_series.append(element)

    my_file.close()
    return self.time_series 


def compute_avg_monthly_difference(time_series, first_year, last_year):
  noYears = int(last_year) - int(first_year) + 1;
  monthlySum = 0
  yearsData = []
  years = []
  currentYear = first_year
  monthlyAvg = []

  for element in time_series:
    readYear = element[0].split("-")[0]
    readMonth = element[0].split("-")[1]
    readValue = element[1]
    if readYear >= first_year and readYear <= last_year:
      if readYear != currentYear:
        currentYear = readYear
        years.append(yearsData)
        yearsData = []
        
    yearsData.append(int(readValue))
  years.append(yearsData)

  for m in range(12):
    monthlySum = 0
    noMeasures = 12
    for y in range(noYears - 1):
      monthlySum += int(years[y+1][m]) - int(years[y][m])
    monthlyAvg.append(monthlySum / (noYears - 1))
  
  return monthlyAvg
 
time_series_file = CSVTimeSeriesFile(name='data.csv')

time_series = time_series_file.get_data()

compute_avg_monthly_difference(time_series,"1949","1951")
