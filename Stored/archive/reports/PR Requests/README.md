# Drive Mirror Repository

**Purpose:** 1:1 mirror of `/MyDrive/VCF-RESEARCH` for review and backup purposes only.

---

## 🎯 Purpose

This repository serves as a **read-only mirror** of the VCF-RESEARCH folder stored in Google Drive. It exists for:

- **Review & Collaboration** - Easy access to research materials via GitHub interface
- **Version Control** - Automated tracking of changes to Drive contents
- **Backup** - Secondary storage of research materials
- **Access Control** - Share specific snapshots without Drive permissions

## ⚠️ Important Constraints

**This is NOT a development repository:**
- ❌ Do not develop code here
- ❌ Do not create Pull Requests
- ❌ Do not manually commit changes
- ❌ Changes here will NOT sync back to Drive

**This IS for:**
- ✅ Reviewing current Drive contents
- ✅ Tracking history of Drive changes
- ✅ Sharing snapshots with collaborators
- ✅ Disaster recovery backup

---

## 🔄 How the Sync Works

### Sync Direction
```
Google Drive → GitHub
(One-way only)
```

### What Gets Synced

**Included:**
- All files in `/MyDrive/VCF-RESEARCH/`
- All subdirectories and their contents
- Jupyter notebooks (.ipynb)
- Data files (.csv, .xlsx, .json)
- Python code (.py)
- Documentation (.md, .txt)

**Excluded (via .gitignore):**
- Large binary files (>100MB)
- Temporary files (~$*, .tmp)
- Cache directories (__pycache__, .ipynb_checkpoints)
- System files (.DS_Store, Thumbs.db)
- Sensitive data (credentials, API keys)

### Sync Process

1. **Mount Google Drive** in Colab
2. **Authenticate GitHub** using Personal Access Token (PAT)
3. **Clone repository** (or use existing)
4. **Sync files** from Drive to local repo
5. **Detect changes** (new, modified, deleted files)
6. **Commit & Push** if changes exist
7. **Clean up** temporary files

### Sync Frequency

- **Manual trigger** - Run the Colab notebook when needed
- **Recommended** - Weekly or after major Drive updates
- **Automated** (optional) - Set up with GitHub Actions + Google Cloud

---

## 🚀 How to Use

### Initial Setup

1. **Create Personal Access Token (PAT)**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Name: `drive_mirror_sync`
   - Scopes: Select `repo` (full control of private repositories)
   - Generate and copy the token

2. **Store PAT in Colab Secrets**
   - Open Google Colab
   - Click the key icon (🔑) in left sidebar
   - Add new secret:
     - Name: `GITHUB_TOKEN`
     - Value: [paste your PAT]
   - Enable "Notebook access"

3. **Open Sync Notebook**
   - Open `Drive_Mirror_Sync.ipynb` in Google Colab
   - File is located in `/MyDrive/VCF-RESEARCH/` (or save it there)

### Running a Sync

1. Open the sync notebook in Colab
2. Run all cells (Runtime → Run all)
3. Authorize Google Drive access when prompted
4. Wait for sync to complete (~1-5 minutes)
5. Check GitHub repository for updates

### Verification

After sync completes, verify:
- ✅ Commit message shows timestamp
- ✅ Files match what's in Drive
- ✅ No sensitive data committed
- ✅ .gitignore is respected

---

## 📁 Repository Structure

This repository mirrors the Drive structure exactly:

```
drive_mirror/
├── README.md              # This file
├── .gitignore             # Sync exclusions
├── Drive_Mirror_Sync.ipynb # Sync notebook (stored in Drive)
│
└── [Mirrored Drive Contents]
    ├── data/              # Data files from Drive
    ├── notebooks/         # Jupyter notebooks
    ├── scripts/           # Python scripts
    ├── docs/              # Documentation
    └── ...                # Other folders from Drive
```

---

## 🔒 Security & Best Practices

### API Keys & Credentials

**NEVER commit:**
- API keys (FRED, Yahoo Finance, etc.)
- Passwords or tokens
- Database credentials
- `.env` files with secrets

**Protection mechanisms:**
1. `.gitignore` blocks common secret files
2. Manual review before each sync
3. GitHub secret scanning alerts

### Personal Access Token (PAT)

