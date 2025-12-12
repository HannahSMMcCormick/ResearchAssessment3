from pathlib import Path
import os


Project_ROOT = Path(__file__).resolve().parents[2]

#Data directories
DATA_DIR = Project_ROOT / 'Data'
Cleaned_DATA_DIR = DATA_DIR / 'Cleaned'
RAW_DATA_DIR = DATA_DIR / 'Raw_Data'
Results_DIR = DATA_DIR / 'Results'

#Data Output 

OUTPUT_PATH = RAW_DATA_DIR / 'public_timeline.csv'
Cleaned_OUTPUT_PATH = Cleaned_DATA_DIR / 'Cleaned_public_timeline.csv'
Results_OUTPUT_PATH = Results_DIR / 'Classified_public_Results.csv'
#Env
Env = Project_ROOT / '.env'

#Might need this not sure yet
def load_functions(module,path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Function to get a function from a module
def getfunction(mod, function_name: str):
    func = getattr(mod, function_name)
    return func
