#!/usr/bin/env python3
"""
Website Files Shipboard to Shipboard Replacement
"""

import os
import re
from pathlib import Path

def replace_shipboard_references(root_dir):
    """Replace Shipboard references with Shipboard in all relevant files"""
    
    # Define replacement mappings
    replacements = {
        'Shipboard': 'Shipboard',
        'shipboard': 'shipboard',
        'ShipboardCompartment': 'ShipboardCompartment',
        'ShipboardShipyardFireScenario': 'ShipboardFireScenario',
        'ShipboardShipyardScenarioGenerator': 'ShipboardScenarioGenerator',
        'ShipboardFireResponseAPI': 'ShipboardFireResponseAPI',
        'shipboard_shipyard': 'shipboard',
        'Shipboard-specific': 'Shipboard-specific',
        'maritime vessel': 'maritime vessel',
        'Shipboard Safety Officer': 'Shipboard Safety Officer',
        'Shipboard DCA': 'Shipboard DCA',
        'Shipboard Fire Response': 'Shipboard Fire Response',
        'Shipboard SAFETY OFFICER': 'SHIPBOARD SAFETY OFFICER',
        'Shipboard engineering': 'shipboard engineering',
        'Shipboard machinery': 'shipboard machinery',
        'Shipboard flight deck': 'shipboard deck areas',
        'Shipboard and USCG': 'shipboard and USCG',
        'shipboard_operations': 'shipboard_operations'
    }
    
    # File extensions to process
    extensions = ['.py', '.md', '.yml', '.json', '.html']
    
    files_processed = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Apply replacements
                    for old, new in replacements.items():
                        content = content.replace(old, new)
                    
                    # Only write if changes were made
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"✅ Updated: {file_path.relative_to(root_dir)}")
                        files_processed += 1
                    
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎯 Processed {files_processed} files")
    return files_processed

if __name__ == "__main__":
    root_directory = Path(".")
    print("🔄 Starting Shipboard to Shipboard replacement for website files...")
    print(f"📁 Processing directory: {root_directory.resolve()}")
    
    count = replace_shipboard_references(root_directory)
    
    print(f"\n✅ Website replacement complete! Updated {count} files.")
    print("🎯 All Shipboard references have been replaced with Shipboard references.")
