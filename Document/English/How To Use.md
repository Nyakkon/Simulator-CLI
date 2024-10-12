
# Simulator-CLI User Guide

## Step 1: Extract the Files
- Extract the **Simulator-CLI ver 1.0.0.zip** file.
- Create a new folder at the path **C:\Windows\Software\QORE**.
- After extracting, paste all the contents into the **C:\Windows\Software\QORE** folder.

## Step 2: Set Up Environment Variables

### Setting Up System Variables
1. Open **Control Panel** and select **System and Security**.
2. Click **System**, then select **Advanced system settings** on the left side.
3. In the **System Properties** dialog, click the **Environment Variables** button.
4. In the **System Variables** section, find **Path** and click **Edit**.
5. Add **C:\Windows\Software\QORE** at the end of the list.

   **Illustration:**

   ![Set up System Variable](https://github.com/Nyakkon/Simulator-CLI/blob/main/Document/Resources/image_path_system_variable.png)

### Setting Up User Variables
1. Similarly, in the **Environment Variables** dialog, scroll down to **User Variables**.
2. Find or add **Path** if it does not exist, then click **Edit**.
3. Add **C:\Windows\Software\QORE** to the list.

   **Illustration:**

   ![Set up User Variable](https://github.com/Nyakkon/Simulator-CLI/blob/main/Document/Resources/image_path_user_variable.png)

## Step 3: Verification

- Open Command Prompt (CMD) and type `QORE -veersion` to check if the tool was successfully installed.
