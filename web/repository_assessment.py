#!/usr/bin/env python3
"""
Repository Readiness Assessment
Comprehensive review of the fire-response-ai repository structure
"""

import os
import subprocess
from pathlib import Path

def assess_repository_structure():
    """Assess current repository structure and identify issues"""
    
    project_root = Path(__file__).parent.parent / "fire-response-rl"
    
    print("🔍 REPOSITORY STRUCTURE ASSESSMENT")
    print("=" * 60)
    
    assessment = {
        'structure_issues': [],
        'security_issues': [],
        'ci_cd_issues': [],
        'file_issues': [],
        'recommendations': []
    }
    
    # 1. Check basic structure
    print("\n1️⃣ BASIC STRUCTURE CHECK:")
    required_files = {
        'README.md': 'Project documentation',
        'requirements.txt': 'Python dependencies', 
        '.gitignore': 'Git ignore rules',
        'LICENSE': 'License file',
        'setup.py': 'Package setup'
    }
    
    for file_name, description in required_files.items():
        file_path = project_root / file_name
        if file_path.exists():
            print(f"   ✅ {file_name} - {description}")
        else:
            print(f"   ❌ {file_name} - {description}")
            assessment['structure_issues'].append(f"Missing {file_name}")
    
    # 2. Check for sensitive data
    print("\n2️⃣ SECURITY SCAN:")
    sensitive_patterns = [
        ('hf_', 'Hugging Face API keys'),
        ('sk-', 'OpenAI API keys'),
        ('AKIA', 'AWS Access Keys'),
        ('password', 'Hardcoded passwords'),
        ('secret', 'Secret tokens')
    ]
    
    security_clean = True
    for root, dirs, files in os.walk(project_root):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if file.endswith(('.py', '.html', '.js', '.json', '.md')):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    for pattern, description in sensitive_patterns:
                        if pattern in content and 'placeholder' not in content.lower():
                            if 'YOUR_' not in content and 'EXAMPLE' not in content:
                                assessment['security_issues'].append(
                                    f"Potential {description} in {file_path.relative_to(project_root)}"
                                )
                                security_clean = False
                except:
                    continue
    
    if security_clean:
        print("   ✅ No sensitive data detected")
    else:
        print(f"   ⚠️  {len(assessment['security_issues'])} potential security issues found")
    
    # 3. Check CI/CD configuration
    print("\n3️⃣ CI/CD CONFIGURATION:")
    workflow_path = project_root / ".github" / "workflows" / "ci.yml"
    
    if workflow_path.exists():
        print("   ✅ GitHub Actions workflow exists")
        
        with open(workflow_path, 'r') as f:
            workflow_content = f.read()
            
        # Check for common issues
        if '"3.10"' in workflow_content:
            print("   ✅ Python versions properly quoted")
        elif '3.10' in workflow_content:
            print("   ⚠️  Python versions may need quoting")
            assessment['ci_cd_issues'].append("Python versions should be quoted in YAML")
            
        if 'checkout@v4' in workflow_content:
            print("   ✅ Using recent GitHub Actions versions")
        else:
            print("   ⚠️  Consider updating GitHub Actions versions")
    else:
        print("   ❌ No GitHub Actions workflow found")
        assessment['ci_cd_issues'].append("Missing CI/CD workflow")
    
    # 4. Check test structure
    print("\n4️⃣ TEST STRUCTURE:")
    test_files = list(project_root.glob("test_*.py")) + list(project_root.glob("*_test.py"))
    
    if test_files:
        print(f"   ✅ Found {len(test_files)} test files")
        
        # Check if tests are discoverable
        for test_file in test_files:
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    
                if 'def test_' in content:
                    print(f"   ✅ {test_file.name} contains test functions")
                else:
                    print(f"   ⚠️  {test_file.name} may not contain valid tests")
                    assessment['file_issues'].append(f"{test_file.name} may not contain valid tests")
            except:
                assessment['file_issues'].append(f"Cannot read {test_file.name}")
    else:
        print("   ❌ No test files found")
        assessment['ci_cd_issues'].append("No test files found")
    
    # 5. Check dependencies
    print("\n5️⃣ DEPENDENCY CHECK:")
    requirements_path = project_root / "requirements.txt"
    
    if requirements_path.exists():
        with open(requirements_path, 'r') as f:
            requirements = f.read()
            
        critical_deps = ['torch', 'numpy', 'pytest']
        for dep in critical_deps:
            if dep in requirements:
                print(f"   ✅ {dep} dependency found")
            else:
                print(f"   ⚠️  {dep} dependency missing")
                assessment['structure_issues'].append(f"Missing {dep} dependency")
    
    # 6. Generate recommendations
    print("\n6️⃣ RECOMMENDATIONS:")
    
    if len(assessment['security_issues']) > 0:
        assessment['recommendations'].append("🔒 SECURITY: Clean up sensitive data before publication")
    
    if len(assessment['ci_cd_issues']) > 0:
        assessment['recommendations'].append("🔧 CI/CD: Fix workflow configuration issues")
        
    if len(assessment['structure_issues']) > 0:
        assessment['recommendations'].append("📁 STRUCTURE: Add missing required files")
        
    if len(assessment['file_issues']) > 0:
        assessment['recommendations'].append("🧪 TESTS: Fix test file issues")
    
    # Overall recommendation
    total_issues = (len(assessment['security_issues']) + 
                   len(assessment['ci_cd_issues']) + 
                   len(assessment['structure_issues']) + 
                   len(assessment['file_issues']))
    
    print("\n" + "=" * 60)
    print("📊 ASSESSMENT SUMMARY:")
    print(f"   Security Issues: {len(assessment['security_issues'])}")
    print(f"   CI/CD Issues: {len(assessment['ci_cd_issues'])}")  
    print(f"   Structure Issues: {len(assessment['structure_issues'])}")
    print(f"   File Issues: {len(assessment['file_issues'])}")
    print(f"   Total Issues: {total_issues}")
    
    if total_issues == 0:
        print("\n✅ RECOMMENDATION: Repository is ready for publication")
        recommendation = "READY"
    elif total_issues <= 3:
        print("\n🔧 RECOMMENDATION: Fix minor issues, no need to recreate repository")
        recommendation = "FIX_ISSUES"
    elif len(assessment['security_issues']) > 0:
        print("\n⚠️  RECOMMENDATION: Clean repository or recreate to remove sensitive data")
        recommendation = "SECURITY_CLEANUP"
    else:
        print("\n🔄 RECOMMENDATION: Consider restructuring repository")
        recommendation = "RESTRUCTURE"
    
    # Specific recommendations
    for rec in assessment['recommendations']:
        print(f"   • {rec}")
    
    return recommendation, assessment

if __name__ == "__main__":
    recommendation, assessment = assess_repository_structure()
    
    print(f"\n🎯 FINAL RECOMMENDATION: {recommendation}")
    
    if recommendation == "SECURITY_CLEANUP":
        print("\n🛡️  SECURITY CLEANUP STEPS:")
        print("   1. Remove any files with API keys")
        print("   2. Update .gitignore to prevent future leaks") 
        print("   3. Consider using environment variables")
        print("   4. Review commit history for sensitive data")
        
    elif recommendation == "FIX_ISSUES":
        print("\n🔧 QUICK FIX STEPS:")
        print("   1. Fix test file syntax errors")
        print("   2. Update CI/CD configuration")
        print("   3. Add any missing required files")
        print("   4. Test locally before pushing")
