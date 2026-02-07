import os
import time
import shutil
import pydicom
from pydicom.uid import UID
from pynetdicom import AE
from pathlib import Path

DCM_DIR = Path("../Retinograf/5_Retinos_dcm") 
TRACTATS = Path("../Retinograf/5_Retinos_dcm/_Tractats")
os.makedirs(TRACTATS, exist_ok=True)

pacs_ip = "www.dicomserver.co.uk"
pacs_port = 11112
pacs_ae = "DCMSERVER"
JPEG_BASELINE_UID = UID('1.2.840.10008.1.2.4.50')

ae = AE(ae_title="RET1987846")
ae.add_requested_context('1.2.840.10008.5.1.4.1.1.77.1.5.1', 
                         transfer_syntax=JPEG_BASELINE_UID)

print("storage.py en marxa...")

while True:
    fitxers = [f for f in os.listdir(DCM_DIR) if f.endswith(".dcm")]

    for f in fitxers:
        path_origen = DCM_DIR / f
        ds = pydicom.dcmread(path_origen.as_posix(), force=True)
        assoc = ae.associate(pacs_ip, pacs_port, ae_title=pacs_ae)

        if assoc.is_established:
            assoc.send_c_store(ds)
            assoc.release()
            path_desti = TRACTATS / f
            shutil.move(path_origen, path_desti)
            print(f"Enviat i mogut: {f}")
        else:
            print("No s'ha pogut connectar al PACS.")

    time.sleep(30)
