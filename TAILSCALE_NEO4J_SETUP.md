# Tailscale + Neo4j Setup Guide

**Secure private network for sharing your Neo4j knowledge graph across all devices**

## Overview

This guide sets up Tailscale (secure VPN) to share your Neo4j database privately across all your Claude Code instances without exposing it to the internet.

**Architecture:**
- **Primary device** (Mac mini): Runs Neo4j, accessible via Tailscale IP
- **Secondary devices** (laptops, work machines): Connect to primary via Tailscale
- **Security**: Encrypted WireGuard VPN, zero-config NAT traversal

---

## Prerequisites

- One device designated as **primary** (always-on recommended, e.g., Mac mini)
- Neo4j installed on primary device
- Admin access on all devices

---

## Part 1: Install Tailscale on All Devices

### Mac/Linux

```bash
# Mac (Homebrew)
brew install tailscale

# Start Tailscale
sudo tailscale up

# Follow authentication prompts in browser
```

### Windows

```powershell
# Download installer from https://tailscale.com/download/windows
# Or use winget:
winget install tailscale.tailscale

# Start Tailscale from system tray
```

### Verify Installation

```bash
# Check Tailscale status
tailscale status

# Get your Tailscale IP (100.x.x.x)
tailscale ip -4
```

**Record each device's Tailscale IP:**
- Mac mini (primary): `100.x.x.x`
- Laptop 1: `100.y.y.y`
- Laptop 2: `100.z.z.z`

---

## Part 2: Configure Neo4j on Primary Device

### Step 1: Find Neo4j Configuration File

```bash
# Homebrew install (Mac)
/opt/homebrew/etc/neo4j/neo4j.conf

# APT install (Linux)
/etc/neo4j/neo4j.conf

# Neo4j Desktop
# Open Neo4j Desktop → Your Database → Settings → neo4j.conf
```

### Step 2: Edit neo4j.conf

**Option A: Listen on all interfaces (easier)**

```bash
# Open config file
nano /opt/homebrew/etc/neo4j/neo4j.conf

# Find and uncomment/modify this line:
server.default_listen_address=0.0.0.0

# Also set the bolt connector address:
server.bolt.listen_address=0.0.0.0:7687
```

**Option B: Listen only on Tailscale IP (more secure)**

```bash
# Get your primary device's Tailscale IP
TAILSCALE_IP=$(tailscale ip -4)
echo "Tailscale IP: $TAILSCALE_IP"

# Edit config with your specific IP
server.default_listen_address=100.x.x.x  # Replace with YOUR Tailscale IP
server.bolt.listen_address=100.x.x.x:7687
```

**Important security settings (add these):**

```conf
# Require authentication
dbms.security.auth_enabled=true

# Set a strong password if not already set
# (Run neo4j-admin set-initial-password <password>)
```

### Step 3: Restart Neo4j

```bash
# Homebrew (Mac)
brew services restart neo4j

# Systemd (Linux)
sudo systemctl restart neo4j

# Neo4j Desktop
# Stop and Start the database in Neo4j Desktop
```

### Step 4: Test Local Connection

```bash
# From primary device, verify Neo4j is accessible
curl http://localhost:7474

# Should return Neo4j browser page
```

### Step 5: Set Neo4j Password (if not done)

```bash
# Set initial password
neo4j-admin set-initial-password YourSecurePassword123

# Or change existing password via Neo4j Browser:
# Open http://localhost:7474
# Login with current password
# Run: ALTER CURRENT USER SET PASSWORD FROM 'old' TO 'new'
```

---

## Part 3: Configure .claude.json on All Devices

### Primary Device Configuration

**File**: `~/.claude/.claude.json`

