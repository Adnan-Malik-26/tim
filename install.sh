#!/usr/bin/env bash
set -e

# Colors
GREEN="\\033[0;32m"
YELLOW="\\033[1;33m"
RESET="\\033[0m"

echo -e "${YELLOW}Installing tim...${RESET}"

# Ensure ~/.local/bin exists
mkdir -p ~/.local/bin

# Check if python-rich is installed
if ! python -c "import rich" &>/dev/null; then
  echo -e "${YELLOW}Installing python-rich...${RESET}"
  pip install --user rich
else
  echo -e "${GREEN}rich already installed${RESET}"
fi

# Make script executable
chmod +x tim.py

# Copy to ~/.local/bin/tim
cp tim.py ~/.local/bin/tim

echo -e "${GREEN}Done!${RESET}"
echo "Now you can run: tim start | tim stop | tim graph"
