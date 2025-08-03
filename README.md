# Storage Manager (stman)

A lightweight CLI tool that tabulates device/folder storage on Windows systems.

## Features

- **Drive Analysis**: View storage usage across all available drives
- **Directory Scanning**: Calculate folder sizes with real-time updates
- **Interactive UI**: Navigate through directories with keyboard commands
- **Performance Optimized**: Uses native Windows APIs for fast scanning
- **Cross-Drive Support**: Works across all accessible Windows drives

## Requirements

- Windows 10/11
- Python 3.8 or higher

## Installation

```powershell
pip install stman
```

## Usage

```powershell
stman
```

### Commands

- `help` - Show available commands
- `exit` - Exit the application
- `goto` - Navigate to a specific path
- `top` - Go to root directory
- `b` - Go back one directory
- `r` - Refresh current view
- `togglecnc` - Toggle showing uncalculatable folders
- `togglewelcome` - Toggle welcome message
- `clearcache` - Clear the size cache

## Contributing

### Reporting Issues

If you encounter any issues or have suggestions for improvements:

1. **Check the error message**: The application provides specific error messages for common issues
2. **Platform compatibility**: This tool only works on Windows systems
3. **DLL errors**: If you see "dir_size.dll not found" errors, try reinstalling the package
4. **Permission errors**: Some folders may be inaccessible due to Windows permissions

### Contributing Code

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on Windows
5. Submit a pull request

### Development Setup

```powershell
git clone https://github.com/glcon/storage-manager.git
cd storage-manager
pip install -e .
```

## License

MIT License - see LICENSE file for details.

## Author

Garrett Connell 