#!/usr/bin/env python3
"""
Deploy the Cloud Function to GCP
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for GCP Cloud Function"""
    print("📦 Creating GCP Cloud Function deployment package...")
    
    # Clean up any existing package
    package_path = Path("feedback_bot_gcp.zip")
    if package_path.exists():
        package_path.unlink()
        print("🧹 Removed existing package")
    
    # Create the package
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the main function
        zipf.write("cloud_function.py")
        print("✅ Added cloud_function.py")
        
        # Add the bot module
        bot_dir = Path("../bot")
        if bot_dir.exists():
            for file_path in bot_dir.rglob("*.py"):
                arcname = f"bot/{file_path.relative_to(bot_dir)}"
                zipf.write(file_path, arcname)
                print(f"✅ Added {arcname}")
        
        # Add requirements
        requirements_file = Path("requirements.txt")
        if requirements_file.exists():
            zipf.write(requirements_file, "requirements.txt")
            print("✅ Added requirements.txt")
        
        # Add main.py for Cloud Functions
        main_content = """from cloud_function import main

# This is the entry point for Cloud Functions
def generate_feedback_bot(request):
    return main(request)
"""
        zipf.writestr("main.py", main_content)
        print("✅ Added main.py")
    
    print(f"📦 Created deployment package: {package_path}")
    print(f"📊 Package size: {package_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    return package_path

def main():
    print("🚀 GCP Cloud Function Deployment Script")
    print("=" * 50)
    
    # Create the deployment package
    package_path = create_deployment_package()
    
    print("\n📋 Next steps:")
    print("1. Go to GCP Console: https://console.cloud.google.com/functions")
    print("2. Create a new function called 'generate-feedback-bot'")
    print("3. Upload the zip file:", package_path)
    print("4. Set entry point to: main.generate_feedback_bot")
    print("5. Set runtime to: Python 3.9")
    print("6. Set memory to: 256 MB")
    print("7. Set timeout to: 60 seconds")
    print("8. Add environment variables:")
    print("   - SLACK_BOT_TOKEN")
    print("   - GOOGLE_SHEETS_ID")
    print("   - GOOGLE_CREDS_PATH")
    print("   - ENVIRONMENT=production")
    print("\n🔗 Then set up Cloud Scheduler!")

if __name__ == "__main__":
    main()
