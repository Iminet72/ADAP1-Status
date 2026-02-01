# Contributing to Adap1Status

Thank you for your interest in contributing to the Adap1Status Home Assistant integration!

## Development Setup

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Test your changes with Home Assistant
6. Submit a pull request

## Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep code simple and readable

## Testing

Before submitting a pull request:

1. Test the integration with a real or simulated ADA-P1 Meter device
2. Verify all sensors are created correctly
3. Check error handling by testing with invalid URLs or unreachable devices
4. Ensure configuration flow works properly
5. Test uninstalling and reinstalling the integration

## Adding New Features

When adding new sensor types or features:

1. Update `const.py` with new sensor definitions
2. Update `sensor.py` to handle the new data
3. Update documentation (README.md, API.md)
4. Update CHANGELOG.md
5. Increment version in `manifest.json` if appropriate

## Localization

To add a new language:

1. Create a new JSON file in `custom_components/adap1status/translations/`
2. Use the two-letter language code (e.g., `de.json` for German)
3. Copy the structure from `en.json`
4. Translate all strings

## Reporting Issues

When reporting issues, please include:

- Home Assistant version
- Adap1Status integration version
- Error messages from the logs
- Steps to reproduce the issue
- Device information (if relevant)

## Pull Request Process

1. Update documentation as needed
2. Update CHANGELOG.md
3. Ensure your code follows the style guidelines
4. Test thoroughly before submitting
5. Provide a clear description of your changes

## Code of Conduct

- Be respectful and constructive
- Help others learn and grow
- Focus on what is best for the community
- Show empathy towards others

## Questions?

Feel free to open an issue for questions or discussions about development.
