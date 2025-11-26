"""
DRIVE MIRROR SYNC SCRIPT
========================

INSTRUCTIONS:
1. Create a NEW notebook in Google Colab
2. Copy each cell block below into separate cells in Colab
3. For markdown cells, change cell type to "Markdown"
4. For code cells, leave as "Code"
5. Run all cells (Runtime → Run all)

Cell types are marked as:
# MARKDOWN CELL or # CODE CELL
"""

# =============================================================================
# MARKDOWN CELL 1: Title and Instructions
# =============================================================================
"""
# 🔄 Drive Mirror Sync Notebook

**Purpose:** Synchronize `/MyDrive/VCF-RESEARCH` to GitHub repository `rudder-research/drive_mirror`

**Direction:** Google Drive → GitHub (one-way)

**Status:** Production-ready

---

## ⚙️ Configuration

**Required Secrets (store in Colab Secrets):**
- `GITHUB_TOKEN` - Personal Access Token with `repo` scope

**Source:** `/MyDrive/VCF-RESEARCH`  
**Destination:** `github.com/rudder-research/drive_mirror`

---

## 📋 Instructions

1. **Setup (one-time):**
   - Create GitHub Personal Access Token
   - Store as `GITHUB_TOKEN` in Colab Secrets (🔑 icon)
   - Enable "Notebook access" for the secret

2. **Run sync:**
   - Runtime → Run all
   - Authorize Drive access when prompted
   - Wait for completion (~1-5 minutes)

3. **Verify:**
   - Check GitHub repository for new commit
   - Review commit message for sync details

---
"""

# =============================================================================
# MARKDOWN CELL 2: Section Header
# =============================================================================
"""
## 1️⃣ Install Dependencies & Setup
"""

# =============================================================================
# CODE CELL 1: Install and Import
# =============================================================================

# Install required packages
!pip install -q gitpython

import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
from google.colab import drive, userdata
import git

