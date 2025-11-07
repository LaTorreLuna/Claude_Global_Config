#!/bin/bash
# Tailscale + Neo4j Setup Helper
# Automates Tailscale + Neo4j configuration for multi-device knowledge graph sharing

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "Tailscale + Neo4j Setup Helper"
echo "========================================"
echo ""

# ============================================
# STEP 1: Check Tailscale Installation
# ============================================

if ! command -v tailscale &> /dev/null; then
    echo -e "${RED}❌ Tailscale not installed${NC}"
    echo ""
    echo "Install Tailscale:"
    echo "  Mac:     brew install tailscale"
    echo "  Linux:   curl -fsSL https://tailscale.com/install.sh | sh"
    echo "  Windows: https://tailscale.com/download/windows"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Tailscale installed${NC}"

# ============================================
# STEP 2: Check Tailscale Status
# ============================================

if ! tailscale status &> /dev/null; then
    echo -e "${RED}❌ Tailscale not running${NC}"
    echo ""
    echo "Start Tailscale:"
    echo "  sudo tailscale up"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo -e "${GREEN}✅ Tailscale running${NC}"

# Get Tailscale IP
TAILSCALE_IP=$(tailscale ip -4)
echo -e "${BLUE}📍 This device's Tailscale IP: $TAILSCALE_IP${NC}"
echo ""

# ============================================
# STEP 3: Determine Device Role
# ============================================

echo "Is this your PRIMARY device (where Neo4j runs)?"
echo "  - PRIMARY: Mac mini or always-on device with Neo4j installed"
echo "  - SECONDARY: Laptop or device that connects to primary"
echo ""
read -p "Is this PRIMARY? [y/N] " -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # ============================================
    # PRIMARY DEVICE SETUP
    # ============================================

    echo "========================================"
    echo "PRIMARY DEVICE SETUP"
    echo "========================================"
    echo ""

    # Check if Neo4j is installed
    NEO4J_CONF=""
    if [ -f "/opt/homebrew/etc/neo4j/neo4j.conf" ]; then
        NEO4J_CONF="/opt/homebrew/etc/neo4j/neo4j.conf"
    elif [ -f "/etc/neo4j/neo4j.conf" ]; then
        NEO4J_CONF="/etc/neo4j/neo4j.conf"
    elif [ -f "/usr/local/etc/neo4j/neo4j.conf" ]; then
        NEO4J_CONF="/usr/local/etc/neo4j/neo4j.conf"
    fi

    if [ -z "$NEO4J_CONF" ]; then
        echo -e "${RED}❌ Neo4j config not found${NC}"
        echo ""
        echo "Install Neo4j:"
        echo "  Mac:   brew install neo4j"
        echo "  Linux: apt install neo4j (or download from neo4j.com)"
        echo ""
        exit 1
    fi

    echo -e "${GREEN}✅ Neo4j config found: $NEO4J_CONF${NC}"
    echo ""

    # Check current listen address
    CURRENT_LISTEN=$(grep "^server.default_listen_address" "$NEO4J_CONF" 2>/dev/null || echo "")

    if [ -n "$CURRENT_LISTEN" ]; then
        echo "Current Neo4j listen address:"
        echo "  $CURRENT_LISTEN"
        echo ""
    fi

    echo "Choose Neo4j listen configuration:"
    echo "  [1] Listen on all interfaces (0.0.0.0) - Easier"
    echo "  [2] Listen only on Tailscale IP ($TAILSCALE_IP) - More secure"
    echo ""
    read -p "Choice [1/2]: " -r LISTEN_CHOICE
    echo ""

    if [ "$LISTEN_CHOICE" = "2" ]; then
        LISTEN_ADDR="$TAILSCALE_IP"
    else
        LISTEN_ADDR="0.0.0.0"
    fi

    echo -e "${YELLOW}⚠️  This will modify Neo4j configuration${NC}"
    echo "File: $NEO4J_CONF"
    echo "New listen address: $LISTEN_ADDR"
    echo ""
    read -p "Proceed? [y/N] " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi

    # Backup config
    sudo cp "$NEO4J_CONF" "${NEO4J_CONF}.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${GREEN}✅ Config backed up${NC}"

    # Update config
    if grep -q "^server.default_listen_address" "$NEO4J_CONF"; then
        sudo sed -i.tmp "s/^server.default_listen_address=.*/server.default_listen_address=$LISTEN_ADDR/" "$NEO4J_CONF"
    else
        echo "server.default_listen_address=$LISTEN_ADDR" | sudo tee -a "$NEO4J_CONF" > /dev/null
    fi

    if grep -q "^server.bolt.listen_address" "$NEO4J_CONF"; then
        sudo sed -i.tmp "s/^server.bolt.listen_address=.*/server.bolt.listen_address=$LISTEN_ADDR:7687/" "$NEO4J_CONF"
    else
        echo "server.bolt.listen_address=$LISTEN_ADDR:7687" | sudo tee -a "$NEO4J_CONF" > /dev/null
    fi

    echo -e "${GREEN}✅ Neo4j config updated${NC}"
    echo ""

    # Restart Neo4j
    echo "Restarting Neo4j..."
    if command -v brew &> /dev/null; then
        brew services restart neo4j
    elif command -v systemctl &> /dev/null; then
        sudo systemctl restart neo4j
    else
        echo -e "${YELLOW}⚠️  Please restart Neo4j manually${NC}"
    fi

    echo ""
    echo "========================================"
    echo -e "${GREEN}✅ PRIMARY SETUP COMPLETE${NC}"
    echo "========================================"
    echo ""
    echo "Your Neo4j is now accessible via Tailscale!"
    echo ""
    echo "Connection details for OTHER devices:"
    echo "  NEO4J_URI: neo4j://$TAILSCALE_IP:7687"
    echo ""
    echo "Save these for secondary device setup."
    echo ""
    echo "Your .claude.json on THIS device should use:"
    echo "  NEO4J_URI: neo4j://localhost:7687"
    echo ""

