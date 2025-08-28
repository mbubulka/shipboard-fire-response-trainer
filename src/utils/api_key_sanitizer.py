#!/usr/bin/env python3
"""
API Key Sanitization Script
Removes hardcoded API keys from recovered files and replaces with environment variables
"""

import os
import re
from pathlib import Path

def sanitize_file(file_path):
    """Remove API keys from a file and replace with environment variable pattern"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace the hardcoded API key with environment variable pattern
        api_key_pattern = r"hf_[A-Za-z0-9_]{30,}"
        placeholder_patterns = [
            # JavaScript patterns
            (r"const HF_API_KEY = '[^']*';", "const HF_API_KEY = process.env.HF_API_KEY || 'YOUR_HUGGING_FACE_TOKEN';"),
            (r'const HF_API_KEY = "[^"]*";', 'const HF_API_KEY = process.env.HF_API_KEY || "YOUR_HUGGING_FACE_TOKEN";'),
            (r"HF_API_KEY = '[^']*'", "HF_API_KEY = 'YOUR_HUGGING_FACE_TOKEN'"),
            (r'HF_API_KEY = "[^"]*"', 'HF_API_KEY = "YOUR_HUGGING_FACE_TOKEN"'),
            
            # Direct API key replacements
            (api_key_pattern, "YOUR_HUGGING_FACE_TOKEN"),
        ]
        
        changes_made = False
        for pattern, replacement in placeholder_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
                print(f"  🔧 Sanitized API key pattern in {file_path.name}")
        
        # Write back if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Sanitized: {file_path}")
            return True
        else:
            print(f"⏭️  Clean: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main sanitization function"""
    
    recovery_root = Path("d:/projects/recovered-files")
    
    # File patterns to sanitize
    file_patterns = [
        "**/*.html",
        "**/*.js",
        "**/*.py"
    ]
    
    sanitized_files = []
    
    print("🔒 Starting API Key Sanitization...")
    print("=" * 60)
    
    for pattern in file_patterns:
        for file_path in recovery_root.glob(pattern):
            if file_path.is_file():
                if sanitize_file(file_path):
                    sanitized_files.append(str(file_path))
    
    print("=" * 60)
    print(f"✅ Sanitization complete!")
    print(f"🛡️  Sanitized {len(sanitized_files)} files")
    
    if sanitized_files:
        print("\n🔧 Sanitized files:")
        for file_path in sanitized_files:
            print(f"   • {file_path}")
    
    print("\n🎯 Files are now safe for deployment!")
    print("\n📋 Next steps:")
    print("   1. Set HF_API_KEY environment variable")
    print("   2. Deploy cleaned files to your hosting platform")
    print("   3. Test functionality with environment variables")

if __name__ == "__main__":
    main()
