import numpy as np
from max31855 import MAX31855

# Ce fichier transforme la donnée brute (sortie de capteur) en 
# mesure un peu filtrée. 


clk_pin=13
data_pin=19
cs_pin=26
th = MAX31855(cs_pin, clk_pin, data_pin)


FW = 5
raw = np.ones(FW) * th.get()
raw_idx = 0

# filtre = médiane des 5 dernières valeurs
def get():
    global raw_idx, FW, th
    raw[raw_idx] = th.get()
    raw_idx += 1
    raw_idx %= FW
    return np.median(raw)

    
