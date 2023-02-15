import tkinter as tk

#main user interface for the server
class ServerWindow(tk.Frame):

    #sets up the window
    def __init__(self, parent):
        #set up the frame
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        #configure the window and make the widgets
        self.configure_gui()
        self.create_widgets()

    #configures the window for use
    def configure_gui(self):
        #window properties
        self.parent.geometry("400x200")
        self.parent.resizable(False, False)
        
        #configure the close protocol
        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    #fills the frame with the required widgets
    def create_widgets(self):
        pass

    #called when the window is to be closed
    def close_window(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    window = ServerWindow(root)
    root.mainloop()