**Security:**
- Store ONLY in Colab Secrets (never in notebook)
- Use fine-grained tokens when possible
- Rotate tokens every 90 days
- Revoke immediately if compromised

**Access:**
- Notebook-level access only
- Not shared across Colab accounts
- Automatically cleared when session ends

### Data Privacy

**Before syncing:**
- Review Drive contents for PII (Personally Identifiable Information)
- Check for proprietary/confidential data
- Verify file sizes (GitHub has 100MB file limit)

**If private data exists:**
- Keep repository private
- Limit collaborator access
- Consider using Git LFS for large files

---

## 🛠️ Troubleshooting

### Common Issues

**"Authentication failed"**
- Check PAT is stored in Colab Secrets as `GITHUB_TOKEN`
- Verify PAT has `repo` scope
- Ensure PAT hasn't expired
- Regenerate PAT if needed

**"Drive folder not found"**
- Verify `/MyDrive/VCF-RESEARCH` exists in your Drive
- Check folder name spelling (case-sensitive)
- Ensure Drive is properly mounted

**"File too large"**
- GitHub rejects files >100MB
- Move large files to Git LFS or exclude via .gitignore
- Consider splitting large datasets

**"Nothing to commit"**
- No changes detected since last sync
- This is normal if Drive hasn't changed
- Verify Drive folder contains files

**"Sync taking too long"**
- Large folders may take 5-10 minutes
- Check internet connection
- Consider excluding large binary files

### Manual Recovery

If sync fails completely:

```bash
# Delete local clone
rm -rf /content/drive_mirror

# Re-run sync notebook
# Fresh clone will be created
```

---

## 📊 Sync Statistics

Track sync performance:
- **Files synced**: Visible in commit message
- **Last sync**: Check latest commit timestamp
- **Sync frequency**: Review commit history
- **Data size**: Check repository size on GitHub

---

## 🔮 Advanced Usage

### Automated Sync (Optional)

For fully automated syncing, consider:

1. **GitHub Actions + Google Cloud**
   - Deploy notebook to Cloud Function
   - Trigger via GitHub Actions schedule
   - Requires service account setup

2. **Colab Pro + Scheduling**
   - Use Colab Pro background execution
   - Schedule via cron or external trigger
   - Limited to Pro/Pro+ subscribers

3. **Local Sync Script**
   - Clone Drive folder locally
   - Run sync script via cron
   - Requires local Google Drive setup

### Branch Strategy

**Default:** All syncs go to `main` branch

**Alternative:** Create dated branches
```python
# Modify sync script to use:
branch_name = f"sync-{datetime.now().strftime('%Y-%m-%d')}"
```

### Selective Sync

To sync only specific folders:

1. Edit `DRIVE_SOURCE_PATH` in notebook
2. Point to subfolder: `/MyDrive/VCF-RESEARCH/notebooks`
3. Run sync as normal

---

## 🤝 Contributing

**This repository does not accept contributions** as it's an automated mirror.

For research contributions, use the main VCF-RESEARCH repository.

---

## 📝 Maintenance

### Regular Tasks

- [ ] **Weekly:** Run sync notebook
- [ ] **Monthly:** Review commit history
- [ ] **Quarterly:** Rotate GitHub PAT
- [ ] **As needed:** Update .gitignore for new file types

### Monitoring

Watch for:
- Unexpected file deletions
- Large file additions (>10MB)
- Sensitive data commits
- Sync failures

---

## 📞 Support

**Issues with sync process:**
- Check Troubleshooting section above
- Review Colab notebook cell outputs
- Verify Drive and GitHub permissions

**Issues with VCF Research:**
- Use main VCF-RESEARCH repository
- Contact: Jason Rudder

---

## 📜 License

This mirror repository follows the same license as the source VCF-RESEARCH project.

---

## 🏷️ Metadata

- **Repository:** `rudder-research/drive_mirror`
- **Source:** `/MyDrive/VCF-RESEARCH`
- **Sync Direction:** Drive → GitHub (one-way)
- **Automation:** Manual (Colab notebook)
- **Access:** Private
- **Last Updated:** 2024-11-21

---

**Remember:** This is a MIRROR, not a working repository. All development happens in Drive and main VCF repos.
