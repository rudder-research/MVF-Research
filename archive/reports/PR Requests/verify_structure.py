#!/usr/bin/env python3
"""
VCF Repository Structure Verification Script

Run this script to verify that the VCF-RESEARCH repository
structure is correct and all imports work properly.
"""

import os
import sys
from pathlib import Path

def verify_structure():
    """Verify directory structure."""
    print("=" * 60)
    print("VCF REPOSITORY STRUCTURE VERIFICATION")
    print("=" * 60)
    
    required_dirs = [
        "data/raw",
        "data/clean",
        "data/interim",
        "docs/specs",
        "docs/proposals",
        "docs/references",
        "notebooks/exploration",
        "notebooks/pipeline",
        "notebooks/viz",
        "src/vcf/core",
        "src/vcf/data",
        "src/vcf/utils",
        "src/vcf/models",
        "src/vcf/config",
        "registry",
        "visuals/plots",
        "visuals/dashboards",
        "tests"
    ]
    
    print("\n✓ Checking directory structure...")
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
            print(f"  ✗ Missing: {dir_path}")
        else:
            print(f"  ✓ Found: {dir_path}")
    
    if missing:
        print(f"\n❌ {len(missing)} directories missing!")
        return False
    else:
        print(f"\n✅ All {len(required_dirs)} required directories present!")
    
    return True

def verify_files():
    """Verify key files exist."""
    print("\n✓ Checking key files...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "docs/specs/VCF_Geometry_Spec_v1.md",
        "registry/metric_registry.json",
        "registry/aliases.json",
        "src/vcf/__init__.py",
        "src/vcf/core/geometry_engine.py",
        "src/vcf/core/vector_math.py",
        "src/vcf/core/harmonics.py",
        "src/vcf/data/loader.py",
        "src/vcf/utils/normalization.py",
        "src/vcf/config/paths.py",
        "src/vcf/config/settings.py",
        "tests/test_normalization.py",
        "tests/test_geometry_engine.py"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
            print(f"  ✗ Missing: {file_path}")
        else:
            print(f"  ✓ Found: {file_path}")
    
    if missing:
        print(f"\n❌ {len(missing)} files missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present!")
    
    return True

def verify_imports():
    """Verify Python imports work."""
    print("\n✓ Checking Python imports...")
    
    imports_to_test = [
        "src.vcf.core.geometry_engine",
        "src.vcf.core.vector_math",
        "src.vcf.core.harmonics",
        "src.vcf.data.loader",
        "src.vcf.data.fred_fetcher",
        "src.vcf.data.yahoo_fetcher",
        "src.vcf.utils.normalization",
        "src.vcf.utils.filters",
        "src.vcf.config.paths",
        "src.vcf.config.settings"
    ]
    
    failed = []
    for module in imports_to_test:
        try:
            __import__(module)
            print(f"  ✓ Import successful: {module}")
        except ImportError as e:
            failed.append(module)
            print(f"  ✗ Import failed: {module} - {e}")
    
    if failed:
        print(f"\n❌ {len(failed)} imports failed!")
        return False
    else:
        print(f"\n✅ All {len(imports_to_test)} imports successful!")
    
    return True

def verify_git():
    """Verify git repository status."""
    print("\n✓ Checking git repository...")
    
    if not Path(".git").exists():
        print("  ✗ Not a git repository!")
        return False
    
    print("  ✓ Git repository initialized")
    
    # Check branches
    try:
        import subprocess
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True
        )
        branches = result.stdout
        print(f"\n  Branches:")
        for line in branches.split('\n'):
            if line.strip():
                print(f"    {line}")
        
        # Check if repo-structure-bootstrap-v1 exists
        if "repo-structure-bootstrap-v1" in branches:
            print("\n  ✓ Feature branch 'repo-structure-bootstrap-v1' exists")
        else:
            print("\n  ✗ Feature branch 'repo-structure-bootstrap-v1' not found")
            return False
            
    except Exception as e:
        print(f"  ✗ Error checking git: {e}")
        return False
    
    print("\n✅ Git repository properly configured!")
    return True

def main():
    """Run all verification checks."""
    # Change to script directory
    script_dir = Path(__file__).parent
    if script_dir.name == "VCF-RESEARCH":
        os.chdir(script_dir)
    
    print(f"\nCurrent directory: {Path.cwd()}")
    print()
    
    results = []
    
    # Run checks
    results.append(("Directory Structure", verify_structure()))
    results.append(("Key Files", verify_files()))
    results.append(("Python Imports", verify_imports()))
    results.append(("Git Repository", verify_git()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check:.<40} {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n" + "=" * 60)
        print("🎉 ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nThe VCF-RESEARCH repository is properly structured")
        print("and ready for Phase III implementation.")
        print("\nNext steps:")
        print("  1. Review the PR_SUMMARY.md")
        print("  2. Push to GitHub (if not already done)")
        print("  3. Create Pull Request")
        print("  4. Begin implementing core functionality")
        return 0
    else:
        print("\n" + "=" * 60)
        print("⚠️  SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease review the errors above and fix any issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
