import re

class Helper(object):
        
    def __init__(self):
        self.host = "IP_ADDRESS_OR_HOST_HERE"
        self.user = "USER_HERE"
        self.password = "PASSWORD_HERE"
        self.database = "DATABASE_HERE"
        self.sql = ''
        self.sql_no_hnumber = ''
        
    def sql_statment(self,row,et,lat,long,update_flag):

        row = self.validate_field_and_remove_spec_chars(row)
        print(row)
        if (str(row).find('house_number')>0):

            house_number = ''
            house_number = row['address']['house_number']

            if (update_flag == True):
                self.sql = f"UPDATE AUX_TABLE set LOGRADOURO = '{row['address']['road']}, {house_number}', CIDADE = '{row['address']['city']}', BAIRRO = '{row['address']['suburb']}', ESTADO = '{row['address']['state']}', CEP= '{row['address']['postcode']}', REGIAO='{row['address']['region']}', PAIS= '{row['address']['country']}', SOME_ADITIONAL_INFO = '{et}', PROCESSED_DATE = GETDATE()  where LATITUDE ={lat} and LONGITUDE = {long}"
            else:
                self.sql = f"INSERT INTO AUX_TABLE values ({lat} , {long}, '{row['address']['road']}, {house_number}','{row['address']['city']}', '{row['address']['state']}', '{row['address']['suburb']}' , '{row['address']['postcode']}','{row['address']['region']}','{row['address']['country']}', '{et}', GETDATE() ) "
        else:

            if(update_flag == True):
                self.sql = f"UPDATE AUX_TABLE set LOGRADOURO = '{row['address']['road']}', CIDADE = '{row['address']['city']}', BAIRRO = '{row['address']['suburb']}', ESTADO = '{row['address']['state']}', CEP= '{row['address']['postcode']}', REGIAO='{row['address']['region']}', PAIS= '{row['address']['country']}', SOME_ADITIONAL_INFO = '{et}', PROCESSED_DATE = GETDATE()  where LATITUDE ={lat} and LONGITUDE = {long}"
            else:
                self.sql = f"INSERT INTO AUX_TABLE values ({lat} , {long}, '{row['address']['road']}','{row['address']['city']}', '{row['address']['state']}', '{row['address']['suburb']}' , '{row['address']['postcode']}','{row['address']['region']}','{row['address']['country']}', '{et}', GETDATE() ) "


    def validate_field_and_remove_spec_chars(self,row):
        
        exists_suburb = False
        exists_state = False
        exists_postcode = False
        exists_region = False
        exists_country = False
        exists_city = False
        exists_town = False

        for word in row['address']:
           row['address'][word] = row['address'][word].replace("'"," ") 
           if (word == 'suburb'):
               exists_suburb = True
           elif (word == 'state'):
               exists_state = True
           elif (word == 'postcode'):
               exists_postcode = True
           elif (word == 'region'):
               exists_region = True
           elif (word == 'country'):
               exists_country = True
           elif (word == 'city'):
               exists_city = True
           elif (word == 'town'):
               exists_town = True
       
        if (exists_suburb == False):
            row['address']['suburb'] = ''
        if (exists_state == False):
            row['address']['state'] = ''
        if (exists_postcode == False):
            row['address']['postcode'] = ''
        if (exists_region == False):
            row['address']['region'] = ''
        if (exists_country == False):
            row['address']['country'] = ''
        if (exists_city == False):
            row['address']['city'] = ''
        if(exists_town == True ):
            row['address']['city'] = row['address']['town']



        return row




