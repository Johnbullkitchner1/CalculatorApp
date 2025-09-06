import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator App")
        self.root.geometry("300x500")
        self.root.resizable(False, False)
        
        # Create canvas for background image
        self.canvas = tk.Canvas(root, width=300, height=500, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=7, columnspan=4)
        
        # Load and display background image
        try:
            if getattr(sys, '_MEIPASS', False):
                # Running as a bundled app
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(__file__)
            image_path = os.path.join(base_path, "background.png")
            self.image = Image.open(image_path)
            self.image = self.image.resize((300, 500), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        except Exception as e:
            self.canvas.configure(bg="gray")
            print(f"Image load error: {e}")
        
        # Set initial colors
        self.button_bg = "white"
        self.button_fg = "black"
        self.display_bg = "white"
        self.display_fg = "black"
        
        # Display
        self.display = tk.Entry(root, width=20, font=("Arial", 16), justify="right", bg=self.display_bg, fg=self.display_fg)
        self.canvas.create_window(150, 50, window=self.display)
        
        self.current = ""
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'Dark'
        ]
        
        row = 2
        col = 0
        self.button_widgets = []
        for button in buttons:
            if button == 'Dark':
                cmd = lambda: self.toggle_dark_mode()
            else:
                cmd = lambda x=button: self.click(x)
            btn = tk.Button(root, text=button, width=5, height=2, font=("Arial", 12, "bold"), bg=self.button_bg, fg=self.button_fg, command=cmd)
            self.canvas.create_window(50 + col * 70, 120 + (row-2) * 70, window=btn)
            self.button_widgets.append(btn)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        self.clear()
    
    def click(self, char):
        if char == 'C':
            self.clear()
        elif char == '=':
            try:
                result = eval(self.current)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current = str(result)
            except ZeroDivisionError:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error: Divide by 0")
                self.current = ""
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current = ""
        else:
            self.current += char
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
    
    def clear(self):
        self.current = ""
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, "0")
    
    def toggle_dark_mode(self):
        if self.button_bg == "white":
            self.button_bg = "#CCCCCC"
            self.button_fg = "black"
            self.display_bg = "#999999"
            self.display_fg = "white"
        else:
            self.button_bg = "white"
            self.button_fg = "black"
            self.display_bg = "white"
            self.display_fg = "black"
        
        self.display.config(bg=self.display_bg, fg=self.display_fg)
        for btn in self.button_widgets:
            btn.config(bg=self.button_bg, fg=self.button_fg)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()