from pathlib import Path
import os


Project_ROOT = Path(__file__).resolve().parents[1]

#Data directories
DATA_DIR = Project_ROOT / 'Data'
Cleaned_DATA_DIR = DATA_DIR / 'Cleaned'
RAW_DATA_DIR = DATA_DIR / 'Raw_Data'
Results_DIR = DATA_DIR / 'Results'

OUTPUT_PATH = RAW_DATA_DIR / 'Scraped.csv'
Cleaned_OUTPUT_PATH = Cleaned_DATA_DIR / 'Cleaned_Scraped.csv'
Results_OUTPUT_PATH = Results_DIR / 'Classified_Results.csv'
#Env
Env = Project_ROOT / '.env'

