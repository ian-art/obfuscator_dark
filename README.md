# Batch File Obfuscator/Deobfuscator

A simple GUI application to obfuscate and deobfuscate batch files (.bat, .cmd) using Base64 encoding. This tool is useful for protecting sensitive information in batch scripts.

## Features

- **Obfuscate**: Encode batch files to obscure their contents.
- **Deobfuscate**: Decode previously obfuscated files back to their original state.
- **User-Friendly GUI**: Built with CustomTkinter for an attractive and intuitive interface.

## Installation

1. Clone the repository:

git clone https://github.com/ian-art/obfuscator_dark.pyw.git

2. Navigate to the project directory:

cd <repo>

3. Install the required package:

pip install customtkinter

## Usage
Run the application:

python script_name.pyw

## Building the Executable
To create a standalone executable from the Python script, you can use PyInstaller. Follow these steps:

Install PyInstaller if you haven't already:

pip install pyinstaller

Prepare the build command with your specific paths:

Replace the placeholders with your actual file paths:

%icopath%: Path to your icon file (if you have one)
%verpath%: Path to your version file (if you have one)
%datapath%: Path to any additional data files needed (choose the icon file)
%filepath%: Path to your main Python script

Run the following command in your terminal:

pyinstaller.exe --clean --onefile --noconsole --icon="%icopath%" --version-file="%verpath%" --add-data="%datapath%;." "%filepath%"

This command does the following:

--clean: Cleans the PyInstaller cache before building
--onefile: Creates a single executable file
--noconsole: Prevents a console window from opening (useful for GUI applications)
--icon: Specifies an icon for the executable
--version-file: Adds version information from a file
--add-data: Includes additional data files with the executable

Locate the executable: After running the command, you can find the generated executable in the dist folder within your project directory.

Feel free to customize this section based on your specific setup or any additional details you want to include!
