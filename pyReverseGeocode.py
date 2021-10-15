import json
import pymssql
import urllib.request
from Helper import Helper
import time

#references test
#sample : 'lat': '-23.49742', 'lon': '-46.504256'
#link = f'https://nominatim.openstreetmap.org/reverse?lat=-23.630761812&lon=-46.614702818&format=json'

class ReverseGeocode:

    def __init__(self):
        self.lat = 0
        self.long = 0
        self.hp = Helper()
        self.cursor = self.conn()

    def get_reverse_gecode_address(self):

        try:
            with urllib.request.urlopen(f'https://nominatim.openstreetmap.org/reverse?lat={self.lat}&lon={self.long}&format=json') as url:

                if(url.code == 400):
                    print('Bad Request error.. waiting 60 seconds...')
                    time.sleep(60)
                    print('60 secs done.. return to processing..')
                    pass

                data = json.loads(url.read().decode())
                return data
        except Exception as ex:
            print('Request error: {ex}.. waiting 60 seconds...')
            time.sleep(60)
            print('60 secs done.. return to processing..')
            pass

    def conn(self):
        conn = pymssql.connect(self.hp.host, self.hp.user, self.hp.password, self.hp.database)
        conn.autocommit(True)

        cursor = conn.cursor(as_dict=True)

        return cursor

    def load_coordinates(self):

        update_flag = False

        try:
            self.cursor.execute(f"SELECT LAT, LONG FROM TABLE")
           
            for row in self.cursor.fetchall():
                self.lat = row['LOAD_Y'] #sample field to validate if value exists
                self.long = row['LOAD_X'] #sample field to validate if value exists
                et = '' #some other information that need to persist
                lat_dest = row['LATITUDE']
                long_dest = row['LONGITUDE']

                json_data = self.get_reverse_gecode_address()

                update_flag = self.coordinates_already_exists(lat_dest,long_dest)

                print(f'PROCESSING {json_data} for latitude {self.lat} and longite {self.long}\r\n')
                self.insert_address(json_data,et,update_flag)
        except Exception as ex :
            print(f'Exception for (lat,long)=({self.lat},{self.long}) : {ex}')

       
    def insert_address(self,row,et,update_flag):

        try:

            self.hp.sql_statment(row,et,self.lat,self.long,update_flag)
            self.cursor.execute(self.hp.sql)
            print(f"Address for  lat : {self.lat} and long: {self.long} has been PROCESSED.")
       
        except KeyError as ke:
           print(f'Value for field "{ke.args[0]}" NOT FOUND!! at lat : {self.lat} and long: {self.long}.. Moving to the next address..')
           pass

    def coordinates_already_exists(self,lat_dest,long_dest):

        if (lat_dest == None or long_dest == None ):
            return False
        return True



def main():

    r = ReverseGeocode()
    r.load_coordinates()
    SystemExit()

if __name__ == '__main__':
    main()
