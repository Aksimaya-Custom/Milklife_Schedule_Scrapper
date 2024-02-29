# Copyright (c) 2024, Kuronekosan
# This version is still alpha-release

import math

class Tools:

    def cap(self, data: str):
        return data.upper()

    def round_up(self, data:int = 10, mod: int = 5):
        print("\n\nTotal data: ", data)
        dataReturn = data / mod
        if not data % mod == 0:
            dataReturn = math.floor(dataReturn) + 1
        return round(dataReturn)
    
    def stepper(self, total: int = 10, step: int = 5):
        data = {}
        count = 0
        loopingForExtractData = self.round_up(total, step)
        print( "{t} file will be generated on folder 'data'.\n\n".format(t = loopingForExtractData) )

        for segment in range(loopingForExtractData):
            if segment == 0:
                data[segment] = {
                    'first': count,
                    'last': count + (step - 1)
                }
                count += step
            elif segment == loopingForExtractData - 1:
                data[segment] = {
                    'first': count,
                    'last': total - 1
                }
            else:
                data[segment] = {
                    'first': count,
                    'last': count + (step - 1)
                }
                count += step
        return data