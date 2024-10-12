
# **README (English)**

## **Introduction**
The CLI "QORE" is a command-line application (CLI) that helps manage and automate tasks by running `.bat` files through XML configuration. It supports commands from XML files and configurations from the `cnf.ini` file, allowing users to create custom commands based on the project's requirements.

### **Project Structure**
```
C:\Windows\Software\QORE\
    ├── cmd/               # Contains .bat files
    ├── env/               # Contains the cnf.ini configuration file
    ├── XML/               # Contains XML files defining commands
    └── main.py            # Main Python file to handle the CLI
```

---

## **Detailed explanation of each part of the code**

### **1. Loading command descriptions from `cnf.ini`**

```python
def load_command_descriptions():
    '''Read command definitions from C:\Windows\Software\QORE\env\cnf.ini'''
    config = configparser.ConfigParser()
    cnf_path = r'C:\Windows\Software\QORE\env\cnf.ini'
```

- **Purpose:** This function reads command definitions from the `cnf.ini` file, which is located in the `env` folder. The function checks if the `cnf.ini` file exists and then retrieves the command descriptions from the `[commands]` section in the file.

```python
if os.path.exists(cnf_path):
    with open(cnf_path, 'r', encoding='utf-8') as configfile:
        config.read_file(configfile)
    if 'commands' in config:
        return config['commands']
    else:
        print("Err: 'commands' section not found in cnf.ini file")
        return {}
else:
    print(f"Err: cnf.ini file not found at {cnf_path}")
    return {}
```

- **Operation:** If the `cnf.ini` file is not found, the function will return an error message. If the file exists, it reads and returns the commands defined in the configuration file.

### **2. Checking for valid command names**

```python
def is_valid_name(name):
    '''Check for valid names, only containing letters, numbers, and hyphens'''
    return re.match(r'^[a-zA-Z0-9-_]+$', name) is not None
```

- **Purpose:** This function checks if the command name is valid. A valid command name contains only letters, numbers, and hyphens.

### **3. Parsing XML Files**

```python
def parse_xml(file_path):
    '''Read XML file and return Name, Description, and .bat file path'''
    tree = ET.parse(file_path)
    root = tree.getroot()
```

- **Purpose:** This function reads the XML configuration files and extracts the command `Name`, `Description`, and the path to the `.bat` file that needs to be run. 

```python
name = root.find('Name').text if root.find('Name') is not None else 'N/A'
description = root.find('Description').text if root.find('Description') is not None else 'N/A'
dat_path = root.find('DatFilePath').text if root.find('DatFilePath') is not None else 'N/A'
dat_path = os.path.join(r'C:\Windows\Software\QORE\cmd', dat_path)
return name, description, dat_path
```

- **Operation:** If certain fields such as `Name` or `Description` are missing, it assigns them a default value of `N/A`. It also constructs the full path to the `.bat` file.

### **4. Getting Commands from XML Directory**

```python
def get_names_from_xml_folder():
    '''Iterate through XML files in the folder and return list of command names'''
    xml_folder = r'C:\Windows\Software\QORE\XML'
    names = {}
```

- **Purpose:** This function looks into the `XML` folder to retrieve the available commands, checking if the folder exists and processing the `.xml` files in that directory.

### **5. Running `.bat` Files from Command Names**

```python
def run_bat_from_name(dat_file):
    '''Execute the corresponding .bat file'''
    full_path = os.path.abspath(dat_file)
    if os.path.exists(full_path):
        os.system(f'call {full_path}')
    else:
        print(f"Err: .bat file {full_path} does not exist (x9338)")
```

- **Purpose:** This function runs the `.bat` file associated with a command. It checks if the file exists before trying to execute it.

### **6. Main Function**

```python
def main():
    command_descriptions = load_command_descriptions()
    names_from_xml = get_names_from_xml_folder()
    parser = argparse.ArgumentParser(description="QORE - CLI application for task management and automation.")
    parser.add_argument('-version', action='version', version='App 1.0')
    parser.add_argument('-list', action='store_true', help="Browse and print information from XML files")
    parser.add_argument('-fix-problem', action='store_true', help="Check and create XML and cmd directories if missing")
    parser.add_argument('-set-env', action='store_true', help="Set the QORE environment variables for CMD")
```

- **Purpose:** The main function initializes the CLI and handles user arguments, invoking the right functions to process the commands.

```python
for name in names_from_xml.keys():
    parser.add_argument(f'-{name}', action='store_true', help=f"Run the .bat file from {name}")

args = parser.parse_args()

if args.fix_problem:
    fix_problem()
if args.set_env:
    set_system_environment()
    clean_path()
if args.list:
    print_command_help(names_from_xml, command_descriptions)
for name, (_, dat_path) in names_from_xml.items():
    if getattr(args, name):
        run_bat_from_name(dat_path)
```

- **Operation:** The function checks for user-provided options and then either lists available commands, runs the associated `.bat` files, or sets up environment variables.