```json
{
  "mcpServers": {
    "memento-dev": {
      "command": "npx",
      "args": ["-y", "@joshuarileydev/memento-mcp-server"],
      "env": {
        "NEO4J_URI": "neo4j://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "YourSecurePassword123",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

### Secondary Devices Configuration

**File**: `~/.claude/.claude.json`

Replace `localhost` with **primary device's Tailscale IP**:

```json
{
  "mcpServers": {
    "memento-dev": {
      "command": "npx",
      "args": ["-y", "@joshuarileydev/memento-mcp-server"],
      "env": {
        "NEO4J_URI": "neo4j://100.x.x.x:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "YourSecurePassword123",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

**Replace**:
- `100.x.x.x` → Your primary device's Tailscale IP
- `YourSecurePassword123` → Your actual Neo4j password

---

## Part 4: Test Multi-Device Connection

### From Secondary Device

```bash
# 1. Verify Tailscale connectivity
ping 100.x.x.x  # Primary device's Tailscale IP

# 2. Test Neo4j connection
curl http://100.x.x.x:7474

# Should return Neo4j browser page
```

### Test via Claude Code

```bash
# On secondary device, open Claude Code and test:
# Use any memento-dev command
```

Example test:
```bash
# Create a test entity
mcp__memento-dev__create_entities with:
{
  "name": "Tailscale Test",
  "entityType": "test",
  "observations": ["Testing from secondary device via Tailscale"]
}

# If successful, you're connected!
```

---

## Part 5: Security Best Practices

### 1. Use Tailscale ACLs (Access Control Lists)

```json
// In Tailscale Admin Console (https://login.tailscale.com/admin/acls)
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:members"],
      "dst": ["100.x.x.x:7687"]  // Your primary device Neo4j port
    }
  ]
}
```

### 2. Store Credentials Securely

**Don't commit passwords to Git!**

Create a local `.env` file:

```bash
# On each device
cat > ~/.claude/.env.neo4j << 'EOF'
NEO4J_URI=neo4j://100.x.x.x:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=YourSecurePassword123
NEO4J_DATABASE=neo4j
EOF

chmod 600 ~/.claude/.env.neo4j
```

**Reference in `.claude.json`:**

```json
{
  "mcpServers": {
    "memento-dev": {
      "command": "npx",
      "args": ["-y", "@joshuarileydev/memento-mcp-server"],
      "env": {
        "NEO4J_URI": "${NEO4J_URI}",
        "NEO4J_USERNAME": "${NEO4J_USERNAME}",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "NEO4J_DATABASE": "${NEO4J_DATABASE}"
      }
    }
  }
}
```

**Note**: If MCP doesn't support env var expansion, use the helper script (Part 6).

### 3. Enable Tailscale Key Expiry

```bash
# Set devices to require periodic re-authentication (recommended)
# In Tailscale Admin Console → Settings → Key Expiry
```

---

## Part 6: Automation Scripts

### Helper Script: tailscale-neo4j-setup.sh

```bash
#!/bin/bash
# Tailscale + Neo4j Setup Helper
# Location: ~/Claude_Code/Claude_Global_Config/tools/tailscale-neo4j-setup.sh

echo "========================================"
echo "Tailscale + Neo4j Setup Helper"
echo "========================================"
echo ""

# Check if Tailscale is installed
if ! command -v tailscale &> /dev/null; then
    echo "❌ Tailscale not installed"
    echo "Install: brew install tailscale"
    exit 1
fi

# Check if Tailscale is running
if ! tailscale status &> /dev/null; then
    echo "❌ Tailscale not running"
    echo "Start: sudo tailscale up"
    exit 1
fi

# Get Tailscale IP
TAILSCALE_IP=$(tailscale ip -4)
echo "✅ This device's Tailscale IP: $TAILSCALE_IP"
echo ""

# Determine if this is primary device
echo "Is this your PRIMARY device (where Neo4j runs)? [y/N]"
read -r IS_PRIMARY

if [[ $IS_PRIMARY =~ ^[Yy]$ ]]; then
    echo ""
    echo "PRIMARY DEVICE SETUP"
    echo "===================="
    echo ""
    echo "1. Configure Neo4j to listen on Tailscale:"
    echo "   Edit: /opt/homebrew/etc/neo4j/neo4j.conf"
    echo "   Add:  server.default_listen_address=$TAILSCALE_IP"
    echo ""
    echo "2. Restart Neo4j:"
    echo "   brew services restart neo4j"
    echo ""
    echo "3. Your Neo4j URI for other devices:"
    echo "   neo4j://$TAILSCALE_IP:7687"
    echo ""
else
    echo ""
    echo "SECONDARY DEVICE SETUP"
    echo "======================"
    echo ""
    echo "Enter PRIMARY device's Tailscale IP (100.x.x.x):"
    read -r PRIMARY_IP

    echo ""
    echo "Testing connection to primary device..."
    if ping -c 1 "$PRIMARY_IP" &> /dev/null; then
        echo "✅ Primary device reachable via Tailscale"
    else
        echo "❌ Cannot reach primary device"
        echo "   Ensure Tailscale is running on both devices"
        exit 1
    fi

    echo ""
    echo "Testing Neo4j connection..."
    if curl -s "http://$PRIMARY_IP:7474" > /dev/null; then
        echo "✅ Neo4j accessible on primary device"
    else
        echo "❌ Neo4j not accessible"
        echo "   Ensure Neo4j is configured to listen on Tailscale IP"
        exit 1
    fi

    echo ""
    echo "✅ Ready to configure Claude Code!"
    echo ""
    echo "Update ~/.claude/.claude.json with:"
    echo "  NEO4J_URI=neo4j://$PRIMARY_IP:7687"
fi
```

---

## Troubleshooting

### Issue: Cannot connect from secondary device

**Check 1: Tailscale connectivity**
```bash
ping 100.x.x.x  # Primary's Tailscale IP
```

**Check 2: Neo4j listening on Tailscale interface**
```bash
# On primary device
netstat -an | grep 7687
# Should show: 100.x.x.x:7687 or 0.0.0.0:7687
```

**Check 3: Firewall**
```bash
# Mac: System Preferences → Security & Privacy → Firewall
# Allow Neo4j or disable firewall temporarily for testing
```

### Issue: "Authentication failed"

**Solution**: Verify password is correct
```bash
# On primary device, reset password:
neo4j-admin set-initial-password NewPassword123
```

### Issue: Tailscale IP changes

**Solution**: Tailscale IPs are stable but can change if device is removed/re-added
```bash
# Check current IP
tailscale ip -4

# Update .claude.json on all devices if it changed
```

### Issue: Primary device offline

**Limitation**: Secondary devices cannot access Neo4j when primary is offline.

**Solutions**:
- Use always-on device as primary (Mac mini ideal)
- Consider Neo4j Aura for always-available cloud option
- Use local-only Neo4j on each device (no sharing)

---

## Maintenance

### Updating Primary Device IP

If your primary device's Tailscale IP changes:

```bash
# 1. Get new IP on primary
tailscale ip -4

# 2. Update Neo4j config (if using specific IP)
nano /opt/homebrew/etc/neo4j/neo4j.conf

# 3. Restart Neo4j
brew services restart neo4j

# 4. Update .claude.json on ALL secondary devices
```

### Backing Up Neo4j

```bash
# Create backup
neo4j-admin database dump neo4j --to-path=/path/to/backup

# Restore backup
neo4j-admin database load neo4j --from-path=/path/to/backup
```

---

## Summary

**What you have now:**
- ✅ Private Neo4j knowledge graph shared across all devices
- ✅ Encrypted Tailscale VPN (no exposed ports)
- ✅ Data stays on your devices (complete privacy)
- ✅ Works across different networks (home, work, travel)

**Quick setup for new device:**
1. Install Tailscale: `brew install tailscale && sudo tailscale up`
2. Get primary IP: `tailscale ip -4` (on primary device)
3. Update `.claude.json` with primary's Tailscale IP
4. Test connection with Claude Code

**Need help?** Check troubleshooting section or create GitHub issue.
