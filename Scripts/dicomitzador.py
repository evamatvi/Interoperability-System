import time
import os
import json
import pydicom
import pydicom.encaps
import pydicom.filewriter
from pathlib import Path
from datetime import datetime
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import UID
from PIL import Image

# --- CONFIGURATION AND PATHS ---
# Base directory for JSON demographic files (metadata input)
json_dir = Path('../Retinograf/3_Demografics_json/')
# Carpeta on mourem els JSON quan ja no els necessitem
json_tractats_dir = Path('../Retinograf/3_Demografics_json/_Tractats/')
# Base directory for JPG images (input)
jpg_dir = Path('../Retinograf/4_Retinos_jpg/')
# Base directory for final DICOM files (output)
output_dest = Path('../Retinograf/5_Retinos_dcm/')
#Base directory for processed images
processed_dir = Path('../Retinograf/4_Retinos_jpg/_Tractats/')

# Ens assegurem que les carpetes de tractats existeixen
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(json_tractats_dir, exist_ok=True)
os.makedirs(output_dest, exist_ok=True)

# Unique ID root for the institution/user (Used to prefix DICOM UIDs)
udg_id = '1990128'
implementation_uid_root = '1.2.826.0.1.' + udg_id
sop_class_uid = "1.2.840.10008.5.1.4.1.1.77.1.5.1"


# aquí hem decidit fer una funció per saber si queden o no imatges d'un pacient i així sabem si podem moure el json o no
def queden_imatges_pendents_del_pacient(patient_id: str) -> bool:
    """
    Hem fet aquesta funció perquè retorni True si dins la carpeta jpg_dir encara queda alguna imatge
    amb aquest patient_id pendent de processar.
    El format de les imatges es AccessionNumber_PatientID_Laterality(.JPG)
    """
    format = f"*_{patient_id}_*.JPG"

    pendents = list(jpg_dir.glob(format))
    return len(pendents) > 0



# --- MAIN LOOP: WATCH DIRECTORY ---

