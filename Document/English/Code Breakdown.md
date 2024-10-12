
# QORE CLI Application

## Overview

This script is a command-line interface (CLI) tool for managing and automating tasks in a system. It uses configuration files in XML and `.ini` formats, which are placed in the folder `C:\Windows\Software\QORE`. The tool allows executing `.bat` scripts, setting system environment variables, and provides a list of available commands.

### Code Breakdown

#### 1. `load_command_descriptions()`
This function loads command descriptions from the file `C:\Windows\Software\QORE\env\cnf.ini`.

- **Purpose:** Reads commands defined in the `.ini` file that describes each command's functionality.
- **Implementation:**
    - Reads the `cnf.ini` file using Python's `configparser` module.
    - Returns the dictionary of commands found in the `[commands]` section.
    - Handles errors in case the `.ini` file or the commands section doesn't exist.

#### 2. `is_valid_name(name)`
This function checks whether a given name contains valid characters (letters, numbers, dashes, and underscores).

- **Purpose:** To ensure that only valid command names are used.
- **Implementation:**
    - Uses regular expressions to match against the allowed characters.

#### 3. `parse_xml(file_path)`
This function parses an XML file to extract the command name, description, and path to a `.bat` file.

- **Purpose:** To read the XML files in the `C:\Windows\Software\QORE\XML` folder, containing details about each command.
- **Implementation:**
    - Extracts the `Name`, `Description`, and the path to the `.bat` file (`DatFilePath`).
    - Constructs the path to the `cmd` folder where `.bat` files are stored.

#### 4. `get_names_from_xml_folder()`
This function loops through all the XML files in the `C:\Windows\Software\QORE\XML` folder to generate a dictionary of valid command names.

- **Purpose:** Collects commands from XML files, and checks whether they are valid by calling `is_valid_name()`.
- **Implementation:**
    - Reads all XML files in the folder and parses their content.
    - Only adds valid commands to the list.

#### 5. `run_bat_from_name(dat_file)`
This function executes the `.bat` file corresponding to the selected command.

- **Purpose:** To run the `.bat` file for each command.
- **Implementation:**
    - Converts the relative path to an absolute path.
    - Uses `os.system()` to call the `.bat` file.

#### 6. `print_command_help(names_from_xml, command_descriptions)`
This function prints all available commands along with their descriptions.

- **Purpose:** Provides a list of commands from both the `.ini` and XML files.
- **Implementation:**
    - Outputs all commands defined in the `cnf.ini` file.
    - Outputs all commands from the XML folder.

#### 7. `fix_problem()`
This function ensures the necessary folders (`XML` and `cmd`) exist.

- **Purpose:** Ensures that the script can create and store files in the correct directories.
- **Implementation:**
    - Checks if the folders exist and creates them if not.

#### 8. `set_system_environment()`
This function adds the path to the `QORE` folder to the system's environment variable `PATH`.

- **Purpose:** To allow the `QORE` commands to be called from any directory in the command line.
- **Implementation:**
    - Opens the Windows Registry to modify the `PATH` variable.

#### 9. `clean_path()`
This function cleans up the system's `PATH` by removing duplicate or invalid entries.

- **Purpose:** To ensure the `PATH` variable is properly formatted.
- **Implementation:**
    - Opens the Windows Registry and removes any redundant characters from the `PATH`.

#### 10. `main()`
This is the main function that coordinates the other functions based on command-line arguments.

- **Purpose:** It serves as the entry point of the script.
- **Implementation:**
    - Handles command-line options using `argparse`.
    - Supports listing commands, setting the environment, fixing folder issues, and running `.bat` files.
