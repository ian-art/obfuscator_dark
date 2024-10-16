import base64
import os
import shutil
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set appearance mode to dark
ctk.set_appearance_mode("dark")  

# Function to get the correct path for resources when using PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller or development """
    try:
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller stores files
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def on_drag(event):
    # Update the position of the window based on mouse movement
    x = event.x_root - drag_offset_x
    y = event.y_root - drag_offset_y
    root.geometry(f"+{x}+{y}")

def on_drag_start(event):
    global drag_offset_x, drag_offset_y
    # Calculate the offset of the mouse cursor relative to the window position
    drag_offset_x = event.x_root - root.winfo_x()
    drag_offset_y = event.y_root - root.winfo_y()
    draggable_area.bind("<B1-Motion>", on_drag)

def on_drag_end(event):
    # Unbind the motion event
    draggable_area.unbind("<B1-Motion>")

# Function to obfuscate the selected batch file
def obfuscate_file(file_path):
    if not file_path:
        return
    
    # Base64 obfuscation content
    obfuscated_content = base64.b64decode(b"//4mY2xzDQo=")

    output_file = os.path.splitext(file_path)[0] + "_obfuscated" + os.path.splitext(file_path)[1]
    
    try:
        with open(output_file, "wb") as output_f:
            output_f.write(obfuscated_content)
        
        with open(file_path, "rb") as original_f, open(output_file, "ab") as output_f:
            shutil.copyfileobj(original_f, output_f)

        messagebox.showinfo("Success", f"File obfuscated and saved as {output_file}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to deobfuscate using Python (replacing batch script)
def deobfuscate_file(file_path):
    try:
        base_name, ext = os.path.splitext(os.path.basename(file_path))
        output_file_path = os.path.join(os.path.dirname(file_path), base_name + "_deobfuscated" + ext)

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as input_file:
            lines = input_file.readlines()

        if len(lines) > 1:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.writelines(lines[1:])

            messagebox.showinfo("Success", f"File deobfuscated and saved as {output_file_path}")
        else:
            messagebox.showerror("Error", "The input file appears to be empty or improperly formatted.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select a file and obfuscate it
def select_file_obfuscate():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        obfuscate_file(file_path)

# Function to select a file and deobfuscate it
def select_file_deobfuscate():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        deobfuscate_file(file_path)

# Main GUI setup
def main():
    global root, draggable_area  # Added draggable_area to global scope for accessibility
    root = ctk.CTk()
    root.title("Batch File Obfuscator/Deobfuscator")
    root.geometry("400x223")

    # Rounded corners for the main window
    root.overrideredirect(True)  # Remove the window decorations
    root.wm_attributes("-topmost", True)  # Keep the window on top

    # Create a frame for the content with rounded corners
    frame = ctk.CTkFrame(root, corner_radius=20, fg_color="black")  # Set frame color to black
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Set the icon (if applicable)
    icon_path = resource_path('obfuscator.ico')
    root.iconbitmap(icon_path)

    # Add a draggable area in the top right corner
    draggable_area = ctk.CTkFrame(frame, width=15, height=15, corner_radius=15, fg_color="grey")
    draggable_area.pack(side="top", anchor="ne")  # Change anchor to "ne" for top right
    draggable_area.bind("<ButtonPress-1>", on_drag_start)
    draggable_area.bind("<ButtonRelease-1>", on_drag_end)

    # Create and place buttons with rounded corners
    select_button_obfuscate = ctk.CTkButton(frame, text="Select a .bat or .cmd file to obfuscate", 
                                            command=select_file_obfuscate, width=300, height=40, corner_radius=20)
    select_button_obfuscate.pack(pady=20)

    select_button_deobfuscate = ctk.CTkButton(frame, text="Select a .bat or .cmd file to deobfuscate", 
                                              command=select_file_deobfuscate, width=300, height=40, corner_radius=20)
    select_button_deobfuscate.pack(pady=10)

    # Add a close button with rounded corners
    close_button = ctk.CTkButton(frame, text="x", command=root.quit, width=15, height=15, corner_radius=50)
    close_button.pack(pady=(10, 20))

    root.mainloop()

if __name__ == "__main__":
    main()
