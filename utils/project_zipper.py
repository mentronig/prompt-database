# utils/project_zipper.py
import zipfile
import os

def zip_project(project_dir: str = ".", zip_name: str = "prompt_manager_snapshot.zip"):
    """
    Zippt das gesamte Projektverzeichnis für Sicherung oder Versand.

    :param project_dir: Verzeichnis, das gezippt werden soll
    :param zip_name: Name der ZIP-Datei
    """
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(project_dir):
            for filename in filenames:
                if filename.endswith(".py") or filename in ["requirements.txt", "database.json"]:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, project_dir)
                    zipf.write(file_path, arcname)



