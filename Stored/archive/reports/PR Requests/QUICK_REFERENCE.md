# Drive Mirror - Quick Reference Card

## 🎯 Essential Info

**Repository:** `rudder-research/drive_mirror`  
**Source:** `/MyDrive/VCF-RESEARCH`  
**Direction:** Drive → GitHub (one-way)  
**Notebook:** `Drive_Mirror_Sync.ipynb`

## 🚀 Quick Start

```python
# 1. Open Colab notebook
# 2. Runtime → Run all
# 3. Authorize Drive when prompted
# 4. Wait ~1-5 minutes
# 5. Check GitHub for new commit
```

## ⚙️ Configuration

```python
GITHUB_USERNAME = "rudder-research"
GITHUB_REPO = "drive_mirror"
DRIVE_SOURCE_PATH = "/content/drive/MyDrive/VCF-RESEARCH"
```

## 🔑 Required Secret

**Colab Secret (🔑 icon):**
- Name: `GITHUB_TOKEN`
- Value: [Your GitHub PAT]
- Access: Notebook access ON

## 📋 Sync Checklist

- [ ] Token stored in Colab Secrets
- [ ] Drive folder exists
- [ ] Notebook uploaded to Drive
- [ ] Run "Runtime → Run all"
- [ ] Review commit on GitHub
- [ ] Check for sensitive data

## 🔍 Verification

```bash
# On GitHub
1. Check latest commit timestamp
2. Verify files match Drive
3. Review commit message

# In Colab
1. Check "✅ Sync successful" message
2. Review file counts
3. Check for errors
```

## ⚠️ Common Issues

| Error | Fix |
|-------|-----|
| Token not found | Add GITHUB_TOKEN to Colab Secrets |
| Drive folder not found | Check /MyDrive/VCF-RESEARCH exists |
| Auth failed | Regenerate GitHub PAT |
| Push failed | Check token scope (needs `repo`) |
| Sync slow | Check file sizes, internet connection |

## 🛡️ Security Reminders

- ✅ Store token only in Colab Secrets
- ✅ Keep repository private
- ✅ Review commits for sensitive data
- ✅ Rotate token every 90 days
- ❌ Never commit tokens to git
- ❌ Never share PAT with others

## 📊 What Gets Synced

**Included:**
- All files in VCF-RESEARCH folder
- Notebooks (.ipynb)
- Python code (.py)
- Data files (.csv, .json, .xlsx)
- Documentation (.md, .txt)

**Excluded (via .gitignore):**
- Cache files (__pycache__, .ipynb_checkpoints)
- Temporary files (~$*, .tmp)
- Large binaries (>100MB)
- System files (.DS_Store, Thumbs.db)
- Credentials (*.pem, *.key, .env)

## 🔄 Sync Frequency

**Recommended:**
- Weekly routine sync
- After major Drive updates
- Before important milestones

**Not recommended:**
- Multiple times per day
- During active editing
- For minor changes

## 📈 Monitoring

```python
# Check sync statistics
- Files in Drive: [shown in output]
- Files copied: [shown in output]
- Total changes: [shown in output]
- Commit SHA: [shown in output]
```

## 🔗 Important Links

**GitHub Repository:**
https://github.com/rudder-research/drive_mirror

**Token Settings:**
https://github.com/settings/tokens

**Colab Notebook:**
Open from /MyDrive/VCF-RESEARCH/Drive_Mirror_Sync.ipynb

## 🆘 Emergency Commands

**If sync fails completely:**
```python
# In Colab cell:
!rm -rf /content/drive_mirror
# Then re-run sync notebook
```

**If token compromised:**
1. Revoke token on GitHub immediately
2. Generate new token
3. Update Colab Secret
4. Re-run sync

**If wrong files committed:**
1. Don't panic
2. Review commit on GitHub
3. Use git revert if needed
4. Update .gitignore
5. Re-run sync

## 📞 Support

**Documentation:**
- README.md - Full guide
- SETUP_GUIDE.md - Initial setup
- ENHANCEMENTS.md - Advanced features

**Troubleshooting:**
See README.md "Troubleshooting" section

---

## ⏱️ Typical Sync Times

| Folder Size | Sync Time |
|-------------|-----------|
| <100 files | 1-2 min |
| 100-500 files | 2-5 min |
| 500-1000 files | 5-10 min |
| >1000 files | 10-15 min |

## 🎓 Best Practices

1. **Before syncing:**
   - Review Drive contents
   - Check for sensitive data
   - Verify no active editing

2. **During sync:**
   - Don't interrupt notebook
   - Don't modify Drive folder
   - Monitor progress output

3. **After sync:**
   - Review commit on GitHub
   - Check file counts match
   - Verify no sensitive data

4. **Regular maintenance:**
   - Update .gitignore as needed
   - Rotate token quarterly
   - Review repository size
   - Clean up old files

---

**Quick Reference v1.0** | Last Updated: 2024-11-21
