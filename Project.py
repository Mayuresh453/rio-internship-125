import language_tool_python
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class GrammarCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Grammar Checker")
        self.root.geometry("800x700")
        self.setup_ui()
        self.tool = language_tool_python.LanguageTool('en-US')
        
    def setup_ui(self):
        """Set up the user interface"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Enter Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_input = ScrolledText(
            input_frame, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            height=15,
            padx=10,
            pady=10
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Check Grammar", 
            command=self.check_grammar,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Clear Text", 
            command=self.clear_text
        ).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Grammar Check Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            height=15,
            padx=10,
            pady=10,
            state='disabled'
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        """Configure custom widget styles"""
        style = ttk.Style()
        style.configure("Accent.TButton", 
                       foreground="white", 
                       background="#4CAF50",
                       font=("Arial", 11, "bold"))
        
    def check_grammar(self):
        """Check the text for grammatical errors"""
        input_text = self.text_input.get("1.0", tk.END).strip()
        
        if not input_text:
            self.show_message("Please enter some text to check.", "warning")
            return
            
        if len(input_text.split()) < 3:
            self.show_message("Please enter at least 3 words for meaningful analysis.", "info")
            return
            
        try:
            self.status_var.set("Checking grammar...")
            self.root.update()
            
            matches = self.tool.check(input_text)
            
            if not matches:
                self.display_results("No grammatical errors detected.", "success")
            else:
                error_details = []
                for i, match in enumerate(matches, 1):
                    error_details.append(
                        f"ERROR {i}:\n"
                        f"Context: {match.context}\n"
                        f"Type: {match.ruleId}\n"
                        f"Message: {match.message}\n"
                        f"Suggestions: {', '.join(match.replacements) if match.replacements else 'None'}\n"
                        f"{'-'*60}\n"
                    )
                self.display_results("".join(error_details))
                
            self.status_var.set("Grammar check completed")
            
        except Exception as e:
            self.show_message(f"An error occurred: {str(e)}", "error")
            self.status_var.set("Error during grammar check")
            
    def display_results(self, text, message_type=None):
        """Display the results in the results text widget"""
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        
        if message_type == "success":
            self.result_text.tag_config("success", foreground="green")
            self.result_text.insert(tk.END, text, "success")
        else:
            self.result_text.insert(tk.END, text)
            
        self.result_text.config(state='disabled')
        
    def clear_text(self):
        """Clear the input and result text widgets"""
        self.text_input.delete(1.0, tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')
        self.status_var.set("Ready")
        
    def show_message(self, message, message_type="info"):
        """Show a message to the user"""
        if message_type == "error":
            messagebox.showerror("Error", message)
        elif message_type == "warning":
            messagebox.showwarning("Warning", message)
        else:
            messagebox.showinfo("Information", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = GrammarCheckerApp(root)
    root.mainloop()