# Implementation Plan: Python Markdown Slides Application for macOS

## Information Gathered

### Repository Analysis

- The repository appears to be a new project with minimal existing structure
- The project is focused on creating a markdown-based slides application for macOS
- There is a task plan document that outlines the requirements and features at
  docs/prds/init/plan.md.

### External Research

- Python libraries for markdown processing: `markdown`, `mistune`, or `python-markdown2`
- GUI frameworks for macOS: `PyQt5`, `PySide6`, `wxPython`, or `Tkinter`
- Global hotkey management: `pynput` or `keyboard` libraries
- YAML parsing: `PyYAML` library
- HTML rendering: `WebKit` or embedded browser components

## Technical Approach

The application will be built using a modular architecture with clear
separation of concerns. We'll use the Model-View-Controller (MVC) pattern to
separate the data handling, presentation, and control logic.

**Justification for chosen approach:**

1. **PyQt5/PySide6 for GUI**: These frameworks provide robust cross-platform
   GUI capabilities with good macOS integration and WebKit components for HTML
   rendering.
2. **Python-markdown for parsing**: This library offers good extension support
   and customization options.
3. **PyYAML for configuration**: Standard library for YAML parsing with good
   performance.
4. **Modular architecture**: Ensures maintainability and separation of
   concerns.

## Implementation Details

### File Structure

```
slides/
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── slides/                 # Main package
│   ├── __init__.py
│   ├── config/             # Configuration handling
│   │   ├── __init__.py
│   │   ├── app_config.py   # Application configuration
│   │   └── slide_config.py # Slide-specific configuration
│   ├── markdown/           # Markdown processing
│   │   ├── __init__.py
│   │   ├── parser.py       # Markdown to HTML conversion
│   │   └── renderer.py     # HTML rendering utilities
│   ├── presentation/       # Presentation UI
│   │   ├── __init__.py
│   │   ├── window.py       # Main presentation window
│   │   ├── slide_view.py   # Slide display component
│   │   └── controls.py     # Navigation controls
│   ├── hotkeys/            # Hotkey management
│   │   ├── __init__.py
│   │   ├── manager.py      # Global hotkey registration
│   │   └── handlers.py     # Hotkey event handlers
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── file_utils.py   # File operations
│       └── error_handler.py # Error handling utilities
└── tests/                  # Unit tests
    ├── __init__.py
    ├── test_config.py
    ├── test_markdown.py
    ├── test_presentation.py
    └── test_hotkeys.py
```

### File Changes

1. New Files:
   - All files listed in the file structure above need to be created

### Class and Function Definitions

#### main.py

```python
def main():
    # Application entry point
    # Initialize application, load configuration, and start UI
    pass

if __name__ == "__main__":
    main()
```

#### slides/config/app_config.py

```python
class AppConfig:
    def __init__(self):
        # Initialize application configuration
        pass

    def load_config(self, config_path):
        # Load application configuration from JSON file
        pass

    def get_hotkey_config(self):
        # Return hotkey configuration
        pass
```

#### slides/config/slide_config.py

```python
class SlideConfig:
    def __init__(self):
        # Initialize slide configuration
        pass

    def load_config(self, yaml_path):
        # Load slide configuration from YAML file
        pass

    def get_slide_paths(self):
        # Return list of markdown file paths
        pass

    def get_global_style(self):
        # Return global styling configuration
        pass

    def get_slide_style(self, slide_index):
        # Return style for specific slide
        pass
```

#### slides/markdown/parser.py

```python
class MarkdownParser:
    def __init__(self, config):
        # Initialize markdown parser with configuration
        pass

    def parse_file(self, file_path):
        # Parse markdown file and return HTML
        pass

    def parse_text(self, markdown_text):
        # Parse markdown text and return HTML
        pass
```

#### slides/markdown/renderer.py

