Here’s a sample README file based on the error codes you provided:

```markdown
# Project Name: Qore Command-Line Tool

## Overview
This command-line tool is designed to execute various operations such as listing commands, setting environment variables, running bat files, and fixing problems related to the Qore application.

## Common Errors and Solutions

### Error Code: (x3801)
- **Description**: This error occurs when the arguments provided to a command are unrecognized or invalid.
- **Example**: 
  ```bash
  python test.py -add_command -command_name test111 -command_sub abc def -description "Lệnh kiểm tra" -bat abc.bat def.bat
  ```
  **Solution**: Ensure that all arguments are recognized and properly formatted. Check the spelling and syntax of the command being executed.

### Error Code: (x3212)
- **Description**: Invalid escape sequence in strings, usually involving backslashes `\`.
- **Example**:
  ```python
  """Đọc các định nghĩa lệnh từ tệp C:\Windows\Software\QORE\env\cnf.ini"""
  ```
  **Solution**: Use raw strings by prefixing with `r` or double the backslashes to avoid the invalid escape sequence warning.
  ```python
  r"C:\Windows\Software\QORE\env\cnf.ini"
  ```

### Error Code: (x3902)
- **Description**: Invalid parameters or arguments, typically when specific flags or options are not recognized by the parser.
- **Example**:
  ```bash
  python test.py -test"hjghksfdc"
  ```
  **Solution**: Verify the argument's format and ensure it's supported by the script. Correctly format arguments and avoid spaces between flags and values.

### Error Code: (x3802)
- **Description**: This error indicates a missing or invalid attribute when processing command-line arguments.
- **Example**: 
  ```bash
  AttributeError: 'Namespace' object has no attribute 'interface'
  ```
  **Solution**: Verify that all attributes and options expected in the script are properly defined in the `argparse` setup. Ensure that optional arguments are declared and correctly handled in the script.

## Usage

### Basic Commands
- **List all commands**:
  ```bash
  python test.py -list
  ```
- **Set environment variables**:
  ```bash
  python test.py -set-env
  ```
- **Run a test command**:
  ```bash
  python test.py -test "test"
  ```

### Version
Check the application version:
```bash
python test.py -version
```

## Known Issues
- Conflicting arguments: Ensure that argument names do not conflict with one another.
- Invalid escape sequences: Use raw strings for paths to avoid warnings.

## Contact
For any issues or support, please contact the development team at support@qoreapp.com.

```

This README outlines the common error codes, their descriptions, examples, and solutions. Let me know if you need further adjustments!