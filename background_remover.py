import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar  # Import Progressbar from tkinter.ttk
from rembg import remove
from PIL import Image, ImageTk
import io
import time
import webbrowser

# Function to remove background from a single image
def remove_background(input_path, output_path):
    try:
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)
            
            # Save the processed image
            output_image = Image.open(io.BytesIO(output_data))
            output_image.save(output_path)
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


# Function to process batch of images
def batch_process_images(input_folder, output_folder, progress_var, status_label):
    # Get all image files from the folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]
    total_files = len(image_files)
    
    # Process each image
    for i, image_file in enumerate(image_files):
        input_image_path = os.path.join(input_folder, image_file)
        output_image_path = os.path.join(output_folder, f"processed_{image_file}")
        
        success = remove_background(input_image_path, output_image_path)
        
        # Update progress
        progress_var.set((i + 1) / total_files * 100)
        status_label.config(text=f"Processing {i+1}/{total_files} images...")
        time.sleep(0.1)  # Simulate processing time for smooth UI update

    messagebox.showinfo("Batch Processing Complete", "All images have been processed successfully!")


# GUI Code using Tkinter
class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover Tool")
        self.root.geometry("800x600")  # Set initial size for large screen
        self.root.resizable(True, True)  # Allow resizing
        self.root.config(bg="#f5f5f5")  # Light background color
        
        # Add title label with improved font
        self.title_label = Label(root, text="Background Remover Tool 1.0", font=("Arial", 24, "bold"), bg="#f5f5f5")
        self.title_label.pack(pady=20)

        # Create a frame for buttons
        self.button_frame = Frame(root, bg="#f5f5f5")
        self.button_frame.pack(pady=20)

        # Single Image Processing Button
        self.process_single_button = Button(self.button_frame, text="Process Single Image", command=self.process_single_image, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.process_single_button.grid(row=0, column=0, padx=10, pady=10)

        # Batch Processing Button
        self.process_batch_button = Button(self.button_frame, text="Process Batch Images", command=self.process_batch_images, width=20, height=2, bg="#2196F3", fg="white", font=("Arial", 14))
        self.process_batch_button.grid(row=0, column=1, padx=10, pady=10)

        # Progress bar and status label
        self.progress_var = DoubleVar()
        self.progress_bar = Progressbar(root, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.pack(pady=20)

        self.status_label = Label(root, text="Choose an option to start", font=("Arial", 12), bg="#f5f5f5")
        self.status_label.pack()

        # Exit Button
        self.exit_button = Button(root, text="Exit", command=root.quit, width=20, height=2, bg="#f44336", fg="white", font=("Arial", 14))
        self.exit_button.pack(pady=20)

        # Developer Support Button
        self.support_button = Button(root, text="Contact Support", command=self.contact_support, width=20, height=2, bg="#FFC107", fg="white", font=("Arial", 14))
        self.support_button.pack(pady=10)

        # Developer Details - Positioned at the bottom
        self.developer_details_frame = Frame(root, bg="#f5f5f5", pady=10)
        self.developer_details_frame.pack(side=BOTTOM, fill=X)

        self.developer_details_label = Label(self.developer_details_frame, text="Developer: Ambarish Mandal\nEmail: dev.ambarish.ofc@gmail.com\nVersion: 1.0", 
                                              font=("Arial", 12), bg="#f5f5f5")
        self.developer_details_label.pack()

    # Function to process single image
    def process_single_image(self):
        # Select an image file
        input_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_file:
                if remove_background(input_file, output_file):
                    messagebox.showinfo("Success", f"Background removed successfully! Saved as {output_file}")
                else:
                    messagebox.showerror("Error", "Failed to remove background from the image.")
    
    # Function to process batch images
    def process_batch_images(self):
        input_folder = filedialog.askdirectory(title="Select Input Folder")
        if input_folder:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            if output_folder:
                # Start batch processing in a separate thread for better UI responsiveness
                threading.Thread(target=batch_process_images, args=(input_folder, output_folder, self.progress_var, self.status_label), daemon=True).start()

    # Function to contact developer support
    def contact_support(self):
        # This will open the default email client with pre-filled email to support
        webbrowser.open("mailto:dev.ambarish.ofc@gmail.com?subject=Support Request&body=Hello, I need assistance with the Background Remover Tool.")


# Main function to run the app
def run_app():
    root = Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