```python
class HTMLRenderer:
    def __init__(self, config):
        # Initialize HTML renderer with configuration
        pass

    def apply_styling(self, html_content, slide_index):
        # Apply styling to HTML content
        pass

    def create_slide_html(self, html_content, slide_index):
        # Create complete HTML document for slide
        pass
```

#### slides/presentation/window.py

```python
class PresentationWindow:
    def __init__(self, config):
        # Initialize presentation window
        pass

    def show(self):
        # Show presentation window
        pass

    def load_slide(self, slide_index):
        # Load and display slide
        pass

    def next_slide(self):
        # Navigate to next slide
        pass

    def previous_slide(self):
        # Navigate to previous slide
        pass
```

#### slides/presentation/slide_view.py

```python
class SlideView:
    def __init__(self, parent):
        # Initialize slide view component
        pass

    def set_content(self, html_content):
        # Set HTML content to display
        pass

    def clear(self):
        # Clear current content
        pass
```

#### slides/hotkeys/manager.py

```python
class HotkeyManager:
    def __init__(self, config):
        # Initialize hotkey manager with configuration
        pass

    def register_hotkeys(self):
        # Register global hotkeys
        pass

    def unregister_hotkeys(self):
        # Unregister global hotkeys
        pass

    def set_next_handler(self, handler):
        # Set handler for next slide hotkey
        pass

    def set_previous_handler(self, handler):
        # Set handler for previous slide hotkey
        pass
```

#### slides/utils/file_utils.py

```python
def ensure_config_directory():
    # Ensure configuration directory exists
    pass

def read_file(file_path):
    # Read file content
    pass

def write_file(file_path, content):
    # Write content to file
    pass

def file_exists(file_path):
    # Check if file exists
    pass
```

#### slides/utils/error_handler.py

```python
class ErrorHandler:
    @staticmethod
    def handle_file_error(error, file_path):
        # Handle file-related errors
        pass

    @staticmethod
    def handle_config_error(error, config_path):
        # Handle configuration errors
        pass

    @staticmethod
    def handle_markdown_error(error, markdown_path):
        # Handle markdown parsing errors
        pass
```

### Data Structures

#### Application Configuration (JSON)

This lays out the initial window dimensions, but the application should be
resizable and should update presentation when resized.

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

#### Slides Configuration (YAML)

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

#### Slide Object

```python
class Slide:
    def __init__(self, path, index, style=None):
        self.path = path
        self.index = index
        self.style = style
        self.content = None
        self.html = None
```

### External Dependencies

- **PyQt5/PySide6**: GUI framework for creating the presentation window and rendering HTML
- **PyYAML**: For parsing YAML configuration files
- **python-markdown**: For converting markdown to HTML
- **pynput**: For global hotkey registration and handling
- **pytest**: For unit testing

## Verification Plan

### Unit Tests

#### Configuration Tests

- Test loading application configuration from JSON file
- Test loading slides configuration from YAML file
- Test handling of missing configuration files
- Test parsing of hotkey configuration

#### Markdown Processing Tests

- Test parsing markdown files to HTML
- Test applying styling to HTML content
- Test handling of invalid markdown

#### Presentation Tests

- Test slide navigation (next/previous)
- Test slide rendering
- Test style application

#### Hotkey Tests

- Test hotkey registration
- Test hotkey event handling

### Validation Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest

# Run application
python main.py
```

### Success Criteria

- Application successfully loads and parses configuration files
- Markdown files are correctly converted to HTML with proper styling
- Presentation window displays slides with correct formatting
- Navigation between slides works using both UI controls and global hotkeys
- Application handles errors gracefully with appropriate user feedback
- All unit tests pass

### Manual Testing Checklist

1. Application starts correctly and prompts for slides.yaml location
2. Configuration is loaded without errors
3. First slide is displayed with correct styling
4. Navigation using global hotkeys works as expected
5. Navigation using UI controls works as expected
6. Slide-specific styling is applied correctly
7. Application handles missing files with appropriate error messages
8. Application handles invalid markdown with appropriate error messages
