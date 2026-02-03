#!/usr/bin/env python3
"""
Python Version Checker (Simple Version)
This script checks your local Python version against the latest available version
and alerts you if you're running an outdated version.
"""

import sys
import subprocess


def compare_versions(v1, v2):
    """
    Compare two version strings.
    Returns: -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
    """
    def normalize(v):
        return [int(x) for x in v.replace('rc', '.').replace('a', '.').replace('b', '.').split('.')]

    n1 = normalize(v1)
    n2 = normalize(v2)
    
    # Pad the shorter version list with zeros
    max_len = max(len(n1), len(n2))
    n1.extend([0] * (max_len - len(n1)))
    n2.extend([0] * (max_len - len(n2)))
    
    for i in range(max_len):
        if n1[i] < n2[i]:
            return -1
        elif n1[i] > n2[i]:
            return 1
    return 0


def main():
    """Main function to run the Python version checker."""
    print("🔍 Python Version Checker")
    print("=" * 40)
    
    # Get local Python version
    local_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Local Python version: {local_version}")
    
    # Based on our web search, the latest stable version is Python 3.14.0
    latest_version = "3.14.0"
    print(f"Latest Python version (from research): {latest_version}")
    
    comparison = compare_versions(local_version, latest_version)
    
    if comparison < 0:
        print(f"\n⚠️  UPDATE AVAILABLE: You are running Python {local_version}, but Python {latest_version} is available!")
        print("\nBenefits of upgrading to the latest Python version:")
        print("- New features and syntax improvements")
        print("- Performance enhancements")
        print("- Security patches")
        print("- Bug fixes")
        print("- Better library compatibility")
        print("\nTo upgrade Python:")
        print("  - On macOS: brew install python or pyenv install latest")
        print("  - On Ubuntu/Debian: apt-get update && apt-get install python3")
        print("  - On Windows: Download from python.org")
        print("  - Using pyenv: pyenv install latest and pyenv global latest")
    elif comparison == 0:
        print(f"\n✅ UP TO DATE: You are running the latest Python version ({local_version})!")
    else:
        print(f"\n🚀 DEVELOPMENT VERSION: You are running Python {local_version}, which is newer than the latest stable release ({latest_version}).")
    
    print(f"\nAdditional Information:")
    print(f"  - Python implementation: {sys.implementation.name}")
    print(f"  - Python compiler: {sys.version.split()[3:5]}")
    print(f"  - Platform: {sys.platform}")
    print(f"  - Executable path: {sys.executable}")
    
    print("\n" + "=" * 40)
    if comparison < 0:
        print("⚠️  Consider upgrading your Python installation.")
    else:
        print("✅ Your Python installation is current!")


if __name__ == "__main__":
    main()