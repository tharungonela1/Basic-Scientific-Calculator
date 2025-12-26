import tkinter as tk
import math as m

class BasicAndScientific(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic and Scientific Calculator")
        self.geometry("440x600")
        self.configure(bg="#222222")
        self.mode = "basic" 
        self.create_widgets() # Now labels will connect properly

    def create_widgets(self):
        # Display area
        self.display_frame = tk.Frame(self, width=400, height=150, bg="#222222")
        self.display_frame.pack(padx=10, pady=10, fill="x")
        self.display_frame.pack_propagate(False)   

        # StringVars to hold input and output
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()

        # Labels connected to StringVars
        self.input_label = tk.Label(self.display_frame, textvariable=self.input_var,
                                    font=("Arial", 20), fg="white", bg="#222222", anchor="e")
        self.input_label.pack(side="top", fill="x", padx=10, pady=(10, 0))

        # Output Label (bottom-right)
        self.output_label = tk.Label(self.display_frame, textvariable=self.output_var,
                                     font=("Arial", 16), fg="#00FF99", bg="#222222", anchor="e")
        self.output_label.pack(side="bottom", fill="x", padx=10, pady=10)

        # Toggle button frame
        self.top_frame = tk.Frame(self, bg="#222222")
        self.top_frame.pack(pady=5, fill="x", padx=10)

        self.toggle_btn = tk.Button(self.top_frame, text="^", font=("Arial", 16), width=3, command=self.toggle_mode)
        self.toggle_btn.pack(side="right", padx=5)

        # Scientific Frame 
        self.scientific_frame = tk.Frame(self, bg="#222222")
        self.create_scientific_mode()

        # Basic panel (always bottom)
        self.basic_frame = tk.Frame(self, bg="#222222")
        self.basic_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.create_basic_mode()

    # Toggle: basic -> scientific (stacked) -> basic
    def toggle_mode(self):
        if self.mode == "basic":
            self.scientific_frame.pack(padx=10, pady=(0,5), fill="both", expand=True)
            self.basic_frame.pack_forget()
            self.basic_frame.pack(padx=10, pady=(5,10), fill="both", expand=True)
            self.geometry("440x750")
            self.mode = "scientific"
        else:
            self.scientific_frame.pack_forget()
            self.basic_frame.pack_forget()
            self.basic_frame.pack(padx=10, pady=5, fill="both", expand=True)
            self.geometry("440x600")
            self.mode = "basic"

    def create_basic_mode(self):
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('AC', 3, 1), ('DEL', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 4),
        ]
        self.basic_buttons = []
        for b in buttons:
            txt, r, c = b[0], b[1], b[2]
            span = b[3] if len(b) > 3 else 1
            
            # Simple white background and black text for all buttons
            btn = tk.Button(self.basic_frame, text=txt, font=("Arial", 16), bg="white", fg="black",
                            command=lambda t=txt: self.basic_click(t))
            btn.grid(row=r, column=c, columnspan=span, padx=3, pady=3, sticky="nsew")
            self.basic_buttons.append(btn)
        for i in range(4):
            self.basic_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.basic_frame.grid_rowconfigure(i, weight=1)

    def create_scientific_mode(self):
        sci_buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('log', 0, 3),
            ('ln', 1, 0), ('√', 1, 1), ('^', 1, 2), ('x!', 1, 3),
            ('π', 2, 0), ('e', 2, 1), ('Deg', 2, 2), ('Rad', 2, 3),
            ('Abs', 3, 0), ('Exp', 3, 1), ('Mod', 3, 2), ('(+/-)', 3, 3),
        ]
        self.scientific_buttons = []
        for (txt, r, c) in sci_buttons:
            btn = tk.Button(self.scientific_frame, text=txt, font=("Arial", 14), bg="white", fg="black",
                            command=lambda t=txt: self.scientific_click(t))
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            self.scientific_buttons.append(btn)
        for i in range(4):
            self.scientific_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.scientific_frame.grid_rowconfigure(i, weight=1)

    def basic_click(self, t):
     try:
        if t == 'DEL':
            current = self.input_var.get()
            if current:   
                self.input_var.set(current[:-1]) 
                self.output_var.set("")
        elif t == 'AC':
            self.input_var.set("")  
            self.output_var.set("")
        elif t == '=':
            expr = self.input_var.get()
            if expr.strip():  
                # Handle replacements for evaluation
                expr = expr.replace('^', '**')
                result = eval(expr)
                self.output_var.set(str(result))
            else:
                self.output_var.set("")
        else:
            self.input_var.set(self.input_var.get() + t)
     except Exception:
        self.output_var.set("Error")

    def scientific_click(self, t):
        val = self.input_var.get()
        try:
            # Evaluate expression first to handle complex inputs
            num = float(eval(val.replace('^', '**'))) if val else 0
            result = None
            if t == 'sin':
                result = m.sin(m.radians(num))
            elif t == 'cos':
                result = m.cos(m.radians(num))
            elif t == 'tan':
                result = m.tan(m.radians(num))
            elif t == 'log':
                result = m.log10(num)
            elif t == 'ln':
                result = m.log(num)
            elif t == '√':
                result = m.sqrt(num)
            elif t == '^':
                self.input_var.set(self.input_var.get() + '**')
                return
            elif t == 'x!':
                result = m.factorial(int(num))
            elif t == 'π':
                self.input_var.set(self.input_var.get() + str(m.pi))
                return
            elif t == 'e':
                self.input_var.set(self.input_var.get() + str(m.e))
                return
            elif t == 'Deg':
                result = m.degrees(num)
            elif t == 'Rad':
                result = m.radians(num)
            elif t == 'Abs':
                result = abs(num)
            elif t == 'Exp':
                result = m.exp(num)
            elif t == 'Mod':
                self.input_var.set(self.input_var.get() + '%')
                return
            elif t == '(+/-)':
                self.input_var.set(str(-num))
                return
            if result is not None:
                self.output_var.set(str(result))
        except Exception:
            self.output_var.set("Error")

if __name__ == "__main__":
    app = BasicAndScientific()
    app.mainloop()