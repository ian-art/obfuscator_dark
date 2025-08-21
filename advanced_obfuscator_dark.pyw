import base64
import os
import shutil
import sys
import random
import customtkinter as ctk
from tkinter import filedialog, messagebox


# =========================
# Utility Functions
# =========================

def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller or development """
    try:
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller stores files
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def xor_bytes(data: bytes, key: int) -> bytes:
    """Simple XOR encryption with a single-byte key."""
    return bytes(b ^ key for b in data)


# =========================
# Your Original Obfuscator
# =========================

def obfuscate_file_executable(file_path):
    """Your version: Obfuscates but still runnable as batch."""
    if not file_path:
        return

    # Base64 obfuscation content (your fixed blob)
    obfuscated_content = base64.b64decode(b"//4mY2xzDQo=")

    output_file = os.path.splitext(file_path)[0] + "_obfuscated" + os.path.splitext(file_path)[1]

    try:
        with open(output_file, "wb") as output_f:
            output_f.write(obfuscated_content)

        with open(file_path, "rb") as original_f, open(output_file, "ab") as output_f:
            shutil.copyfileobj(original_f, output_f)

        messagebox.showinfo("Success", f"File obfuscated (executable) saved as {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# =========================
# Safer Wrapper Obfuscator
# =========================

def obfuscate_file_safer(file_path):
    """My version: Stronger obfuscation but no longer directly executable."""
    if not file_path:
        return

    with open(file_path, "rb") as f:
        original_data = f.read()

    # Random XOR key
    key = random.randint(1, 255)

    # XOR + Base64
    xored = xor_bytes(original_data, key)
    encoded = base64.b64encode(xored).decode("ascii")

    # Output scrambled file (not runnable as batch anymore)
    output_file = os.path.splitext(file_path)[0] + "_obfuscated_safe.bat"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"REM Encoded with XOR+Base64\n")
        out.write(f"REM Key={key}\n")
        out.write(f"REM This file is no longer directly executable.\n")
        out.write(f"PAYLOAD={encoded}\n")

    messagebox.showinfo("Success", f"File obfuscated (safe, not executable) saved as {output_file}")


# =========================
# Deobfuscators
# =========================

def deobfuscate_file(file_path):
    """Deobfuscate your original format (skips first line)."""
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


def deobfuscate_file_safer(file_path):
    """Deobfuscate my safer format (XOR+Base64)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        key, payload = None, None
        for line in lines:
            if line.strip().startswith("PAYLOAD="):
                payload = line.split("=", 1)[1].strip()
            if line.strip().startswith("REM Key="):
                key = int(line.split("=", 1)[1].strip())

        if not payload or key is None:
            messagebox.showerror("Error", "Invalid safe obfuscated file format.")
            return

        decoded = base64.b64decode(payload)
        decoded = xor_bytes(decoded, key)

        output_file = os.path.splitext(file_path)[0] + "_deobfuscated.bat"
        with open(output_file, "wb") as out:
            out.write(decoded)

        messagebox.showinfo("Success", f"File deobfuscated (safe) saved as {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# =========================
# Help Information
# =========================

def show_help():
    """Displays information about how this tool works."""
    help_text = (
        "🔹 Obfuscate (Executable Version)\n"
        " - Adds a tiny header + your original batch file.\n"
        " - Still runnable directly as a batch file.\n\n"
        "🔹 Deobfuscate (Executable Version)\n"
        " - Removes the header, restoring the original script.\n\n"
        "🔹 Obfuscate (Not Executable Version)\n"
        " - Encodes batch file with XOR + Base64.\n"
        " - Resulting file is NOT runnable as batch anymore.\n\n"
        "🔹 Deobfuscate (Not Executable Version)\n"
        " - Reads XOR key + payload.\n"
        " - Decodes and reconstructs the original batch file.\n\n"
        "Use the 'Executable Version' if you still want to run the file.\n"
        "Use the 'Not Executable Version' for safer distribution."
    )
    messagebox.showinfo("How It Works", help_text)


# =========================
# GUI Functions
# =========================

def select_file_obfuscate_exec():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        obfuscate_file_executable(file_path)


def select_file_obfuscate_safe():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        obfuscate_file_safer(file_path)


def select_file_deobfuscate_exec():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        deobfuscate_file(file_path)


def select_file_deobfuscate_safe():
    file_path = filedialog.askopenfilename(filetypes=[("Batch files", "*.bat *.cmd")])
    if file_path:
        deobfuscate_file_safer(file_path)


# =========================
# GUI Setup
# =========================

def main():
    global root, draggable_area
    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.title("Batch File Obfuscator/Deobfuscator")
    root.geometry("350x310")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)

    frame = ctk.CTkFrame(root, corner_radius=20, fg_color="black")
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Icon
    try:
        icon_path = resource_path('obfuscator.ico')
        root.iconbitmap(icon_path)
    except Exception:
        pass

    # Draggable corner
    draggable_area = ctk.CTkFrame(frame, width=15, height=15, corner_radius=15, fg_color="grey")
    draggable_area.pack(side="top", anchor="ne")
    draggable_area.bind("<ButtonPress-1>", on_drag_start)
    draggable_area.bind("<ButtonRelease-1>", on_drag_end)

    # Buttons
    ctk.CTkButton(frame, text="Obfuscate (Executable Version)",
                  command=select_file_obfuscate_exec, width=300, height=40, corner_radius=20).pack(pady=6)
                  
    ctk.CTkButton(frame, text="Deobfuscate (Executable Version)",
                  command=select_file_deobfuscate_exec, width=300, height=40, corner_radius=20).pack(pady=6)                  

    ctk.CTkButton(frame, text="Obfuscate (Not Executable Version)",
                  command=select_file_obfuscate_safe, width=300, height=40, corner_radius=20).pack(pady=6)

    ctk.CTkButton(frame, text="Deobfuscate (Not Executable Version)",
                  command=select_file_deobfuscate_safe, width=300, height=40, corner_radius=20).pack(pady=6)

    # Help � button
    ctk.CTkButton(frame, text="�", command=show_help,
                  width=15, height=15, corner_radius=15, fg_color="black").pack(pady=4)

    # Close button
    ctk.CTkButton(frame, text="❎", command=root.quit,
                  width=25, height=25, corner_radius=100, fg_color="black").pack(pady=(6, 11))

    root.mainloop()


# =========================
# Window Drag Handlers
# =========================

def on_drag(event):
    x = event.x_root - drag_offset_x
    y = event.y_root - drag_offset_y
    root.geometry(f"+{x}+{y}")


def on_drag_start(event):
    global drag_offset_x, drag_offset_y
    drag_offset_x = event.x_root - root.winfo_x()
    drag_offset_y = event.y_root - root.winfo_y()
    draggable_area.bind("<B1-Motion>", on_drag)


def on_drag_end(event):
    draggable_area.unbind("<B1-Motion>")


if __name__ == "__main__":
    main()