while True:
    # Get list of all JPG files in the input directory
    jpg_files = list(jpg_dir.glob('*.JPG'))
    
    if jpg_files:
        # Load all JSON files once per batch of JPGs
        json_files = list(json_dir.glob('*.json'))
        # hem decidit fer un diccionari per tenir tots els json amb clau el patient id per accedir despres més ràpidament
        json_map = {jf.stem: jf for jf in json_files}  # clau: "00653811" -> Path("00653811.json")
        
        for jpg_file in jpg_files:

             # --- 0 VALIDEM EL NOM DEL FITXER i que tingui el format correcte ---
            parts = jpg_file.stem.split('_')
            if len(parts) < 3:
                print(f"Nom de fitxer incorrecte (esperem que siguin 3 parts): {jpg_file.name}")
                continue

            # Filename should be in format: AccessionNumber_PatientID_Laterality
            accession_number = parts[0]
            patient_id = parts[1]
            laterality = parts[2]  # OD / OS

            # --- 0.1 BUSQUEM EL JSON del pacient (a partir del diccionari que ens ha semblat que així era més ràpid) ---
            json_found = json_map.get(patient_id)
            if not json_found:
                print(f"Alguna cosa no va bé ja que no existeix JSON per PatientID {patient_id} ({jpg_file.name})")
                continue

            # --- 1. EXTRACT DATA FROM FILE SYSTEM (DATE/TIME) ---
            
            # Use os.stat to get file metadata
            file_metadata = os.stat(jpg_file)
            
            # st_ctime is Creation Time on Windows, or Metadata Change Time on Unix/Linux.
            creation_dt = datetime.fromtimestamp(file_metadata.st_ctime)
            
            # DICOM Date/Time format (AAAAMMDD and HHMMSS)
            dicom_date = creation_dt.strftime("%Y%m%d")
            dicom_time = creation_dt.strftime("%H%M%S")
            
            # Assign dates/times (Assuming Study, Series, Acquisition times are the same)
            study_date = series_date = acquisition_date = dicom_date
            study_time = series_time = acquisition_time = dicom_time
            
            # --- 2. READ JPG PIXEL DATA AND DIMENSIONS ---
            
            # Read binary data for PixelData (compressed JPG data)
            with open(jpg_file, 'rb') as f:
                pixel_data = f.read()
            
            # Read dimensions using PIL (Pillow) - Object must be closed after use
            img = Image.open(jpg_file)
            # PIL returns (width, height), which corresponds to (Columns, Rows) in DICOM
            columns, rows = img.size 
            img.close() # Close the PIL image object
            
            # --- 3. READ DEMOGRAPHIC DATA FROM JSON ---

            with open(json_found, 'r') as file_data_j:
                demographic_data = json.load(file_data_j)
                    # PN format: LastName^SecondLastName^FirstName^MiddleName
                   
            patient_name = demographic_data['cognom1'] + '^' + demographic_data['cognom2'] + '^' + demographic_data['nom']
            patient_birth_date = demographic_data['dataNaixament']
            patient_sex = demographic_data['sexe']
                    
            # --- 4. FIXED CONSTANTS ---
                    
            modality = 'OP'
            manufacturer = 'Topcon'
            institution_name = 'Hospital^Universitari^Doctor^Josep^Trueta'
            institution_address = 'Avinguda^de^França^S/N^17007^Girona'
            station_name = 'u' + udg_id
            study_description = 'Non-mydriatic^retinography'
            institutional_department_name = 'Endocrinology'
            series_description = 'Non-mydriatic^retinography'
            manufacturer_model_name = 'ImageNET^i-base^3.2.4'
            body_part_examined = 'EYE'
            series_number = 1

            # --- 5. DICOM STRUCTURE: UID GENERATION AND METADATA ---
                    
            ds = Dataset()
                    
            # Generate UIDs for Study, Series, and Instance (SOP)
            study_instance_uid = implementation_uid_root + '.' + pydicom.uid.generate_uid(prefix=None)
            series_instance_uid = implementation_uid_root + '.' + pydicom.uid.generate_uid(prefix=None)
            sop_instance_uid = implementation_uid_root + '.' + pydicom.uid.generate_uid(prefix=None)

            # Set Content Date/Time (Time of DICOM creation, not acquisition)
            dt_now = datetime.now()
            ds.ContentDate = dt_now.strftime("%Y%m%d")
            # Truncate microseconds for DICOM TM format (HHMMSS.FFF)
            ds.ContentTime = dt_now.strftime("%H%M%S.%f")[:-3] 
                    
            # --- 6. FILE META INFORMATION HEADER (GROUP 0002) ---
                    
            file_meta = FileMetaDataset()
            # Set SOP Class for Ophthalmic Photography Image Storage
            file_meta.MediaStorageSOPClassUID = UID(sop_class_uid) 
            # Link the file header to the specific instance UID
            file_meta.MediaStorageSOPInstanceUID = sop_instance_uid 
            # Set the software identifier (Implementation Class UID)
            file_meta.ImplementationClassUID = UID(implementation_uid_root) 
            # Set Transfer Syntax for compressed JPEG Baseline (8-bit)
            file_meta.TransferSyntaxUID = UID("1.2.840.10008.1.2.4.50") 
            ds.file_meta = file_meta
            ds.SOPClassUID = sop_class_uid

            # --- 7. DATASET ASSIGNMENT (GROUPS 0008, 0010, 0020...) ---

            # === STUDY/SERIES/ACQUISITION TIMING ===
            ds.StudyDate = study_date                  #pdf_table: 0008,0020
            ds.SeriesDate = series_date                #pdf_table: 0008,0021
            ds.AcquisitionDate = acquisition_date      #pdf_table: 0008,0022
            ds.StudyTime = study_time                  #pdf_table: 0008,0030
            ds.SeriesTime = series_time                #pdf_table: 0008,0031
            ds.AcquisitionTime = acquisition_time      #pdf_table: 0008,0032
            ds.AccessionNumber = accession_number      #pdf_table: 0008,0050

            # === IMAGE/EQUIPMENT ===
            ds.SOPInstanceUID = sop_instance_uid       #pdf_table: 0008,0018
            ds.Modality = modality                     #pdf_table: 0008,0060
            ds.Manufacturer = manufacturer             #pdf_table: 0008,0070
            ds.InstitutionName = institution_name      #pdf_table: 0008,0080
            ds.InstitutionAddress = institution_address #pdf_table: 0008,0081
            ds.StationName = station_name              #pdf_table: 0008,1010
            ds.StudyDescription = study_description    #pdf_table: 0008,1030
            ds.InstitutionalDepartmentName = institutional_department_name #pdf_table: 0008,1040
            ds.SeriesDescription = series_description  #pdf_table: 0008,103E
            ds.ManufacturerModelName = manufacturer_model_name #pdf_table: 0008,1090
            ds.BodyPartExamined = body_part_examined   #pdf_table: 0018,0015
            ds.Laterality = laterality                 #pdf_table: 0020,0060

            # === PATIENT DEMOGRAPHICS ===
            ds.PatientName = patient_name              #pdf_table: 0010,0010
            ds.PatientID = patient_id                  #pdf_table: 0010,0020
            ds.PatientBirthDate = patient_birth_date   #pdf_table: 0010,0030
            ds.PatientSex = patient_sex                #pdf_table: 0010,0040

            # === STUDY/SERIES HIERARCHY ===
            ds.StudyInstanceUID = study_instance_uid   #pdf_table: 0020,000D
            ds.SeriesNumber = series_number            #pdf_table: 0020,0011
            ds.SeriesInstanceUID = series_instance_uid

            # --- PIXEL DATA DESCRIPTION TAGS (REQUIRED FOR DICOM IMAGE RECONSTRUCTION) ---

            # Image Dimensions
            ds.Rows = rows                              #Set the image height
            ds.Columns = columns                        #Set the image width

            # Color and Bit Depth
            ds.SamplesPerPixel = 3                      #Mandatory for color images (RGB/YBR)
            ds.PhotometricInterpretation = 'YBR_FULL_422' #Specifies the color space. YBR_FULL_422 is standard for 8-bit JPEG baseline compressed DICOM
            ds.BitsAllocated = 8                        #Bits reserved in memory for each color sample (8 bits = 256 levels)
            ds.BitsStored = 8                           #Bits containing valid pixel data (usually matches BitsAllocated for 8-bit images)
            ds.HighBit = 7                              #Position of the MSB
            ds.PixelRepresentation = 0                  #Set to 0 for Unsigned Integer

            # Data Storage Layout
            ds.PlanarConfiguration = 0                  #Set to 0 for color-by-pixel (RGBRGB...)
                    
            # Data format compression required
            ds.is_little_endian = True
            ds.is_implicit_VR = False

            # Actual Pixel Data Content
            ds.PixelData = pydicom.encaps.encapsulate([pixel_data])                   #The compressed binary content of the compressed JPG file
                                
            # --- 8. SAVE FILE ---
                    
            output_filename = jpg_file.stem + '.dcm'
            output_path = output_dest / output_filename                   
                    
            # Save the DICOM file (enforce_file_format=True ensures the file_meta header is written)
            ds.save_as(output_path.as_posix(), enforce_file_format=True)
                    
            #pydicom.filewriter.dcmwrite(output_path.as_posix(), ds)
                    
            print(f"SUCCESS: Created DICOM file for Patient ID {patient_id} at {output_path.as_posix()}")


            # --- 9. MOVE PROCESSED FILES --- 
            # Aquí el que fem és moure els jpg a la carpeta de tractats, ja que sempre que arribem aquí vol dir que ja s'ha creat el dcm correctament
            destination_path = processed_dir / jpg_file.name
            os.rename(jpg_file, destination_path)

            # Moure el JSON a _tractats només si ja no queden més imatges pendents del pacient ---
            # # Important: ho comprovem DESPRÉS de moure el JPG actual, així el patró ja no el troba com a "pendent"
            if not queden_imatges_pendents_del_pacient(patient_id):
                json_dest = json_tractats_dir / json_found.name
                print("Intentant moure:", json_found, "->", json_dest, "| dest existeix?", json_dest.exists())
                os.rename(json_found, json_dest)
                print(f"Hem mogut el JSONa _tractats: {json_found.name} perquè ja no queden imatges d'aquest pacient a processar.")

    # Delay the next check
    time.sleep(30)

