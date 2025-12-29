# Create XZ (Default)
# python utils/pack_vcsky.py --output vcbr/custom.data.xz

# Create Raw Data
# python utils/pack_vcsky.py --output vcbr/custom.data

import os
import re
import json
import pathlib
import argparse
import lzma

# Default Paths
BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_METADATA_IN = BASE_DIR / "dist" / "modules" / "packages" / "en.js"
DEFAULT_METADATA_OUT = BASE_DIR / "dist" / "modules" / "packages" / "custom.js"
DEFAULT_DATA_OUT = BASE_DIR / "vcbr" / "custom.data.xz"
DEFAULT_INPUT_DIR = BASE_DIR / "extracted_vcsky"

def parse_metadata_filenames(js_path):
    print(f"Reading file list from {js_path}...")
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Metadata file not found at {js_path}")
        return []

    pattern = re.compile(r'filename:\s*"(.*?)",', re.DOTALL)
    matches = pattern.findall(content)
    
    print(f"Found {len(matches)} files in original metadata.")
    return matches

def pack_files(filenames, input_dir, output_data_path, output_js_path):
    output_data_path = pathlib.Path(output_data_path)
    is_xz = output_data_path.suffix == '.xz'
    
    mode_str = "LZMA2 (Max Compression)" if is_xz else "RAW (No Compression)"
    print(f"Packing files to {output_data_path} with {mode_str}...")
    
    new_files_metadata = []
    current_uncompressed_offset = 0
    
    input_dir = pathlib.Path(input_dir)
    
    try:
        if is_xz:
            lzma_filters = [{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}]
            out_f = lzma.open(output_data_path, "wb", filters=lzma_filters)
        else:
            out_f = open(output_data_path, "wb")
            
        with out_f:
            for filename in filenames:
                rel_path = filename.lstrip("/")
                file_path = input_dir / rel_path
                
                if not file_path.exists():
                    print(f"Warning: File not found: {file_path}")
                    continue
                
                size = file_path.stat().st_size
                
                with open(file_path, "rb") as in_f:
                    out_f.write(in_f.read())
                
                # Metadata always records UNCOMPRESSED offsets
                new_files_metadata.append({
                    "filename": filename,
                    "start": current_uncompressed_offset,
                    "end": current_uncompressed_offset + size
                })
                current_uncompressed_offset += size
                
    except Exception as e:
        print(f"Error packing files: {e}")
        return

    compressed_size = output_data_path.stat().st_size
    ratio = (1 - (compressed_size / current_uncompressed_offset)) * 100 if current_uncompressed_offset > 0 else 0

    print(f"Packing complete.")
    print(f"Total Uncompressed Size: {current_uncompressed_offset:,} bytes")
    print(f"Total Output Size:       {compressed_size:,} bytes")
    if is_xz:
        print(f"Compression Savings:     {ratio:.2f}%")

    print(f"Generating metadata at {output_js_path}...")
    
    js_content = "const DATA_PACKAGE = {\n    files: [\n"
    for i, item in enumerate(new_files_metadata):
        js_content += "    {\n"
        js_content += f'        filename: "{item["filename"]}",\n'
        js_content += f'        start: {item["start"]},\n'
        js_content += f'        end: {item["end"]}\n'
        js_content += "    }, " if i < len(new_files_metadata) - 1 else "    }\n"
            
    js_content += "    ],\n"
    js_content += f'    remote_package_size: {current_uncompressed_offset}\n'
    js_content += "};\n"
    
    with open(output_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("Metadata generation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack GTA VcSky assets.")
    parser.add_argument("--metadata-in", default=DEFAULT_METADATA_IN, help="Input JS metadata (manifest)")
    parser.add_argument("--input", default=DEFAULT_INPUT_DIR, help="Directory containing source files")
    parser.add_argument("--output", default=DEFAULT_DATA_OUT, help="Output .data or .data.xz file")
    parser.add_argument("--metadata-out", default=DEFAULT_METADATA_OUT, help="Output JS metadata file")
    
    args = parser.parse_args()
    
    filenames = parse_metadata_filenames(args.metadata_in)
    if filenames:
        pack_files(filenames, args.input, args.output, args.metadata_out)
