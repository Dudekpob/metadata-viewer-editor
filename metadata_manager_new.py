import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import json
from pathlib import Path
import threading

class ImageMetadataManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Metadata Manager")
        self.window.geometry("1400x800")
        
        # Set styles
        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Helvetica', 11))
        style.configure("TLabel", font=('Helvetica', 11))
        style.configure("Info.TFrame", padding=20, relief="solid", borderwidth=2)
        style.configure("DropZone.TFrame", padding=10, relief="solid", borderwidth=2)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image list to store loaded images
        self.image_list = []
        self.current_image = None
        
        # Setup file drag & drop
        self.window.drop_target_register = lambda *args: None  # Dummy function
        self.window.bind('<B1-Motion>', self.on_drag)
        self.window.bind('<ButtonRelease-1>', self.on_drop)
        
        # Create and configure widgets
        self.create_widgets()
        
        # Create and configure widgets
        self.create_widgets()
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
    def create_widgets(self):
        # Create left panel for file list
        self.left_panel = ttk.Frame(self.main_frame, padding="10")
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # File list frame
        self.file_list_frame = ttk.LabelFrame(self.left_panel, text="Image Files", padding="10")
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create listbox for files
        self.file_listbox = tk.Listbox(self.file_list_frame, width=40, height=15, font=('Courier', 10))
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select_file)
        
        # Scrollbar for listbox
        listbox_scrollbar = ttk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.configure(yscrollcommand=listbox_scrollbar.set)
        
        # Buttons for file operations
        self.file_buttons_frame = ttk.Frame(self.left_panel)
        self.file_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(self.file_buttons_frame, text="Add Images", command=self.add_images).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.file_buttons_frame, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.file_buttons_frame, text="Clear All", command=self.clear_files).pack(side=tk.LEFT, padx=2)
        
        # Create right panel for metadata
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Metadata frame
        self.metadata_frame = ttk.LabelFrame(self.right_panel, text="Image Metadata", padding="10")
        self.metadata_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create metadata text widget with better styling
        self.metadata_text = scrolledtext.ScrolledText(
            self.metadata_frame, 
            wrap=tk.WORD, 
            width=80,
            height=30,
            font=('Courier', 10),
            bg='#f8f9fa',
            padx=10,
            pady=10
        )
        self.metadata_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons for metadata operations
        self.metadata_buttons_frame = ttk.Frame(self.right_panel)
        self.metadata_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(self.metadata_buttons_frame, text="Save Changes", command=self.save_changes).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.metadata_buttons_frame, text="Export Metadata", command=self.export_metadata).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.metadata_buttons_frame, text="Clear", command=self.clear_metadata).pack(side=tk.LEFT, padx=2)
        
        # Configure grid weights for panels
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
            
    def add_images(self):
        """Open file dialog to select images"""
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_paths:
            self.add_image_paths(file_paths)
    
    def add_image_paths(self, paths):
        """Add multiple image paths to the list"""
        for path in paths:
            if path and path not in self.image_list:
                self.image_list.append(path)
                self.file_listbox.insert(tk.END, os.path.basename(path))
    
    def on_drag(self, event):
        """Handle file drag"""
        pass

    def on_drop(self, event):
        """Handle file drop"""
        # Get clipboard content (might contain dropped files)
        try:
            data = self.window.clipboard_get()
            if data and os.path.exists(data):
                # Check if it's an image file
                ext = os.path.splitext(data)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.tiff', '.bmp'):
                    self.add_image_paths([data])
                else:
                    messagebox.showwarning("Warning", 
                        "Please drop only image files (PNG, JPG, JPEG, TIFF, BMP)")
        except:
            pass  # Clipboard was empty or invalid
            
    def remove_selected(self):
        selection = self.file_listbox.curselection()
        if selection:
            idx = selection[0]
            self.file_listbox.delete(idx)
            self.image_list.pop(idx)
            if self.current_image == self.image_list[idx]:
                self.current_image = None
                self.clear_metadata()
                
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.image_list.clear()
        self.current_image = None
        self.clear_metadata()
        
    def on_select_file(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            idx = selection[0]
            self.current_image = self.image_list[idx]
            self.display_metadata(self.current_image)
            
    def display_metadata(self, image_path):
        try:
            # Close any existing image to ensure fresh read
            Image.open(image_path).close()
            
            # Open the image again to read metadata
            with Image.open(image_path) as img:
                self.metadata_text.delete(1.0, tk.END)
                self.metadata_text.insert(tk.END, f"File: {os.path.basename(image_path)}\n")
                self.metadata_text.insert(tk.END, f"Size: {img.size}\n")
                self.metadata_text.insert(tk.END, f"Format: {img.format}\n")
                self.metadata_text.insert(tk.END, f"Mode: {img.mode}\n\n")

                prompt_found = False

                # JPEG: look for UserComment in EXIF
                if img.format in ["JPEG", "JPG"]:
                    exif_data = img._getexif()
                    if exif_data:
                        self.metadata_text.insert(tk.END, "EXIF Data:\n")
                        self.metadata_text.insert(tk.END, "-" * 40 + "\n")
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            if tag == "UserComment":
                                prompt_found = True
                                # Handle bytes and string formats
                                if isinstance(value, bytes):
                                    try:
                                        value = value.decode('utf-8')
                                    except:
                                        try:
                                            value = value.decode('ascii')
                                        except:
                                            value = str(value)
                                self.metadata_text.insert(tk.END, f"PROMPT (UserComment):\n{value}\n\n")
                            self.metadata_text.insert(tk.END, f"{tag}: {value}\n")
                    else:
                        self.metadata_text.insert(tk.END, "No EXIF data found\n")

                # PNG: look for parameters (prompt)
                elif img.format == "PNG":
                    pnginfo = img.text if hasattr(img, 'text') else img.info
                    if pnginfo and len(pnginfo) > 0:
                        self.metadata_text.insert(tk.END, "PNG Metadata:\n")
                        self.metadata_text.insert(tk.END, "-" * 40 + "\n")
                        
                        # First try to parse workflow and prompt data
                        try:
                            if "prompt" in pnginfo:
                                workflow_data = json.loads(pnginfo["prompt"])
                                prompt_found = True
                                
                                # Extract positive prompts from nodes
                                for node_id, node in workflow_data.items():
                                    if node.get("class_type") in ["CLIPTextEncode", "PromptSchedule"]:
                                        if "inputs" in node and "text" in node["inputs"]:
                                            self.metadata_text.insert(tk.END, f"PROMPT (Node {node_id}):\n")
                                            self.metadata_text.insert(tk.END, f"{node['inputs']['text']}\n\n")
                                        elif "widgets_values" in node and node["widgets_values"]:
                                            self.metadata_text.insert(tk.END, f"PROMPT (Node {node_id}):\n")
                                            self.metadata_text.insert(tk.END, f"{node['widgets_values'][0]}\n\n")
                            
                            # Look for traditional parameters
                            if "parameters" in pnginfo:
                                prompt_found = True
                                self.metadata_text.insert(tk.END, "PROMPT (parameters):\n")
                                self.metadata_text.insert(tk.END, f"{pnginfo['parameters']}\n\n")
                        except json.JSONDecodeError:
                            pass
                        
                        # Then display all metadata
                        self.metadata_text.insert(tk.END, "All Metadata:\n")
                        self.metadata_text.insert(tk.END, "-" * 40 + "\n")
                        for k, v in pnginfo.items():
                            # Try to format JSON data nicely
                            try:
                                if isinstance(v, str) and (v.startswith('{') or v.startswith('[')):
                                    parsed_v = json.loads(v)
                                    v = json.dumps(parsed_v, indent=2)
                            except json.JSONDecodeError:
                                pass
                            self.metadata_text.insert(tk.END, f"{k}:\n{v}\n\n")
                    else:
                        self.metadata_text.insert(tk.END, "No PNG metadata found\n")

                # TIFF/BMP/GIF: standard metadata
                else:
                    exif_data = img.info.get('exif')
                    if exif_data:
                        self.metadata_text.insert(tk.END, "EXIF Data:\n")
                        self.metadata_text.insert(tk.END, "-" * 40 + "\n")
                        self.metadata_text.insert(tk.END, str(exif_data) + "\n")
                    else:
                        self.metadata_text.insert(tk.END, "No metadata found\n")

                if not prompt_found:
                    self.metadata_text.insert(tk.END, "\nNo prompt found in metadata.\n")
                    
        except Exception as e:
            self.metadata_text.delete(1.0, tk.END)
            self.metadata_text.insert(tk.END, f"Error reading metadata: {str(e)}")
            
    def save_changes(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        try:
            with Image.open(self.current_image) as img:
                # Create a new image with the same mode and size
                new_image = img.copy()
                
                # Get metadata text and parse it
                metadata_text = self.metadata_text.get(1.0, tk.END)
                lines = metadata_text.split('\n')
                
                # For PNG files
                if img.format == 'PNG':
                    # Create a new PngInfo object
                    from PIL.PngImagePlugin import PngInfo
                    metadata = PngInfo()
                    
                    # First check the text attribute, then fall back to info
                    source_metadata = img.text if hasattr(img, 'text') and img.text else img.info
                    
                    # Copy all existing metadata
                    for k, v in source_metadata.items():
                        if k != 'parameters':  # We'll handle this separately
                            try:
                                metadata.add_text(str(k), str(v))
                            except Exception as e:
                                print(f"Warning: Could not add metadata {k}: {e}")
                    
                    # Get the entire metadata text for parameters
                    current_text = ""
                    capture_next = False
                    for line in lines:
                        if "PROMPT (parameters):" in line or "parameters:" in line:
                            capture_next = True
                            continue
                        elif capture_next and line.strip():
                            if not line.startswith("-"):
                                current_text = line.strip()
                                break
                    
                    if current_text:
                        print(f"Setting new parameters: {current_text}")  # Debug print
                        metadata.add_text("parameters", current_text)
                    
                    # Make sure we're using the metadata when saving
                    new_image = img.copy()
                    new_image.info = {}
                
                elif img.format in ['JPEG', 'JPG']:
                    # Parse metadata text for JPEG
                    in_usercomment_section = False
                    usercomment_lines = []
                    
                    for line in lines:
                        if "PROMPT (UserComment):" in line:
                            in_usercomment_section = True
                            continue
                        elif in_usercomment_section and line.strip() and not line.startswith("-"):
                            usercomment_lines.append(line.strip())
                        elif in_usercomment_section and not line.strip():
                            in_usercomment_section = False
                    
                    if usercomment_lines:
                        prompt = "\n".join(usercomment_lines)
                        # Get existing EXIF or create new
                        exif_dict = new_image.info.get('exif', {})
                        if not exif_dict:
                            exif_dict = {}
                        
                        # Find UserComment tag ID
                        user_comment_tag = None
                        for tag_id, tag_name in TAGS.items():
                            if tag_name == 'UserComment':
                                user_comment_tag = tag_id
                                break
                        
                        if user_comment_tag:
                            exif_dict[user_comment_tag] = prompt.encode('utf-8')
                            new_image.info['exif'] = exif_dict
                
                # Ask user where to save the modified image
                save_path = filedialog.asksaveasfilename(
                    initialfile=os.path.basename(self.current_image),
                    defaultextension=f".{img.format.lower()}",
                    filetypes=[
                        (f"{img.format} files", f"*.{img.format.lower()}"),
                        ("All files", "*.*")
                    ]
                )
                
                if save_path:
                    if img.format == 'PNG':
                        # Parse the current text to find any changes
                        sections = {}
                        current_section = None
                        current_content = []
                        
                        for line in lines:
                            if line.strip().endswith(':'):
                                if current_section and current_content:
                                    sections[current_section] = '\n'.join(current_content).strip()
                                current_section = line.strip()[:-1]
                                current_content = []
                            elif line.strip() and not line.startswith('-' * 10):
                                if current_section:
                                    current_content.append(line.strip())
                        
                        if current_section and current_content:
                            sections[current_section] = '\n'.join(current_content).strip()
                        
                        # Create new PngInfo object
                        new_metadata = PngInfo()
                        
                        # First, preserve original workflow data if it exists
                        if 'prompt' in img.info:
                            try:
                                workflow = json.loads(img.info['prompt'])
                                # Update workflow with any changes from sections
                                for section, content in sections.items():
                                    if section.startswith('PROMPT (Node '):
                                        node_id = section.split('Node ')[1].split(')')[0]
                                        if node_id in workflow:
                                            if 'inputs' in workflow[node_id] and 'text' in workflow[node_id]['inputs']:
                                                workflow[node_id]['inputs']['text'] = content
                                            elif 'widgets_values' in workflow[node_id]:
                                                workflow[node_id]['widgets_values'][0] = content
                                new_metadata.add_text('prompt', json.dumps(workflow))
                            except json.JSONDecodeError:
                                # If workflow parse failed, preserve original
                                new_metadata.add_text('prompt', img.info['prompt'])
                        
                        # Add all other metadata
                        for key, value in img.info.items():
                            if key != 'prompt':  # Skip prompt as we handled it above
                                try:
                                    new_metadata.add_text(str(key), str(value))
                                except Exception as e:
                                    print(f"Warning: Could not preserve metadata {key}: {e}")
                        
                        # Clear the image info and save with new metadata
                        new_image.info = {}
                        new_image.save(save_path, format='PNG', pnginfo=new_metadata, optimize=False)
                        print(f"Saved image with metadata: {new_metadata.text if hasattr(new_metadata, 'text') else new_metadata}")
                    else:
                        # Save other formats
                        new_image.save(save_path, format=img.format)
                    
                    # Force close all images
                    new_image.close()
                    img.close()
                    
                    # Force reload the image to verify metadata
                    with Image.open(save_path) as verify_img:
                        print(f"Verified metadata after save: {verify_img.info}")  # Debug print
                    
                    # Update the list if it's a new file
                    if save_path not in self.image_list:
                        self.image_list.append(save_path)
                        self.file_listbox.insert(tk.END, os.path.basename(save_path))
                    
                    # Update current image and display
                    self.current_image = save_path
                    
                    # Select the new file in the listbox
                    idx = self.image_list.index(save_path)
                    self.file_listbox.selection_clear(0, tk.END)
                    self.file_listbox.selection_set(idx)
                    self.file_listbox.see(idx)
                    
                    # Wait a moment to ensure file is written
                    self.window.after(100, lambda: self.display_metadata(save_path))
                    
                    messagebox.showinfo("Success", "Image saved with updated metadata")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
        
    def export_metadata(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                metadata = self.metadata_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(metadata)
                messagebox.showinfo("Success", "Metadata exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export metadata: {str(e)}")
        
    def clear_metadata(self):
        self.metadata_text.delete(1.0, tk.END)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageMetadataManager()
    app.run()
