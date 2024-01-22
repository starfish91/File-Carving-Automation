#code for hex editor apps.
import tkinter as tk
from tkinter import filedialog

class HexEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Hex Editor")
        self.create_widgets()

    def create_widgets(self):
        self.text_widget = tk.Text(self.root, wrap="none", undo=True, width=80, height=20)
        self.text_widget.pack(expand=True, fill="both")

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                content = file.read()
                hex_lines = [content[i:i+10] for i in range(0, len(content), 10)]
                ascii_lines = [self.format_ascii_line(content[i:i+10]) for i in range(0, len(content), 10)]

                formatted_content = ""
                for hex_line, ascii_line in zip(hex_lines, ascii_lines):
                    formatted_content += f"{self.format_hex_line(hex_line)}  |  {ascii_line}\n"

                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(1.0, f"Offset   |  Hexadecimal                           |  ASCII\n")
                self.text_widget.insert(2.0, f"--------+--------------------------------------+------------------------\n")
                self.text_widget.insert(3.0, formatted_content)

    def format_hex_line(self, hex_line):
        return " ".join(f"{byte:02X}" for byte in hex_line)

    def format_ascii_line(self, ascii_line):
        return "".join(chr(ascii_char) if 32 <= ascii_char < 127 else '.' for ascii_char in ascii_line)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary Files", "*.bin")])
        if file_path:
            hex_content = self.text_widget.get(3.0, tk.END)
            hex_values = [int(value, 16) for value in hex_content.split() if value]
            byte_values = bytes(hex_values)
            with open(file_path, "wb") as file:
                file.write(byte_values)

if __name__ == "__main__":
    root = tk.Tk()
    editor = HexEditor(root)
    root.mainloop()