else
    # ============================================
    # SECONDARY DEVICE SETUP
    # ============================================

    echo "========================================"
    echo "SECONDARY DEVICE SETUP"
    echo "========================================"
    echo ""

    read -p "Enter PRIMARY device's Tailscale IP (100.x.x.x): " PRIMARY_IP
    echo ""

    # Validate IP format
    if [[ ! $PRIMARY_IP =~ ^100\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo -e "${RED}❌ Invalid Tailscale IP format${NC}"
        echo "Expected: 100.x.x.x"
        exit 1
    fi

    # Test Tailscale connectivity
    echo "Testing Tailscale connection to primary..."
    if ping -c 1 -W 2 "$PRIMARY_IP" &> /dev/null; then
        echo -e "${GREEN}✅ Primary device reachable via Tailscale${NC}"
    else
        echo -e "${RED}❌ Cannot reach primary device${NC}"
        echo ""
        echo "Troubleshooting:"
        echo "  1. Ensure Tailscale is running on primary device"
        echo "  2. Verify primary IP: tailscale ip -4 (on primary)"
        echo "  3. Check Tailscale status: tailscale status"
        exit 1
    fi

    # Test Neo4j connectivity
    echo "Testing Neo4j connection..."
    if curl -s -m 5 "http://$PRIMARY_IP:7474" > /dev/null; then
        echo -e "${GREEN}✅ Neo4j accessible on primary device${NC}"
    else
        echo -e "${RED}❌ Neo4j not accessible${NC}"
        echo ""
        echo "Troubleshooting:"
        echo "  1. Ensure Neo4j is running on primary"
        echo "  2. Verify Neo4j config: server.default_listen_address"
        echo "  3. Check firewall settings on primary"
        exit 1
    fi

    echo ""
    echo "========================================"
    echo -e "${GREEN}✅ CONNECTION VERIFIED${NC}"
    echo "========================================"
    echo ""
    echo "Update ~/.claude/.claude.json with:"
    echo ""
    echo '  "memento-dev": {'
    echo '    "command": "npx",'
    echo '    "args": ["-y", "@joshuarileydev/memento-mcp-server"],'
    echo '    "env": {'
    echo "      \"NEO4J_URI\": \"neo4j://$PRIMARY_IP:7687\","
    echo '      "NEO4J_USERNAME": "neo4j",'
    echo '      "NEO4J_PASSWORD": "YourNeo4jPassword",'
    echo '      "NEO4J_DATABASE": "neo4j"'
    echo '    }'
    echo '  }'
    echo ""
    echo "Then restart Claude Code to apply changes."
    echo ""
fi

echo "For full documentation, see:"
echo "  ~/Claude_Code/Claude_Global_Config/TAILSCALE_NEO4J_SETUP.md"
