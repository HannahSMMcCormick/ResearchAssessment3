from pathlib import Path
import os


Project_ROOT = Path(__file__).resolve().parents[1]

#Data directories
DATA_DIR = Project_ROOT / 'Data'
Cleaned_DATA_DIR = DATA_DIR / 'Cleaned'
RAW_DATA_DIR = DATA_DIR / 'Raw_Data'
Results_DIR = DATA_DIR / 'Results'

OUTPUT_AUTISM_PATH = RAW_DATA_DIR / 'Scraped.csv'
Cleaned_OUTPUT_AUTISM_PATH = Cleaned_DATA_DIR / 'Cleaned_Scraped.csv'
Results_OUTPUT_AUTISM_PATH = Results_DIR / 'Classified_Results.csv'

OUTPUT_PUBLIC_PATH = RAW_DATA_DIR / 'public_timeline.csv'
Cleaned_OUTPUT_PUBLIC_PATH = Cleaned_DATA_DIR / 'Cleaned_public_timeline.csv'
Results_OUTPUT_PUBLIC_PATH = Results_DIR / 'Classified_public_Results.csv'

#Env
Env = Project_ROOT / '.env'

