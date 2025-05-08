# Task Plan: Python Markdown Slides Application for macOS

## Problem Statement

Create a Python application that renders markdown files as HTML slides with configurable global hotkeys for navigation on macOS.

## Requirements

### Functional Requirements

- Load and parse a `slides.yaml` configuration file from a specified directory
- Read markdown files specified in the configuration
- Convert markdown content to HTML for presentation
- Display slides in a window on macOS
- Navigate between slides (forward and backward)
- Support configurable global hotkeys for navigation
- Maintain slide state (current position) during presentation

### Non-functional Requirements

- Usability: Simple interface with clear navigation
- Compatibility: Full compatibility with macOS
- Reliability: Proper error handling for missing files or invalid markdown
- Maintainability: Clean, modular code structure with separation of concerns.

## Task Breakdown

1. Configuration Management

   - Application-wide configuration will be in a config file in ~/.config/slides/config.json.
   - Application config includes global hotkeys for navigation
   - When the application starts, the user should be able to use Finder to navigate to a folder that contains a slides.yaml file.
   - Selecting the folder will trigger the application to load the configuration and start the presentation
   - To start the presentation, we need to extract file paths from configuration and render the first markdown slide.

2. Markdown Processing

   - Read markdown files from specified paths
   - Convert markdown to HTML
   - Apply styling to HTML output

3. Presentation Interface

   - Create window for displaying slides
   - Style should be configurable in the slides.yaml. Customizations include
     font, font size, background color both for the whole presentation and for
     each individual slide. Individual slides settings override global settings.
   - Implement slide navigation controls

4. Hotkey Management

   - Implement global hotkey registration on macOS
   - Configure hotkeys for next/previous slide navigation
   - Handle hotkey events

5. Application Flow
   - Initialize configuration
   - Load all slides at startup
   - Manage slide state and transitions
   - Handle application lifecycle events

## Potential Challenges

- Global hotkey registration may require special permissions on macOS
- Markdown files might contain complex elements that need special rendering
- Ensuring smooth transitions between slides

## Assumptions

- Users will provide valid markdown files
- The application will run with appropriate permissions for global hotkey registration
- The slides.yaml file will be properly formatted
- The application will be used on a single display
- Users will have the necessary Python dependencies installed

## Success Criteria

- Application successfully loads slides from configuration
- Markdown files are correctly rendered as HTML
- Navigation works smoothly with configurable hotkeys
- Application runs properly on macOS without requiring workarounds
- Users can easily configure the application through the slides.yaml file
- Application handles errors gracefully (missing files, invalid markdown)
