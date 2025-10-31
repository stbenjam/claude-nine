#!/bin/bash
set -e

echo "🚀 Claude Marketplace Template Setup"
echo "===================================="
echo ""

# Function to prompt for input with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local result

    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " result
        echo "${result:-$default}"
    else
        read -p "$prompt: " result
        echo "$result"
    fi
}

# Get marketplace configuration
echo "Let's configure your marketplace!"
echo ""

MARKETPLACE_NAME=$(prompt_with_default "Marketplace name (e.g., 'my-plugins', 'claude-nine')" "")
while [ -z "$MARKETPLACE_NAME" ]; do
    echo "Error: Marketplace name is required"
    MARKETPLACE_NAME=$(prompt_with_default "Marketplace name" "")
done

OWNER_NAME=$(prompt_with_default "Owner name (e.g., GitHub username)" "")
while [ -z "$OWNER_NAME" ]; do
    echo "Error: Owner name is required"
    OWNER_NAME=$(prompt_with_default "Owner name" "")
done

GITHUB_REPO=$(prompt_with_default "GitHub repository (e.g., 'username/repo-name')" "$OWNER_NAME/$MARKETPLACE_NAME")

echo ""
echo "Color scheme options:"
echo "  1) forest-green (default)"
echo "  2) ocean-blue"
echo "  3) sunset-orange"
echo "  4) royal-purple"
echo "  5) crimson-red"
echo "  6) custom"
echo ""

COLOR_CHOICE=$(prompt_with_default "Choose a color scheme" "1")

case $COLOR_CHOICE in
    1)
        PRIMARY_COLOR="#228B22"
        PRIMARY_DARK="#1a6b1a"
        SECONDARY_COLOR="#32CD32"
        ;;
    2)
        PRIMARY_COLOR="#0077be"
        PRIMARY_DARK="#005a8e"
        SECONDARY_COLOR="#4db8ff"
        ;;
    3)
        PRIMARY_COLOR="#ff6b35"
        PRIMARY_DARK="#d94f1f"
        SECONDARY_COLOR="#ff9966"
        ;;
    4)
        PRIMARY_COLOR="#6a4c93"
        PRIMARY_DARK="#4a3369"
        SECONDARY_COLOR="#9d84b7"
        ;;
    5)
        PRIMARY_COLOR="#dc143c"
        PRIMARY_DARK="#a0102a"
        SECONDARY_COLOR="#ff6b7a"
        ;;
    6)
        PRIMARY_COLOR=$(prompt_with_default "Primary color (hex)" "#6366f1")
        PRIMARY_DARK=$(prompt_with_default "Primary dark color (hex)" "#4f46e5")
        SECONDARY_COLOR=$(prompt_with_default "Secondary color (hex)" "#818cf8")
        ;;
    *)
        PRIMARY_COLOR="#228B22"
        PRIMARY_DARK="#1a6b1a"
        SECONDARY_COLOR="#32CD32"
        ;;
esac

echo ""
echo "Keep example plugin? (You can delete it later)"
KEEP_EXAMPLE=$(prompt_with_default "Keep example plugin? (y/n)" "y")

echo ""
echo "📝 Creating configuration..."

# Create config file
cat > .template-config.json << EOF
{
  "template_version": "1.0.0",
  "marketplace_name": "$MARKETPLACE_NAME",
  "owner_name": "$OWNER_NAME",
  "github_repo": "$GITHUB_REPO",
  "color_scheme": {
    "primary": "$PRIMARY_COLOR",
    "primary_dark": "$PRIMARY_DARK",
    "secondary": "$SECONDARY_COLOR"
  }
}
EOF

# Create marketplace.json from template (overwrite if exists)
cp .claude-plugin/marketplace.json.template .claude-plugin/marketplace.json

# Create README.md from template (overwrite if exists)
cp README.md.template README.md

echo "✓ Configuration created"

# Apply branding
echo ""
echo "🎨 Applying branding..."
python3 scripts/apply-branding.py

# Generate documentation
echo ""
echo "📚 Generating documentation..."
make update

# Remove example plugin if requested
if [[ "$KEEP_EXAMPLE" != "y" && "$KEEP_EXAMPLE" != "Y" ]]; then
    echo ""
    echo "🗑️  Removing example plugin..."
    rm -rf plugins/example-plugin

    # Update marketplace.json to remove example plugin
    python3 -c "
import json
with open('.claude-plugin/marketplace.json', 'r') as f:
    data = json.load(f)
data['plugins'] = []
with open('.claude-plugin/marketplace.json', 'w') as f:
    json.dump(data, f, indent=2)
"

    # Update settings.json to remove example plugin
    python3 -c "
import json
with open('.claude-plugin/settings.json', 'r') as f:
    data = json.load(f)
data['installedPlugins'] = []
with open('.claude-plugin/settings.json', 'w') as f:
    json.dump(data, f, indent=2)
"
    echo "✓ Example plugin removed"
fi

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo ""
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Create plugins with: make new-plugin NAME=my-plugin"
echo "  2. Run linter with: make lint"
echo "  3. Generate docs with: make update"
echo "  4. Push to GitHub: git remote add origin git@github.com:$GITHUB_REPO.git"
echo ""
echo "📚 Documentation: https://docs.claude.com/en/docs/claude-code/plugins"
echo ""

# Ask if we should delete setup.sh
echo "Delete this setup script? (Recommended after setup is complete)"
DELETE_SETUP=$(prompt_with_default "Delete setup.sh? (y/n)" "y")

if [[ "$DELETE_SETUP" == "y" || "$DELETE_SETUP" == "Y" ]]; then
    echo ""
    echo "🗑️  Removing setup.sh..."
    rm -- "$0"
    echo "✓ Setup script removed"
fi
