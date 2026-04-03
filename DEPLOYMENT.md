# Deployment Guide

This guide explains how to publish this project to GitHub and set up automated releases.

## Initial Setup

1. **Create a new repository on GitHub** (do not initialize it with README, .gitignore, or license)

2. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Scrcpy GUI project"
   ```

3. **Add GitHub remote** (replace YOUR_USERNAME with your GitHub username):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/scrcpy_gui.git
   ```

4. **Push to GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Important Notes

### Binary Files

Binary files (`adb`, `scrcpy`, `scrcpy-server`) are part of the application and are included in the repository. They are marked as binary in `.gitattributes` to ensure proper handling by Git.

### Automated Releases

The GitHub Actions workflow (`.github/workflows/release.yml`) is configured to automatically build and release the project when you push a commit with a version tag in the first line of the commit message.

**Commit message format:**
```
v1.3.0 - Description of changes
```

The workflow will:
1. Detect the version from the commit message (must start with `v` and contain dots, e.g., `v1.3.0`)
2. Build the DEB package
3. Create a Git tag automatically
4. Create a GitHub Release with the package attached

**Example workflow:**

```bash
# Make your changes
git add .
git commit -m "v1.3.0 - Added new feature and bug fixes"
git push origin main
```

After pushing, GitHub Actions will automatically:
- Build the DEB package
- Create tag `v1.3.0`
- Publish a release on GitHub

## Updating README

Before publishing, update the README.md to replace `YOUR_USERNAME` with your actual GitHub username:

```bash
sed -i 's/YOUR_USERNAME/your-github-username/g' README.md
```

## Verification

After pushing, verify:
1. All files are visible on GitHub
2. GitHub Actions workflow is present in the Actions tab
3. The repository displays the README correctly

## Future Releases

For subsequent releases, simply commit with a message starting with the version:

```bash
git commit -m "v1.4.0 - New feature"
git push origin main
```

The workflow will automatically handle the rest.

## Troubleshooting

If the workflow doesn't trigger:
1. Check that the commit message starts with `v` followed by version numbers (e.g., `v1.3.0`)
2. Ensure you're pushing to the `main` or `master` branch
3. Check the Actions tab for any error messages