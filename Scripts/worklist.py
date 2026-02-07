import os
import time
from datetime import datetime

src = '../Retinograf/2_Worklist_XML'
dst = '../Retinograf/2_Worklist_XML/_Tractats'

while True:
    # Per cada element que trobi a la carpeta src
    for fname in os.listdir(src):
        # Si es tracta d'un arxiu (no ha de tractar les subcarpetes)
        if os.path.isfile(os.path.join(src, fname)):
            print('Processing worklist from file: ' + fname)
            # Crea una marca de temps (timestamp)
            ara = datetime.now()
            timestamp = ara.strftime('%Y%m%d%H%M%S%f')[:-3]
            # Mou l'arxiu i li posa el timestamp com a prefix
            os.rename(os.path.join(src, fname),
                      os.path.join(dst, timestamp + '_' + fname))

    # Espera 60" abans de tornar a comprovar
    time.sleep(5)
