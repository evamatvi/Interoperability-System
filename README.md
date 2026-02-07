#HL7–DICOM Interoperability Pipeline with Mirth Connect

This project implements an end-to-end healthcare interoperability pipeline that processes HL7 admission messages, generates XML worklists and JSON demographic files, dicomizes retinal images, and sends the resulting DICOM studies to a PACS.

The objective is to simulate a real clinical workflow using standard healthcare technologies and interoperability tools commonly found in hospital environments.



## Overview

The system follows a complete interoperability workflow:

1. Ingestion of HL7 ADT-A01 messages from a HIS using Mirth Connect  
2. Filtering of Emergency Department admissions  
3. Generation of XML worklists for a retinal camera  
4. Generation of patient demographic data in JSON format  
5. Automatic dicomization of retinal JPG images using Python  
6. Transmission of DICOM files to a PACS via C-STORE  



## Technologies Used

- **Mirth Connect**
- **HL7 v2.x**
- **Python**
- **DICOM**
- **PACS**
- **pydicom**
- **JavaScript (Mirth channel scripts)**

---

## Project Structure


├── channels/ 

│     ├── Deploy_unix.js

│     ├── Undeploy_unix.js

│     ├── Deploy_windows.js

│     └── Undeploy_windows.js
│
├── scripts/  

│     ├── worklist.py

│     ├── dicomitzador.py

│     ├── storage.py

│     ├── runner.sh

│     └── stopper.sh
│
└── README.md

