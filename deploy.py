#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Automated deployment script for multi-calendar-dimension package
اسکریپت خودکار برای deploy کردن پکیج
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step_num, message):
    """Print a step message"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[Step {step_num}]{Colors.END} {message}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def run_command(command, check=True):
    """Run a shell command"""
    print(f"  Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0 and check:
        print_error(f"Command failed: {command}")
        print(result.stderr)
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True

def main():
    """Main deployment function"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Multi-Calendar Dimension - Deployment Script{Colors.END}")
    print(f"{Colors.BOLD}Version 1.0.4 - Bug Fix Release{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"\nProject directory: {project_dir}")
    
    # Step 1: Clean old builds
    print_step(1, "Cleaning old builds...")
    dirs_to_clean = ['dist', 'build', 'multi_calendar_dimension.egg-info']
    for dir_name in dirs_to_clean:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print_success(f"Removed {dir_name}/")
    
    # Step 2: Run tests (if available)
    print_step(2, "Running tests...")
    if (project_dir / 'tests').exists():
        if not run_command("python -m pytest tests/ -v", check=False):
            print_warning("Tests failed or not configured. Continuing anyway...")
    else:
        print_warning("No tests directory found. Skipping tests.")
    
    # Step 3: Build package
    print_step(3, "Building package...")
    if not run_command("python -m build"):
        print_error("Build failed!")
        return 1
    print_success("Package built successfully!")
    
    # Step 4: Check package
    print_step(4, "Checking package with twine...")
    if not run_command("twine check dist/*"):
        print_error("Package check failed!")
        return 1
    print_success("Package check passed!")
    
    # Step 5: Ask user what to do
    print_step(5, "Ready to upload!")
    print("\nWhat would you like to do?")
    print("  1. Upload to TestPyPI (recommended for testing)")
    print("  2. Upload to PyPI (production)")
    print("  3. Exit without uploading")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print_step(6, "Uploading to TestPyPI...")
        if run_command("twine upload --repository testpypi dist/*"):
            print_success("Uploaded to TestPyPI!")
            print("\nTest installation:")
            print("  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ multi-calendar-dimension==1.0.4")
    
    elif choice == "2":
        print_warning("\n⚠ WARNING: You are about to upload to PRODUCTION PyPI!")
        confirm = input("Are you sure? Type 'YES' to confirm: ").strip()
        
        if confirm == "YES":
            print_step(6, "Uploading to PyPI...")
            if run_command("twine upload dist/*"):
                print_success("Uploaded to PyPI!")
                print("\n" + "="*60)
                print(f"{Colors.GREEN}{Colors.BOLD}Deployment Successful! 🎉{Colors.END}")
                print("="*60)
                print("\nNext steps:")
                print("  1. Test installation: pip install --upgrade multi-calendar-dimension")
                print("  2. Visit: https://pypi.org/project/multi-calendar-dimension/")
                print("  3. Commit and tag:")
                print('     git add .')
                print('     git commit -m "Release v1.0.4"')
                print('     git tag -a v1.0.4 -m "Version 1.0.4"')
                print('     git push origin main')
                print('     git push origin v1.0.4')
        else:
            print_warning("Upload cancelled.")
    
    else:
        print("Exiting without upload.")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

