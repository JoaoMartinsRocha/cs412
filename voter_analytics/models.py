from django.db import models
# from .models import Result

from urllib.parse import urlencode


# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # identification
    last_name = models.TextField()
    first_name = models.TextField()
    
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    
    dob = models.DateField(auto_now=False)
    dor = models.DateField(auto_now=False)

  
    party_affiliation = models.CharField(max_length=3)
    

    precinct_num = models.TextField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary  = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
   
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.party_affiliation}'
    
    # def get_runners_passed(self):
    #     '''Return the number of runners passed by this runner.'''
    #     started_first = Result.objects.filter(start_time_of_day__lt=self.start_time_of_day)
    #     passed = started_first.filter(finish_time_of_day__gt=self.finish_time_of_day)

    #     return len(passed)
        
    # def get_runners_passed_by(self):
    #     '''Return the number of runners who passed this runner.'''
    #     started_later = Result.objects.filter(start_time_of_day__gt=self.start_time_of_day)
    #     passed_by = started_later.filter(finish_time_of_day__lt=self.finish_time_of_day)

    #     return len(passed_by)
    def full_address(self):
        parts = [str(self.street_number), self.street_name]
        if self.apartment_number:
            parts.append(f"Apt {self.apartment_number}")
        parts.append(self.zip_code)
        return " ".join(parts)

    def google_maps_link(self):
        query = urlencode({"query": self.full_address()})
        return f"https://www.google.com/maps/search/?api=1&{query}"

    
    def load_data():

        '''Function to load data records from CSV file into Django model instances.'''

        Voter.objects.all().delete()

        filename = '/Users/jprocha/Desktop/django/newton_voters.csv'
        f = open(filename)
        f.readline() # discard headers

        for line in f:
            # line = f.readline().strip()
            
            fields = line.split(',')
            # show which value in each field

            # print(f'fields={fields}')
            
            # for i in range(len(fields)):
            
            #     print(f'fields[{i}] = {fields[i]}')

            try:
                result = Voter(last_name=fields[1],
                    first_name=fields[2],
                    street_number=fields[3],
                    street_name = fields[4],
                    apartment_number = fields[5],
                    zip_code = fields[6],
                    
                    dob = fields[7],
                    dor = fields[8],

                    party_affiliation = fields[9],
                    precinct_num = fields[10],
                    v20state = string_to_bool(fields[11]), 
                    v21town = string_to_bool(fields[12]), 
                    v21primary = string_to_bool(fields[13]),
                    v22general= string_to_bool(fields[14]),
                    v23town = string_to_bool(fields[15]), 
                    voter_score = fields[16],
                )

            
                result.save() # commit to database
                # print(f'Created result: {result}')
            except Exception as e:
                print(f"Skipped: {e}")

        print(f'Done. Created {len(Voter.objects.all())} Results.')


def string_to_bool(s):
    s = s.lower()
    if s == "true":
        return True
    elif s == "false":
        return False
    else:
        raise ValueError("Invalid boolean string")
