import csv
from collections import Counter


class PassengerCounter():
    def __init__(self):
        gendercsv = '/home/pi/Desktop/GenderAge/gender.csv'
        agecsv = '/home/pi/Desktop/GenderAge/age.csv'
        self.male_counts = 0
        self.female_counts = 0
        self.age_0_2_counts = 0
        self.age_4_6_counts = 0
        self.age_8_12_counts = 0
        self.age_15_20_counts = 0
        self.age_25_32_counts = 0
        self.age_38_43_counts = 0
        self.age_48_53_counts = 0
        self.age_60_100_counts = 0

        with open (gendercsv) as g:
            reader = csv.reader(g, delimiter = ',', quotechar = '|')
            next(g)

            for row in reader:
                #check if there is any blank row in the gender.csv
                if row == '':
                    continue
                if row[1] == 'Male':
                    self.male_counts+=1
                if row[1] == 'Female':
                    self.female_counts+=1
        
        with open (agecsv) as a:
            reader = csv.reader(a, delimiter = ',', quotechar = '|')
            next(a)

            for row in reader:
                #check if there is any blank row in the age.csv
                if row == '':
                    continue
                if row[1] == '0-2':
                    self.age_0_2_counts+=1
                if row[1] == '4-6':
                    self.age_4_6_counts+=1
                if row[1] == '8-12':
                    self.age_8_12_counts+=1
                if row[1] == '15-20':
                    self.age_15_20_counts+=1
                if row[1] == '25-32':
                    self.age_25_32_counts+=1
                if row[1] == '38-43':
                    self.age_38_43_counts+=1
                if row[1] == '48-53':
                    self.age_48_53_counts+=1
                if row[1] == '60-100':
                    self.age_60_100_counts+=1

    def Female(self):
        return self.female_counts
    
    def Male(self):
        return self.male_counts

    def age_0_2(self):
        return self.age_0_2_counts

    def age_4_6(self):
        return self.age_4_6_counts

    def age_8_12(self):
        return self.age_8_12_counts

    def age_15_20(self):
        return self.age_15_20_counts

    def age_25_32(self):
        return self.age_25_32_counts

    def age_38_43(self):
        return self.age_38_43_counts

    def age_48_53(self):
        return self.age_48_53_counts

    def age_60_100(self):
        return self.age_60_100_counts

