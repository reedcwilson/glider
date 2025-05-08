# Markdown Slides

A Python application that renders markdown files as HTML slides with configurable global hotkeys for macOS.

## Features

- Load and parse a `slides.yaml` configuration file
- Convert markdown content to HTML for presentation
- Display slides in a window on macOS
- Navigate between slides using UI controls or global hotkeys
- Configure styling for the entire presentation or individual slides
- Support for code highlighting, tables, and other markdown features

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/slides.git
   cd slides
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. When prompted, select a directory containing a `slides.yaml` file.

3. Use the navigation buttons or hotkeys to move between slides.

### Global Hotkeys

Default hotkeys (configurable in `~/.config/slides/config.json`):
- Next slide: `Cmd + Alt + Shift + Right`
- Previous slide: `Cmd + Alt + Shift + Left`

You can also use the arrow keys or space/backspace for navigation within the application window.

## Configuration

### Application Configuration

The application configuration is stored in `~/.config/slides/config.json`:

```json
{
  "hotkeys": {
    "next_slide": ["cmd", "alt", "shift", "right"],
    "previous_slide": ["cmd", "alt", "shift", "left"]
  },
  "window": {
    "width": 800,
    "height": 600,
    "fullscreen": false
  }
}
```

### Slides Configuration

Slides are configured using a `slides.yaml` file:

```yaml
title: "Presentation Title"
style:
  font: "Helvetica"
  fontSize: 24
  backgroundColor: "#FFFFFF"
  textColor: "#000000"
  justify: "left"
slides:
  - path: "slide1.md"
    style:
      backgroundColor: "#F0F0F0"
      justify: "center"
  - path: "slide2.md"
  - path: "slide3.md"
    style:
      fontSize: 28
```

## Development

### Running Tests

```
pytest
```

### Project Structure

```
slides/
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── slides/                  # Main package
│   ├── __init__.py
│   ├── config/              # Configuration handling
│   ├── markdown/            # Markdown processing
│   ├── presentation/        # Presentation UI
│   ├── hotkeys/             # Hotkey management
│   └── utils/               # Utility functions
└── tests/                   # Unit tests
```

## License

MIT
