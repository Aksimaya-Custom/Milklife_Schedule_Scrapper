# Copyright (c) 2024, Kuronekosan
# This version is still alpha-release

import os
import re
from .tools import Tools
from .fileFolderHandler import FileHandler

class ExtractData(Tools, FileHandler):

    def extractDate(self, data: str, option: int = 0):
        dateNonLocale = data.split(' ', 1)[0]
        dateLocale = dateNonLocale.split('-', 3)
        date = dateLocale[0] if option == 0 else dateLocale[2]
        month = dateLocale[1]
        year = dateLocale[2] if option == 0 else dateLocale[0]
        month = 'Januari' if month == '01' else 'Februari' if month == '02' else 'Maret' if month == '03' else 'April' if month == '04' else 'Mei' if month == '05' else 'Juni' if month == '06' else 'Juli' if month == '07' else 'Agustus' if month == '08' else 'September' if month == '09' else 'Oktober' if month == '10' else 'November' if month == '11' else 'Desember'
        return self.cap('{d} {m} {y}'.format(d = date, m = month, y = year))

    def extractTime(self, data:str):
        timeRaw = data.split(' ', 1)[1]
        return timeRaw

    def extractDraw(self, data:str, separ:str = 'U10 '):
        return self.cap(data.split(separ,1)[1])

    def extractPlayers(self, data:str = '', separ:str = 'U10 '):
        dataBeforeTrim = data.replace(separ,'', -1)
        return self.cap( dataBeforeTrim.strip() )

    def extractPlayersFG(self, data:str = '', separ:str = 'U10 '):
        dataBeforeTrim = self.cap(data)
        dataBeforeTrim = re.sub('[(][A-Z,0-9][A-Z,0-9][)]', '', dataBeforeTrim)
        dataBeforeTrim = re.sub('[(][A-Z,0-9][A-Z,0-9][A-Z,0-9][)]', '', dataBeforeTrim)
        data = dataBeforeTrim.replace(separ, '', -1)
        return data.strip()

    def extractToCsv(self, data: str = "", date: str = "", cat: str = "U10", typed: str = "FG", name: str = ""):
        try:
            endpointFile = 'data/' + "{n}/".format(n = date) + "{c}/".format(c = cat) + typed
            self.checkAndCreateIfNotExists( 'data' )
            self.checkAndCreateIfNotExists( 'data/' + date )
            self.checkAndCreateIfNotExists( 'data/' + "{n}/".format(n = date) + cat )
            self.checkAndCreateIfNotExists( endpointFile )
            with open("{e}/{n}.csv".format(e = endpointFile, n = name), "w+") as file1:
                file1.write(data)
        except Exception as e:
            print("Error Occurred when check and creating folder or file, please check permission.")
            raise