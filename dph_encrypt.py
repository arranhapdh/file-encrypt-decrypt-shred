import customtkinter as tk
from customtkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

class CustomFileEncryptorDecryptor:
    def __init__(self):
        self.key_file = "encryption_key.key"
        self.key = None
        self.cipher = None
        self.input_file = None
        self.output_file = None
        self.input_dir = None
        self.output_dir = None
        self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def save_key(self):
        if self.key:
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            messagebox.showinfo("Success", "Encryption key saved successfully!")
        else:
            messagebox.showerror("Error", "No encryption key found!")

    def import_key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                self.key = f.read()
                self.cipher = Fernet(self.key)
                messagebox.showinfo("Success", "Encryption key imported successfully!")
        else:
            messagebox.showerror("Error", "No file selected!")

    def select_file(self):
        self.input_file = filedialog.askopenfilename()
        return self.input_file

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".encrypted")
        return self.output_file

    def select_directory(self):
        self.input_dir = filedialog.askdirectory()
        return self.input_dir

    def select_output_directory(self):
        self.output_dir = filedialog.askdirectory()
        return self.output_dir

    def encrypt_file(self):
        self.select_file()
        if self.input_file:
            self.select_output_file()
            if self.output_file:
                try:
                    with open(self.input_file, 'rb') as f:
                        data = f.read()
                        encrypted_data = self.cipher.encrypt(data)
                    with open(self.output_file, 'wb') as f:
                        f.write(encrypted_data)
                    messagebox.showinfo("Success", "File encrypted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def decrypt_file(self):
        self.select_file()
        if self.input_file:
            self.select_output_file()
            if self.output_file:
                try:
                    with open(self.input_file, 'rb') as f:
                        data = f.read()
                        decrypted_data = self.cipher.decrypt(data)
                    with open(self.output_file, 'wb') as f:
                        f.write(decrypted_data)
                    messagebox.showinfo("Success", "File decrypted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Decryption failed: {str(e)}")

    def batch_encrypt_files(self):
        self.select_directory()
        if self.input_dir:
            self.select_output_directory()
            if self.output_dir:
                try:
                    for filename in os.listdir(self.input_dir):
                        if os.path.isfile(os.path.join(self.input_dir, filename)):
                            input_file = os.path.join(self.input_dir, filename)
                            output_file = os.path.join(self.output_dir, filename + '.encrypted')
                            with open(input_file, 'rb') as f:
                                data = f.read()
                                encrypted_data = self.cipher.encrypt(data)
                            with open(output_file, 'wb') as f:
                                f.write(encrypted_data)
                    messagebox.showinfo("Success", "Batch encryption completed!")
                except Exception as e:
                    messagebox.showerror("Error", f"Batch encryption failed: {str(e)}")

    def batch_decrypt_files(self):
        self.select_directory()
        if self.input_dir:
            self.select_output_directory()
            if self.output_dir:
                try:
                    for filename in os.listdir(self.input_dir):
                        if os.path.isfile(os.path.join(self.input_dir, filename)):
                            input_file = os.path.join(self.input_dir, filename)
                            output_file = os.path.join(self.output_dir, filename[:-10])  # remove '.encrypted' from filename
                            with open(input_file, 'rb') as f:
                                data = f.read()
                                decrypted_data = self.cipher.decrypt(data)
                            with open(output_file, 'wb') as f:
                                f.write(decrypted_data)
                    messagebox.showinfo("Success", "Batch decryption completed!")
                except Exception as e:
                    messagebox.showerror("Error", f"Batch decryption failed: {str(e)}")

    def shred_file(self):
        self.select_file()
        if self.input_file:
            try:
                with open(self.input_file, 'rb+') as f:
                    length = f.tell()
                    f.seek(0)
                    f.write(os.urandom(length))
                os.remove(self.input_file)
                messagebox.showinfo("Success", "File shredded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"File shredding failed: {str(e)}")

    def show_about_dialog(self):
        messagebox.showinfo("About", "Custom File Encryptor/Decryptor\nVersion 1.0\n\nDeveloped by DPH Security")

def create_custom_gui():
    root = tk.CTk()
    root.title("File Encryptor/Decryptor")

    label = tk.CTkLabel(root, text="Select an operation:")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    encrypt_button = tk.CTkButton(root, text="Encrypt File", command=app.encrypt_file)
    encrypt_button.grid(row=1, column=0, pady=5, padx=5)

    decrypt_button = tk.CTkButton(root, text="Decrypt File", command=app.decrypt_file)
    decrypt_button.grid(row=1, column=1, pady=5, padx=5)

    batch_encrypt_button = tk.CTkButton(root, text="Batch Encrypt Files", command=app.batch_encrypt_files)
    batch_encrypt_button.grid(row=2, column=0, pady=5, padx=5)

    batch_decrypt_button = tk.CTkButton(root, text="Batch Decrypt Files", command=app.batch_decrypt_files)
    batch_decrypt_button.grid(row=2, column=1, pady=5, padx=5)

    shred_button = tk.CTkButton(root, text="Shred File", command=app.shred_file)
    shred_button.grid(row=3, column=0, pady=5, padx=5)

    about_button = tk.CTkButton(root, text="About", command=app.show_about_dialog)
    about_button.grid(row=3, column=1, pady=5, padx=5)

    save_key_button = tk.CTkButton(root, text="Save Encryption Key", command=app.save_key)
    save_key_button.grid(row=4, column=0, pady=5, padx=5)

    import_key_button = tk.CTkButton(root, text="Import Encryption Key", command=app.import_key)
    import_key_button.grid(row=4, column=1, pady=5, padx=5)

    root.mainloop()

def main():
    global app
    app = CustomFileEncryptorDecryptor()
    create_custom_gui()

if __name__ == "__main__":
    main()