print("✅ Dependencies installed")
print(f"📅 Sync started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# =============================================================================
# MARKDOWN CELL 3: Section Header
# =============================================================================
"""
## 2️⃣ Configuration & Validation
"""

# =============================================================================
# CODE CELL 2: Configuration and Validation
# =============================================================================

# ============================================================================
# CONFIGURATION
# ============================================================================

# GitHub configuration
GITHUB_USERNAME = "rudder-research"
GITHUB_REPO = "drive_mirror"
GITHUB_BRANCH = "main"

# Google Drive configuration
DRIVE_SOURCE_PATH = "/content/drive/MyDrive/VCF-RESEARCH"

# Local workspace
LOCAL_REPO_PATH = "/content/drive_mirror"

# Git configuration
GIT_USER_NAME = "Drive Mirror Bot"
GIT_USER_EMAIL = "noreply@rudder-research.github.io"

# ============================================================================
# VALIDATION
# ============================================================================

print("🔍 Validating configuration...\n")

# Check for GitHub token
try:
    GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')
    print("✅ GitHub token found")
except Exception as e:
    print("❌ ERROR: GITHUB_TOKEN not found in Colab Secrets")
    print("\n📝 To fix:")
    print("   1. Click the key icon (🔑) in left sidebar")
    print("   2. Add secret: Name='GITHUB_TOKEN', Value=[your PAT]")
    print("   3. Enable 'Notebook access'")
    print("   4. Re-run this cell")
    raise Exception("Missing GITHUB_TOKEN")

# Build GitHub URL with token
GITHUB_URL = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

print(f"\n📊 Configuration:")
print(f"   Repository: {GITHUB_USERNAME}/{GITHUB_REPO}")
print(f"   Branch: {GITHUB_BRANCH}")
print(f"   Drive Source: {DRIVE_SOURCE_PATH}")
print(f"   Local Path: {LOCAL_REPO_PATH}")
print("\n✅ Configuration valid")


# =============================================================================
# MARKDOWN CELL 4: Section Header
# =============================================================================
"""
## 3️⃣ Mount Google Drive
"""

# =============================================================================
# CODE CELL 3: Mount Drive
# =============================================================================

print("📁 Mounting Google Drive...\n")

# Mount Drive
drive.mount('/content/drive', force_remount=False)

# Verify source folder exists
if not Path(DRIVE_SOURCE_PATH).exists():
    print(f"\n❌ ERROR: Drive folder not found: {DRIVE_SOURCE_PATH}")
    print("\n📝 To fix:")
    print("   1. Check folder exists in Google Drive")
    print("   2. Verify folder name (case-sensitive)")
    print("   3. Update DRIVE_SOURCE_PATH if needed")
    raise FileNotFoundError(f"Drive folder not found: {DRIVE_SOURCE_PATH}")

# Count files in source
source_files = list(Path(DRIVE_SOURCE_PATH).rglob('*'))
source_file_count = len([f for f in source_files if f.is_file()])

print(f"✅ Drive mounted successfully")
print(f"📊 Source folder: {source_file_count} files found")


# =============================================================================
# MARKDOWN CELL 5: Section Header
# =============================================================================
"""
## 4️⃣ Clone or Update Repository
"""

# =============================================================================
# CODE CELL 4: Clone Repository
# =============================================================================

print("📥 Setting up local repository...\n")

# Clean up any existing repo
if Path(LOCAL_REPO_PATH).exists():
    print("🧹 Removing existing local repository...")
    shutil.rmtree(LOCAL_REPO_PATH)

# Clone repository
print(f"📥 Cloning {GITHUB_USERNAME}/{GITHUB_REPO}...")

try:
    repo = git.Repo.clone_from(
        GITHUB_URL,
        LOCAL_REPO_PATH,
        branch=GITHUB_BRANCH
    )
    print("✅ Repository cloned successfully")
except git.exc.GitCommandError as e:
    if "not found" in str(e).lower():
        print("❌ ERROR: Repository not found or token invalid")
        print("\n📝 To fix:")
        print("   1. Verify repository exists on GitHub")
        print("   2. Check token has 'repo' scope")
        print("   3. Ensure token hasn't expired")
    raise

# Configure git
with repo.config_writer() as git_config:
    git_config.set_value('user', 'name', GIT_USER_NAME)
    git_config.set_value('user', 'email', GIT_USER_EMAIL)

print(f"✅ Git configured: {GIT_USER_NAME} <{GIT_USER_EMAIL}>")


# =============================================================================
# MARKDOWN CELL 6: Section Header
# =============================================================================
"""
## 5️⃣ Sync Files from Drive to Repo
"""

# =============================================================================
# CODE CELL 5: Sync Files
# =============================================================================

print("🔄 Syncing files from Drive to repository...\n")

# Files to preserve (never delete)
PRESERVE_FILES = {'.git', '.gitignore', 'README.md', 'LICENSE'}

# Step 1: Remove all files except preserved ones
print("🧹 Cleaning repository...")
removed_count = 0

for item in Path(LOCAL_REPO_PATH).iterdir():
    if item.name not in PRESERVE_FILES:
        if item.is_file():
            item.unlink()
            removed_count += 1
        elif item.is_dir():
            shutil.rmtree(item)
            removed_count += 1

print(f"   Removed {removed_count} items")

# Step 2: Copy all files from Drive
print("\n📋 Copying files from Drive...")
copied_count = 0
skipped_count = 0

def should_ignore(path):
    """Check if file should be ignored based on common patterns."""
    path_str = str(path)
    ignore_patterns = [
        '.ipynb_checkpoints',
        '__pycache__',
        '.DS_Store',
        'Thumbs.db',
        '.tmp.drive',
        '~$',
    ]
    return any(pattern in path_str for pattern in ignore_patterns)

for source_path in Path(DRIVE_SOURCE_PATH).rglob('*'):
    if source_path.is_file():
        # Skip ignored files
        if should_ignore(source_path):
            skipped_count += 1
            continue
        
        # Calculate relative path
        rel_path = source_path.relative_to(DRIVE_SOURCE_PATH)
        dest_path = Path(LOCAL_REPO_PATH) / rel_path
        
        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        copied_count += 1

print(f"   Copied {copied_count} files")
print(f"   Skipped {skipped_count} files (ignored patterns)")
print("\n✅ Sync complete")


# =============================================================================
# MARKDOWN CELL 7: Section Header
# =============================================================================
"""
## 6️⃣ Detect Changes & Prepare Commit
"""

# =============================================================================
# CODE CELL 6: Detect Changes
# =============================================================================

print("🔍 Detecting changes...\n")

# Get repository status
repo = git.Repo(LOCAL_REPO_PATH)

# Check for changes
changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files

# Count by type
modified_files = [f for f in changed_files if Path(LOCAL_REPO_PATH, f).exists()]
deleted_files = [f for f in changed_files if not Path(LOCAL_REPO_PATH, f).exists()]
new_files = untracked_files

total_changes = len(modified_files) + len(deleted_files) + len(new_files)

print(f"📊 Change Summary:")
print(f"   New files: {len(new_files)}")
print(f"   Modified files: {len(modified_files)}")
print(f"   Deleted files: {len(deleted_files)}")
print(f"   Total changes: {total_changes}")

if total_changes == 0:
    print("\n✅ No changes detected - Drive and GitHub are in sync")
    HAS_CHANGES = False
else:
    print("\n📝 Changes detected - preparing commit...")
    HAS_CHANGES = True
    
    # Show sample of changes
    if new_files:
        print(f"\n   Sample new files (showing up to 5):")
        for f in new_files[:5]:
            print(f"      + {f}")
    
    if modified_files:
        print(f"\n   Sample modified files (showing up to 5):")
        for f in modified_files[:5]:
            print(f"      ~ {f}")
    
    if deleted_files:
        print(f"\n   Sample deleted files (showing up to 5):")
        for f in deleted_files[:5]:
            print(f"      - {f}")


# =============================================================================
# MARKDOWN CELL 8: Section Header
# =============================================================================
"""
## 7️⃣ Commit & Push Changes
"""

# =============================================================================
# CODE CELL 7: Commit and Push
# =============================================================================

if HAS_CHANGES:
    print("📤 Committing and pushing changes...\n")
    
    # Stage all changes
    repo.git.add(A=True)
    print("✅ Changes staged")
    
    # Create commit message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"""Sync from Google Drive - {timestamp}

Changes:
- New files: {len(new_files)}
- Modified files: {len(modified_files)}
- Deleted files: {len(deleted_files)}
- Total changes: {total_changes}

Source: /MyDrive/VCF-RESEARCH
Synced by: Drive Mirror Bot (Colab)
"""
    
    # Commit changes
    repo.index.commit(commit_message)
    print("✅ Changes committed")
    
    # Push to GitHub
    print("\n📤 Pushing to GitHub...")
    try:
        origin = repo.remote('origin')
        push_info = origin.push()
        
        # Check push result
        if push_info and push_info[0].flags & git.remote.PushInfo.ERROR:
            print("❌ Push failed")
            print(f"   Error: {push_info[0].summary}")
        else:
            print("✅ Push successful")
            print(f"\n🎉 Sync complete!")
            print(f"   View on GitHub: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
    
    except git.exc.GitCommandError as e:
        print("❌ Push failed")
        print(f"   Error: {str(e)}")
        raise

else:
    print("\n✅ No changes to commit - repository is up to date")


# =============================================================================
# MARKDOWN CELL 9: Section Header
# =============================================================================
"""
## 8️⃣ Cleanup & Summary
"""

# =============================================================================
# CODE CELL 8: Cleanup and Summary
# =============================================================================

print("🧹 Cleaning up...\n")

# Clear token from memory (security)
GITHUB_TOKEN = None
GITHUB_URL = None

# Get final repository stats
repo = git.Repo(LOCAL_REPO_PATH)
latest_commit = repo.head.commit

print("="*60)
print("📊 SYNC SUMMARY")
print("="*60)
print(f"\n📁 Source: {DRIVE_SOURCE_PATH}")
print(f"🎯 Destination: {GITHUB_USERNAME}/{GITHUB_REPO}")
print(f"🌿 Branch: {GITHUB_BRANCH}")
print(f"\n📊 Statistics:")
print(f"   Files in Drive: {source_file_count}")
print(f"   Files copied: {copied_count}")
print(f"   Files skipped: {skipped_count}")
print(f"   Total changes: {total_changes if HAS_CHANGES else 0}")
print(f"\n📝 Latest commit:")
print(f"   SHA: {latest_commit.hexsha[:8]}")
print(f"   Author: {latest_commit.author}")
print(f"   Date: {datetime.fromtimestamp(latest_commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Message: {latest_commit.message.split(chr(10))[0]}")
print(f"\n🔗 View on GitHub:")
print(f"   https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
print(f"\n⏰ Sync completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

if HAS_CHANGES:
    print("\n✅ Sync successful - changes pushed to GitHub")
else:
    print("\n✅ Sync successful - no changes needed")

print("\n✨ Done!")


# =============================================================================
# MARKDOWN CELL 10: Footer
# =============================================================================
"""
---

## 🔒 Security Notes

- GitHub token is stored in Colab Secrets (not in notebook)
- Token is cleared from memory after use
- Token is never printed or logged
- Repository uses HTTPS with token authentication

## 📝 Next Steps

1. Review changes on GitHub
2. Verify no sensitive data was committed
3. Update documentation if needed
4. Run sync again when Drive contents change

## 🔄 Sync Frequency

Recommended: Run weekly or after major Drive updates

---

*Drive Mirror Bot v1.0 - Powered by Google Colab*
"""

# =============================================================================
# END OF SCRIPT
# =============================================================================

print("""
================================================================================
COLAB NOTEBOOK SETUP COMPLETE
================================================================================

TO USE THIS SCRIPT:

1. Open Google Colab: https://colab.research.google.com
2. Create a new notebook (File → New notebook)
3. Copy the cell blocks above into separate cells
4. Change markdown cells to "Markdown" type (click dropdown)
5. Keep code cells as "Code" type
6. Save notebook as "Drive_Mirror_Sync.ipynb"
7. Follow the instructions in the first cell

IMPORTANT:
- Markdown cells start with triple quotes and contain markdown text
- Code cells contain Python code
- Make sure to create the GITHUB_TOKEN secret in Colab first!

================================================================================
""")
