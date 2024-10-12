# Simulator-CLI Testing Guide

## Introduction
The purpose of this guide is to assist users in testing the Simulator-CLI tool, identifying potential errors, and providing detailed steps on how to troubleshoot them. This document is crucial for ensuring a smooth setup and functioning of the tool.

## Common Errors and Troubleshooting

### 1. Error: `Environment Variables Not Set`

**Description:**
One of the most common issues when running the CLI is missing environment variables. If you encounter an error stating that the `QORE` command is not recognized or fails to run, this means the environment variable has not been configured correctly.

**Cause:**
The system cannot find the path `C:\Windows\Software\QORE`, and thus, it cannot recognize the `QORE` command.

**Solution:**
1. Open **Control Panel** and navigate to **System and Security**.
2. Click on **System**, then select **Advanced system settings** on the left-hand panel.
3. In the **System Properties** window, click on the **Environment Variables** button.
4. Under **System variables**, scroll to **Path**, and click **Edit**.
5. Add `C:\Windows\Software\QORE` to the end of the list.
6. Press **OK** and restart your command prompt.
7. Verify the environment by typing `QORE -list` in the command prompt.

**Note:** Be sure to set both **System Variables** and **User Variables** if the error persists.

### 2. Error: `File Not Found` for XML or Batch Files

**Description:**
You might encounter errors that point to missing `.xml` or `.bat` files in the `QORE` directory when running commands like `QORE -list`.

**Cause:**
The necessary XML configuration or `.bat` script files are not present in the correct directory, usually `C:\Windows\Software\QORE\XML` or `C:\Windows\Software\QORE\cmd`.

**Solution:**
1. Ensure that the necessary `.xml` files are present in the `C:\Windows\Software\QORE\XML` directory.
2. Similarly, the `.bat` files should be located in `C:\Windows\Software\QORE\cmd`.
3. If the files are missing, either download them from the appropriate source or manually create the required structure.
4. Re-run the command after verifying the file locations.

### 3. Error: `Permission Denied` or `Access Denied`

**Description:**
When running the program, especially during environment variable setup, you may encounter permission errors preventing changes to the system settings.

**Cause:**
This is typically due to not having administrative privileges.

**Solution:**
1. Close the current command prompt or terminal.
2. Open a new command prompt or PowerShell window **as an administrator**.
   - Right-click the Command Prompt or PowerShell icon and select **Run as administrator**.
3. Re-run the command that caused the permission issue.
4. If you’re modifying the registry or system paths, administrative rights are required.

### 4. Error: `Registry Path Not Found`

**Description:**
When running `set_system_environment`, you might get an error indicating that the system path could not be updated due to a missing registry path.

**Cause:**
This error occurs when the registry key for the environment variable doesn’t exist or cannot be accessed.

**Solution:**
1. Open **Registry Editor** by typing `regedit` in the Windows search bar.
2. Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`.
3. Right-click on **Environment** and select **New** > **String Value**.
4. Name the new string `Path` and set its value to `C:\Windows\Software\QORE`.
5. Exit the Registry Editor and try running the CLI command again.

### 5. Error: `Invalid Command in cnf.ini`

**Description:**
While running the tool, an error might occur when reading commands from the `cnf.ini` file, especially if there are invalid or malformed entries.

**Cause:**
This error happens when the `cnf.ini` file contains invalid characters, improper formatting, or missing sections.

**Solution:**
1. Navigate to `C:\Windows\Software\QORE\env\cnf.ini`.
2. Open the `cnf.ini` file in a text editor (such as Notepad++ or Visual Studio Code).
3. Ensure that the `[commands]` section is present and that each command follows the correct format:
   ```
   [commands]
   version = Application version
   list = Display available commands
   fix-problem = Check and create necessary directories
   set-env = Set system environment variables
   ```
4. Correct any formatting issues and save the file.
5. Re-run the CLI tool.

### 6. Error: `Unicode Decode Error in cnf.ini`

**Description:**
This error might arise when attempting to parse the `cnf.ini` file, especially when it contains non-ASCII characters that cause the parser to fail.

**Cause:**
This can happen if the `cnf.ini` file is saved in a non-UTF-8 format, or if it contains characters that cannot be properly decoded.

**Solution:**
1. Open `cnf.ini` in a text editor.
2. Save the file with UTF-8 encoding:
   - In Notepad++, go to **Encoding** > **Convert to UTF-8**.
   - Save and close the file.
3. Retry the command.

### 7. Error: `Batch File Not Executing`

**Description:**
When attempting to execute a `.bat` file from the CLI, the command might fail, and nothing happens.

**Cause:**
This usually occurs if the path to the `.bat` file is incorrect or if the batch file itself has issues such as invalid commands.

**Solution:**
1. Double-check the path to the `.bat` file to ensure it’s correct.
2. Ensure that the `.bat` file contains valid commands by opening it in a text editor.
3. If necessary, run the `.bat` file directly from the command line using `call` to check for any errors.

### 8. Error: `Command Not Recognized`

**Description:**
When typing `QORE -list` or any other command, you receive an error stating that the command is not recognized.

**Cause:**
This error occurs when the environment variables have not been properly set, or the tool is not located in the correct directory.

**Solution:**
1. Ensure that the tool has been placed in the `C:\Windows\Software\QORE` directory.
2. Follow the environment variable setup instructions provided in this guide.
3. Restart the command prompt and try the command again.

## Step-by-Step Guide to Fix Errors

### Environment Variable Setup
1. Open **Control Panel**.
2. Select **System and Security** > **System** > **Advanced System Settings**.
3. In **System Properties**, click **Environment Variables**.
4. Edit the **Path** variable in **System Variables** and add `C:\Windows\Software\QORE`.
5. Restart your command prompt and type `QORE -version` to confirm the setup.

### Manually Fixing Registry Issues
If you encounter issues related to the system registry when setting the environment, follow these steps:
1. Open **Registry Editor** (`regedit`).
2. Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`.
3. Verify that `Path` exists and contains the correct entry for `C:\Windows\Software\QORE`.
4. If the entry is missing, manually create it and add the correct path.

## Contact and Support
For further assistance, feel free to contact the support team at **miko@wibu.me**.

We are here to ensure that your experience with **Simulator-CLI** is smooth and error-free!
