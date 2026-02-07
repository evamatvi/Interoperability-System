# HL7–DICOM Interoperability Pipeline with Mirth Connect

## General Description
This project implements an end-to-end healthcare interoperability pipeline that simulates a real clinical workflow using standard hospital technologies.

The system processes HL7 admission messages, generates worklists and demographic files, dicomizes retinal images, and transmits the resulting DICOM studies to a PACS. The project focuses on interoperability between information systems and medical imaging workflows commonly found in hospital environments.

The main goal is to demonstrate how different healthcare standards and tools can be integrated to support automated, reliable, and scalable clinical data exchange.

---

## Objectives
- Simulate a real clinical interoperability workflow
- Process HL7 ADT-A01 admission messages from a Hospital Information System (HIS)
- Generate XML worklists for a retinal imaging device
- Generate patient demographic data in JSON format
- Automatically dicomize retinal images
- Transmit DICOM studies to a PACS using standard protocols

---

## System Overview
The system follows a complete interoperability pipeline composed of several stages:

1. Ingestion of HL7 ADT-A01 messages from a HIS using Mirth Connect  
2. Filtering of admissions corresponding to the Emergency Department  
3. Generation of XML worklists for a retinal camera  
4. Generation of patient demographic data in JSON format  
5. Automatic dicomization of retinal JPG images using Python  
6. Transmission of DICOM files to a PACS via the C-STORE protocol  

This workflow reproduces the interaction between clinical information systems and medical imaging systems in a hospital setting.

---

## Workflow Description
When an HL7 ADT-A01 message is received, the system extracts and validates patient and admission data. Only Emergency Department admissions are processed further.

For valid cases:
- An XML worklist is generated to be consumed by a retinal camera
- A JSON file containing patient demographic information is created
- Retinal images in JPG format are automatically converted into DICOM files
- The resulting DICOM studies are sent to a PACS using standard DICOM networking services

This process ensures consistency between administrative data and imaging data.

---

## Technologies Used
The project integrates multiple healthcare standards and tools:

- **Mirth Connect**  
  Used as the integration engine to receive, filter, and process HL7 messages.

- **HL7 v2.x**  
  Used for patient admission and demographic information exchange.

- **Python**  
  Used for image processing and automatic dicomization.

- **DICOM**  
  Used as the standard for medical imaging storage and transmission.

- **PACS**  
  Acts as the storage system for the generated DICOM studies.

- **pydicom**  
  Python library used to create and manipulate DICOM files.

- **JavaScript (Mirth channel scripts)**  
  Used for message transformation and routing inside Mirth Connect.

---

## Design and Architecture
The system follows a modular and interoperable architecture, where each stage of the pipeline has a well-defined responsibility.

Key design principles include:
- Compliance with healthcare standards
- Clear separation between data ingestion, processing, and transmission
- Automation of repetitive clinical workflows
- Scalability and adaptability to real hospital environments

This design makes the pipeline suitable for educational purposes as well as for prototyping real clinical interoperability solutions.
