# Google Cloud & GitHub Deployment Guide

This guide provides exhaustive, step-by-step instructions to set up a 100% free, 24/7 cloud-hosted version of the Universal Second Brain Ingester using Google Cloud Platform (e2-micro free tier) and GitHub for storage synchronization.

## Step 1: Initialize the GitHub Storage Layer
Because the n8n bot will live on a Google server, it pushes notes to a private GitHub repository. Your local laptop will then pull them down automatically.

1. **Create the Vault Repo:** Log in to GitHub and create a new **Private** repository (e.g., `my-obsidian-vault`). Check the box to "Add a README file" so the repository is initialized.
2. **Generate the Fine-grained Token:**
   - On GitHub, click your profile picture (top right) -> **Settings** -> **Developer Settings** (bottom left) -> **Personal access tokens** -> **Fine-grained tokens**.
   - Click **Generate new token**. Name it `n8n-vault-sync`.
   - Set the expiration (up to 1 year max). *Note: You will need to rotate this key once a year.*
   - Under **Repository access**, select **Only select repositories**, and choose your new `my-obsidian-vault` repository.
   - Under **Permissions**, click **Repository permissions**. Scroll down the alphabetical list to **Contents**. Click the dropdown (which says "No access") and change it to **Read and write**. *(Leave all other permissions empty).*
   - Click Generate, and **copy the token**. Keep it secure.

## Step 2: Configure Obsidian (Your Local Laptop)
Your local Obsidian app needs to automatically download the notes that n8n pushes to GitHub.

1. Open Obsidian -> Settings -> **Community Plugins**. Turn off Safe Mode if prompted.
2. Search for and install **Obsidian Git**. Enable it.
3. Open the Obsidian command palette (Cmd+P or Ctrl+P) and search for `Git: Clone an existing remote repo`.
4. Paste your private repository URL (e.g., `https://github.com/your-username/my-obsidian-vault.git`).
5. When prompted for credentials, use your GitHub username, and paste your **Fine-grained Token** as the password.
6. When prompted for a directory, type a name for the folder where you want the notes to live (e.g., `Brainless_Sync`). Obsidian will create this folder and clone the repo into it.
7. Open the Obsidian Git plugin settings.
   - Look for a setting called **Base path** (or "Git repository path"). Type the name of the folder you just created (e.g., `Brainless_Sync`). Restart Obsidian so the plugin recognizes the subfolder as a valid Git repo.
   - Go back to Obsidian Git settings. Under the **Automatic** section:
     - Set **Auto commit-and-sync interval (minutes)** to `0` (This stops your laptop from pushing blank notes up to the cloud).
     - Set **Auto pull interval (minutes)** to `5`. *(Obsidian will now silently download new notes every 5 minutes).*

## Step 3: Create the Free Google Cloud Server (The Brain)
1. **Create the Free VM:**
   - Log in to the [Google Cloud Console](https://console.cloud.google.com). Go to **Compute Engine** -> **VM Instances** -> **Create Instance**.
   - **Region:** MUST be `us-central1`, `us-east1`, or `us-west1` (Required for free tier).
   - **Machine Type:** Select `e2-micro`.
   - **Boot Disk:** Change the OS to **Ubuntu 24.04 LTS** (Choose the standard version, **not** minimal). Ensure the architecture is **x86/64**. Change the disk type to **Standard Persistent Disk** (set size to 30GB). *Do not select Balanced or SSD, they are not free.*
   - **Firewall:** Check both "Allow HTTP traffic" and "Allow HTTPS traffic".
   - *Note on Pricing:* On the right sidebar, you will see a "Monthly estimate" of around $6 to $8. **Do not panic.** The Google Cloud UI shows the *gross* cost and does not calculate Free Tier discounts in this preview. The Always Free tier works by crediting you 100% of the cost on your monthly invoice, bringing the final bill to $0.00.
   - *Note on Networking Tier:* Leave the "Network Service Tier" set to **Premium** (which is the default). Counter-intuitively, the 1 GB of free monthly egress only applies to the Premium tier. If you switch to Standard, you will be billed from the very first byte.
   - *Note on Checkboxes:* 
     1. Uncheck **"Install Ops Agent for Monitoring and Logging"**. It consumes precious RAM/CPU on this tiny micro-server, and we don't need it.
     2. Under Data Protection / Backups, ensure **"Snapshot schedules"** is turned off. Snapshots are *not* free and will incur storage charges. Your data is backed up to GitHub anyway!
   - Click Create.
2. **Open the n8n UI Port:**
   - By default, Google blocks port `5678`. Go to **VPC Network** -> **Firewall**.
   - Click **Create Firewall Rule**.
   - Name: `allow-n8n`. 
   - Direction of traffic: **Ingress** (Incoming traffic).
   - Action on match: **Allow**.
   - Targets: `All instances in the network`. Source IPv4 ranges: `0.0.0.0/0`.
   - Protocols and ports: Check `TCP` and type `5678`. Save.
3. **Connect to the Server:**
   - Go back to VM Instances. Click the **SSH** button next to your new VM to open a browser terminal.

## Step 4: Deploying Your App on the VPS
Inside the Google Cloud SSH terminal, run these exact commands sequentially:

1. **Install Docker:**
   ```bash
   sudo apt update && sudo apt install docker.io docker-compose-plugin git -y
   sudo usermod -aG docker $USER
   newgrp docker
   ```
2. **Clone your project:**
   ```bash
   git clone -b branch_name https://github.com/vladveterok/brainless.git

   cd brainless
   ```
3. **Configure the Secrets (.env):**
   ```bash
   cp .env.example .env
   nano .env
   ```
   *Inside the nano text editor, navigate with your arrow keys and configure the secrets:*
   - `STORAGE_MODE=github`
   - `GITHUB_OWNER=your_github_username`
   - `GITHUB_REPO=my-obsidian-vault`
   - `GITHUB_TOKEN=your_fine_grained_token`
   - Set your `TELEGRAM_BOT_TOKEN` and `GEMINI_API_KEY`.
   *(Press Ctrl+X, then type Y, then press Enter to save and exit).*
4. **Start the Engine:**
   ```bash
   chmod +x ./scripts/setup_host.sh
   ./scripts/setup_host.sh
   ```

## Step 5: Final n8n Setup
1. Open a new tab in your browser and go to `http://<YOUR_GOOGLE_VM_EXTERNAL_IP>:5678`.
2. Set up the owner account (this secures your n8n instance).
3. In n8n, click **Add workflow** -> **...** (top right menu) -> **Import from File**. Select `workflows/main_workflow.json` from your laptop.
4. Double-click the **Telegram Trigger** node. 
5. Under "Credential for Telegram API", select **Create New Credential**. Name it "My Telegram Bot". Type `dummy` in the token field, save, and close. *(Because the `.env` variables are strictly whitelisted in Docker, n8n ignores this dummy text and seamlessly uses the real token in the background).*
6. Toggle the workflow to **Active** (top right corner).

Your bot is now 100% operational in the cloud, and your laptop will pull down any newly generated notes every 5 minutes.
