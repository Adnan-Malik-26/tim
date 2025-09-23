# 🕒 Tim - Beautiful Terminal Time Tracker

A minimalist, aesthetically pleasing time tracking CLI tool built with Rich and the Catppuccin color scheme. Track your time, visualize your productivity, and maintain streaks with style.

![GitHub Style Contributions Graph](https://img.shields.io/badge/features-github%20style%20graph-brightgreen)
![Catppuccin Theme](https://img.shields.io/badge/theme-catppuccin-pink)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## ✨ Features

- 🏷️ **Tag-based tracking** - Organize your time with custom tags
- ⏱️ **Session management** - Start, stop, and track work sessions
- 📊 **GitHub-style contributions graph** - Visualize your activity over time
- 🔥 **Streak tracking** - Monitor consistency across different activities
- 📈 **Detailed summaries** - View comprehensive session reports
- 🎨 **Beautiful terminal UI** - Powered by Rich with Catppuccin colors
- 🗃️ **Local SQLite storage** - Your data stays on your machine

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### From PyPI (Recommended)

```bash
pip install tim-tracker
```

### From Source

```bash
git clone https://github.com/Adnan-Malik-26/tim.git
cd tim
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/Adnan-Malik-26/tim.git
cd tim
pip install -e ".[dev]"
```

## 📖 Usage

### Quick Start

```bash
# Add your first tag
tim add-tag "Python Study"

# Start tracking time
tim start

# Stop the current session
tim stop

# View your contributions graph
tim graph

# See all your sessions
tim summary

# Check your streaks
tim streak

# List all tags
tim tags
```

### Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add-tag <name>` | Create a new tag | `tim add-tag "Reading"` |
| `tags` | List all available tags | `tim tags` |
| `start` | Start a new session | `tim start` |
| `stop` | Stop the current session | `tim stop` |
| `summary` | Show all sessions | `tim summary` |
| `streak` | Display streak information | `tim streak` |
| `graph [--weeks N]` | Show contributions graph | `tim graph --weeks 26` |

### Advanced Usage

#### Viewing Different Time Ranges

```bash
# Show last 26 weeks
tim graph --weeks 26

# Show last 12 weeks
tim graph -w 12
```

#### Session Management

The tool supports one active session at a time. Starting a new session will not affect any running sessions - you need to explicitly stop the current one first.

## 📁 Data Storage

Tim stores all data locally in an SQLite database located at `~/.tim.db`. This ensures:

- 🔒 **Privacy**: Your data never leaves your machine
- 🚀 **Speed**: Fast local queries
- 💾 **Reliability**: Robust SQLite storage
- 📦 **Portability**: Easy to backup and migrate

## 🎨 Customization

### Color Scheme

Tim uses the beautiful [Catppuccin Mocha](https://github.com/catppuccin/catppuccin) color palette by default. The colors are carefully chosen to provide excellent readability while being easy on the eyes.

### Activity Levels

The contributions graph uses 5 activity levels:
- **Level 0**: No activity (dark)
- **Level 1**: Light activity (< 30 minutes)
- **Level 2**: Moderate activity (30-60 minutes)
- **Level 3**: High activity (60-120 minutes)
- **Level 4**: Very high activity (120+ minutes)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Development Setup

```bash
git clone https://github.com/yourusername/tim.git
cd tim
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest
pytest --cov=tim  # With coverage
```

## 📋 Requirements

- Python 3.8+
- Rich 13.0+
- Typer 0.9+
- prompt-toolkit 3.0+

See [requirements.txt](requirements.txt) for the complete list.

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature request? Please open an issue on our [GitHub Issues](https://github.com/yourusername/tim/issues) page.

When reporting bugs, please include:
- Your operating system
- Python version
- Tim version (`tim --version`)
- Steps to reproduce the issue

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - For the beautiful terminal output
- [Typer](https://github.com/tiangolo/typer) - For the CLI framework
- [Catppuccin](https://github.com/catppuccin/catppuccin) - For the gorgeous color palette
- [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - For interactive prompts

## 🔮 Roadmap

- [ ] Goal tracking and progress monitoring
- [ ] Export data to CSV/JSON
- [ ] Pomodoro timer integration
- [ ] Web dashboard
- [ ] Team collaboration features

---

Made with ❤️ and lots of ☕

**[⭐ Star this repo](https://github.com/yourusername/tim) if you find it useful!**
