import os
import hashlib
import json

ORDNER = "C:/Users/Milivoj/Desktop/FileScanner"
HASH_FILE = "hashes.json"

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan_folder():
    data = {}
    for root, _, files in os.walk(ORDNER):
        for name in files:
            p = os.path.join(root, name)
            data[p] = get_file_hash(p)
    return data

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(data):
    with open(HASH_FILE, "w") as f:
        json.dump(data, f, indent=2)

def compare_hashes(old, new):
    added = new.keys() - old.keys()
    removed = old.keys() - new.keys()
    changed = [k for k in new if k in old and new[k] != old[k]]

    if added:
        print("Neue Dateien:", *added, sep="\n  ")
    if removed:
        print("Gelöschte Dateien:", *removed, sep="\n  ")
    if changed:
        print("Geänderte Dateien:", *changed, sep="\n  ")
    if not (added or removed or changed):
        print("Keine Änderungen gefunden.")

def main():
    old = load_hashes()
    new = scan_folder()
    compare_hashes(old, new)
    save_hashes(new)

if __name__ == "__main__":
    main()
