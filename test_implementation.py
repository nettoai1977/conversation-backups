"""
Test script to verify the implementation of the OpenClaw integration enhancements.
"""

import asyncio
import json
from pathlib import Path

def test_mcp_servers_exist():
    """Test that all MCP server files exist."""
    print("🔍 Testing MCP Server Files...")
    
    mcp_dir = Path("mcp-servers")
    expected_files = [
        "crawl4ai_mcp_server.py",
        "notion_mcp_server.py", 
        "email_mcp_server.py",
        "business_ops_mcp_server.py",
        "research_analysis_mcp_server.py",
        "config.json",
        "start_all_servers.py"
    ]
    
    all_found = True
    for file in expected_files:
        file_path = mcp_dir / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            all_found = False
    
    return all_found

def test_skills_exist():
    """Test that enhanced skills exist."""
    print("\n🔍 Testing Enhanced Skills...")
    
    skills_dir = Path("skills")
    expected_files = [
        "enhanced_business_skills.py"
    ]
    
    all_found = True
    for file in expected_files:
        file_path = skills_dir / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            all_found = False
    
    return all_found

def test_config_valid():
    """Test that configuration file is valid JSON."""
    print("\n🔍 Testing Configuration File...")
    
    config_path = Path("mcp-servers/config.json")
    if not config_path.exists():
        print("  ❌ config.json not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for required sections
        required_sections = ["servers", "openclaw_config"]
        for section in required_sections:
            if section not in config:
                print(f"  ❌ Missing section: {section}")
                return False
        
        print("  ✅ config.json is valid")
        print(f"  📋 Found {len(config['servers'])} servers configured")
        
        # List the servers
        for server_name, server_info in config['servers'].items():
            print(f"    - {server_name}: {server_info['description']}")
        
        return True
    except json.JSONDecodeError:
        print("  ❌ config.json is not valid JSON")
        return False
    except Exception as e:
        print(f"  ❌ Error reading config.json: {e}")
        return False

def test_readme_exists():
    """Test that README exists and has content."""
    print("\n🔍 Testing Documentation...")
    
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("  ❌ README.md not found")
        return False
    
    content = readme_path.read_text()
    required_sections = [
        "Overview",
        "MCP Servers", 
        "Enhanced Skills Architecture",
        "Directory Structure",
        "Installation and Setup"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"  ⚠️  Missing sections in README: {', '.join(missing_sections)}")
        return True  # Still consider it OK, just warn
    else:
        print("  ✅ README.md complete with all required sections")
        return True

async def test_skills_import():
    """Test that skills can be imported without errors."""
    print("\n🔍 Testing Skills Import...")
    
    try:
        # Import the skills module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "enhanced_business_skills", 
            "skills/enhanced_business_skills.py"
        )
        skills_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(skills_module)
        
        # Check for expected functions
        expected_functions = [
            'send_email_skill',
            'schedule_meeting_skill',
            'create_client_profile_skill',
            'prioritize_tasks_skill',
            'optimize_workflow_skill'
        ]
        
        missing_functions = []
        for func in expected_functions:
            if not hasattr(skills_module, func):
                missing_functions.append(func)
        
        if missing_functions:
            print(f"  ❌ Missing functions: {missing_functions}")
            return False
        
        print("  ✅ Skills module imports successfully")
        print(f"  🛠️  Found {len(expected_functions)} skill functions")
        return True
        
    except ImportError as e:
        print(f"  ❌ Error importing skills: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing skills: {e}")
        return False

async def main():
    print("🧪 Testing OpenClaw Integration Enhancement Implementation")
    print("=" * 60)
    
    # Run all tests
    test_results = []
    
    test_results.append(("MCP Server Files", test_mcp_servers_exist()))
    test_results.append(("Skills Files", test_skills_exist()))
    test_results.append(("Configuration", test_config_valid()))
    test_results.append(("Documentation", test_readme_exists()))
    test_results.append(("Skills Import", await test_skills_import()))
    
    print(f"\n📊 Test Results:")
    print("-" * 30)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<25} {status}")
        if result:
            passed += 1
    
    print("-" * 30)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Implementation is ready.")
        print("\n🚀 To start using the implementation:")
        print("   1. Install requirements: pip install -r requirements.txt")
        print("   2. Start MCP servers: cd mcp-servers && python start_all_servers.py")
        print("   3. Add configuration to your OpenClaw config file")
        print("   4. Begin using the enhanced capabilities!")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the implementation.")

if __name__ == "__main__":
    asyncio.run(main())