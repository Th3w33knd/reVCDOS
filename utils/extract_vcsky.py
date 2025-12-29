# Extract XZ
# python utils/extract_vcsky.py --data vcbr/custom.data.xz --output extracted_vcsky

import os
import re
import pathlib
import argparse
import lzma

# Default Paths (can be overridden by CLI args)
BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_METADATA = BASE_DIR / "dist" / "modules" / "packages" / "custom.js"
DEFAULT_DATA = BASE_DIR / "vcbr" / "custom.data.xz"
DEFAULT_OUTPUT = BASE_DIR / "extracted_vcsky"

def parse_metadata(js_path):
    print(f"Reading metadata from {js_path}...")
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Metadata file not found at {js_path}")
        return []

    # Regex to find file entries
    pattern = re.compile(r'filename:\s*"(.*?)",\s*start:\s*(\d+),\s*end:\s*(\d+)', re.DOTALL)
    matches = pattern.findall(content)
    
    files = []
    for filename, start, end in matches:
        files.append({
            "filename": filename,
            "start": int(start),
            "end": int(end)
        })
    
    print(f"Found {len(files)} files in metadata.")
    return files

def extract_files(data_path, files, output_dir):
    data_path = pathlib.Path(data_path)
    print(f"Opening data file {data_path}...")
    
    try:
        # Determine opener based on extension
        opener = lzma.open if data_path.suffix == '.xz' else open
        
        with opener(data_path, "rb") as f:
            for item in files:
                rel_path = item["filename"].lstrip("/")
                out_path = output_dir / rel_path
                
                # Create directories
                out_path.parent.mkdir(parents=True, exist_ok=True)
                
                # For XZ, we can't easily seek randomly without re-reading from start or using an index.
                # However, Python's lzma module handles seeking in .xz files by decoding blocks.
                # It might be slow for random access, but since our files are sequential in the block usually,
                # it's acceptable for this script.
                # Note: If the file was packed sequentially, sequential reads are fast.
                
                f.seek(item["start"])
                size = item["end"] - item["start"]
                data = f.read(size)
                
                with open(out_path, "wb") as out_f:
                    out_f.write(data)
                
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return
    except Exception as e:
        print(f"Error during extraction: {e}")
        return

    print("Extraction complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GTA VcSky assets.")
    parser.add_argument("--metadata", default=DEFAULT_METADATA, help="Path to the JS metadata file")
    parser.add_argument("--data", default=DEFAULT_DATA, help="Path to the .data or .data.xz file")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output directory")
    
    args = parser.parse_args()
    
    files = parse_metadata(args.metadata)
    if files:
        extract_files(args.data, files, pathlib.Path(args.output))
