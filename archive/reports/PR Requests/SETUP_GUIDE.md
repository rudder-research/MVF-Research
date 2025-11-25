# Drive Mirror - Repository Initialization Guide

This guide walks you through setting up the `drive_mirror` repository on GitHub.

## 📋 Prerequisites

- GitHub account (`rudder-research`)
- Google Drive with `/MyDrive/VCF-RESEARCH` folder
- Google Colab access

## 🚀 Step-by-Step Setup

### 1. Create GitHub Repository

1. **Go to GitHub:**
   - Navigate to https://github.com/new
   - Sign in as `rudder-research`

2. **Repository settings:**
   - Repository name: `drive_mirror`
   - Description: `Mirror of /MyDrive/VCF-RESEARCH for review and backup`
   - Visibility: **Private** (recommended) or Public
   - ✅ Initialize with README
   - ✅ Add .gitignore: Python
   - ❌ Add license: (skip for now)

3. **Create repository**
   - Click "Create repository"

### 2. Replace Default Files

The repository will be initialized with default files. Replace them:

1. **Upload this repository's files:**
   - Go to your new repository
   - Click "Add file" → "Upload files"
   - Upload:
     - `README.md` (from this folder)
     - `.gitignore` (from this folder)
   - Commit message: "Initialize drive_mirror repository"
   - Click "Commit changes"

**OR use git from command line:**

```bash
# Clone the new repository
git clone https://github.com/rudder-research/drive_mirror.git
cd drive_mirror

# Copy files from this folder
cp /path/to/drive_mirror/README.md .
cp /path/to/drive_mirror/.gitignore .

# Commit and push
git add README.md .gitignore
git commit -m "Initialize drive_mirror repository"
git push origin main
```

### 3. Create Personal Access Token (PAT)

1. **Navigate to token settings:**
   - Go to https://github.com/settings/tokens
   - Click "Tokens (classic)"
   - Click "Generate new token" → "Generate new token (classic)"

2. **Token configuration:**
   - Note: `drive_mirror_sync`
   - Expiration: 90 days (or custom)
   - **Scopes:** Select **`repo`** (Full control of private repositories)
     - ✅ repo:status
     - ✅ repo_deployment
     - ✅ public_repo
     - ✅ repo:invite
     - ✅ security_events

3. **Generate and copy:**
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)
   - Store securely (you'll need it for Colab)

### 4. Set Up Colab Secrets

1. **Open Google Colab:**
   - Go to https://colab.research.google.com
   - Create a new notebook OR open existing one

2. **Access Secrets:**
   - Click the key icon (🔑) in the left sidebar
   - This opens the "Secrets" panel

3. **Add GitHub Token:**
   - Click "+ Add new secret"
   - Name: `GITHUB_TOKEN`
   - Value: [paste your PAT from step 3]
   - Toggle "Notebook access" to **ON**
   - Click "Save"

4. **Verify secret:**
   - Secret should appear in the list
   - Notebook access should show "On"

### 5. Upload Sync Notebook to Drive

1. **Save notebook to Drive:**
   - Open `Drive_Mirror_Sync.ipynb` in Google Colab
   - File → Save a copy in Drive
   - Move to `/MyDrive/VCF-RESEARCH/` folder
   - Rename to `Drive_Mirror_Sync.ipynb`

**OR manually upload:**
   - Go to Google Drive
   - Navigate to `/MyDrive/VCF-RESEARCH/`
   - Click "New" → "File upload"
   - Select `Drive_Mirror_Sync.ipynb`

### 6. Test First Sync

1. **Open sync notebook:**
   - In Google Drive, navigate to `/MyDrive/VCF-RESEARCH/`
   - Open `Drive_Mirror_Sync.ipynb` in Colab

2. **Run the sync:**
   - Runtime → Run all
   - Authorize Drive access when prompted
   - Wait for completion

3. **Verify on GitHub:**
   - Go to https://github.com/rudder-research/drive_mirror
   - Check for new commit with timestamp
   - Review files - should match Drive contents

4. **Check commit message:**
   - Should show:
     - Sync timestamp
     - Number of files added/modified/deleted
     - Source path

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub repository `rudder-research/drive_mirror` exists
- [ ] Repository is private (if desired)
- [ ] README.md and .gitignore are in place
- [ ] Personal Access Token created and saved
- [ ] Token stored in Colab Secrets as `GITHUB_TOKEN`
- [ ] Notebook access enabled for secret
- [ ] Sync notebook uploaded to Drive
- [ ] First sync completed successfully
- [ ] Files visible on GitHub match Drive

## 🔧 Troubleshooting

### "Repository not found" error
- Verify repository name is exactly `drive_mirror`
- Check token has `repo` scope
- Ensure token hasn't expired

### "GITHUB_TOKEN not found" error
- Verify secret name is exactly `GITHUB_TOKEN` (case-sensitive)
- Check "Notebook access" is enabled
- Restart Colab runtime and try again

### "Drive folder not found" error
- Verify `/MyDrive/VCF-RESEARCH` exists
- Check folder name spelling (case-sensitive)
- Ensure Drive is mounted before running sync

### "Authentication failed" error
- Regenerate Personal Access Token
- Update token in Colab Secrets
- Verify token has correct scopes

### Sync takes too long
- Check folder size (large folders take longer)
- Consider excluding large files via .gitignore
- Verify internet connection

## 🔒 Security Best Practices

1. **Token Management:**
   - Store tokens only in Colab Secrets
   - Never commit tokens to git
   - Rotate tokens every 90 days
   - Revoke immediately if compromised

2. **Repository Access:**
   - Keep repository private for sensitive data
   - Limit collaborator access
   - Review commits for sensitive data

3. **Data Privacy:**
   - Review Drive contents before syncing
   - Check .gitignore excludes secrets
   - Never commit API keys or credentials

## 📚 Additional Resources

- [GitHub Token Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Colab Secrets Guide](https://colab.research.google.com/notebooks/secrets.ipynb)
- [Google Drive in Colab](https://colab.research.google.com/notebooks/io.ipynb)

## 🆘 Support

If issues persist:
1. Check error messages carefully
2. Review troubleshooting section above
3. Verify all steps were completed
4. Check GitHub and Colab documentation

## 📅 Maintenance Schedule

**Weekly:**
- [ ] Run sync notebook
- [ ] Review commit history

**Monthly:**
- [ ] Verify token hasn't expired
- [ ] Review repository size
- [ ] Update .gitignore if needed

**Quarterly:**
- [ ] Rotate GitHub PAT
- [ ] Review security settings
- [ ] Check for outdated files

---

**Setup Complete!** You're ready to maintain your Drive mirror.

*Last Updated: 2024-11-21*
