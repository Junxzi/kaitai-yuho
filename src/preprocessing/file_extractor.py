import os
import zipfile
from tqdm import tqdm

def extract_all_zips(zip_dir: str = "../data/0_raw/edinet_reports", extract_dir: str = "../data/2_interim/extracted_reports", log_file: str = "logs/extraction_errors.log"):
    """
    Extracts all .zip files from zip_dir to extract_dir.
    Skips if already extracted. Shows a progress bar.
    """
    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    zip_files = [f for f in os.listdir(zip_dir) if f.endswith(".zip")]

    with open(log_file, "a") as logf:
        for zip_file in tqdm(zip_files, desc="📦 Extracting ZIP files", ncols=100):
            doc_id = zip_file.replace(".zip", "")
            target_dir = os.path.join(extract_dir, doc_id)
            zip_path = os.path.join(zip_dir, zip_file)

            if os.path.exists(target_dir):
                continue # Skip if already extracted

            try:
                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(target_dir)
            except zipfile.BadZipFile:
                logf.write(f"{doc_id}\tBadZipFile: Corrupted or invalid ZIP file\n")
            except Exception as e:
                logf.write(f"{doc_id}\tUnexpected extraction error: {str(e)}\n")