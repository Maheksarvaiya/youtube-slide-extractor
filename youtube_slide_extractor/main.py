import tkinter as tk  # Imports the tkinter library for GUI components
from tkinter import messagebox  # For showing popup alert messages
from extractor import download_video, extract_slides  # Importing functions from our own extractor.py file
class SlideExtractorApp:  # Creating a class to organize our GUI
    def __init__(self, root):  # Constructor that takes the main tkinter window
        self.root = root
        root.title("YouTube Slide Extractor")  # Sets window title
        root.geometry("600x400")  # Sets window size (Width x Height)

        # Label above the text input
        tk.Label(root, text="Enter YouTube URL:").pack(pady=10)

        # Textbox to enter the URL
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        # A label to show status (e.g., "Downloading...", "Done!")
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=10)

        # Button that triggers the download + extraction
        tk.Button(root, text="Start Extraction", command=self.start_process).pack()


    def start_process(self):  # Function called when the button is clicked
        url = self.url_entry.get().strip()  # Get the URL from the textbox

        if not url:  # If empty, show an error popup
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        try:
            self.status_label.config(text="Downloading video")  # Update the status label
            self.root.update_idletasks()  # ✅ Force GUI to update
            video_path= download_video(url)  # Download video and get file path
            self.status_label.config(text="Extracting slides")  # Update status
            extract_slides(video_path)  # Extract slides and save them
            self.status_label.config(text="Done! Slides saved in 'frames' folder.")  # Done!
        except Exception as e:  # If error occurs, show popup
            self.status_label.config(text="Error occurred.")
            messagebox.showerror("Error", str(e))
# Main starting point of the script
if __name__ == "__main__":
    print("Starting GUI...")  # Debug print
    root = tk.Tk()  # Create the main window
    app = SlideExtractorApp(root)  # Create an instance of the app
    root.mainloop()  # Run the app loop (keeps window open)

