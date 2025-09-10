# Image Metadata Manager
<img width="1385" height="834" alt="Screenshot from 2025-09-10 19-24-30" src="https://github.com/user-attachments/assets/5b1925ab-13be-4e47-beeb-790254a7b409" />

A Python GUI application for managing image metadata with drag-and-drop functionality. This tool allows you to remove metadata from images, add new metadata, and process images in bulk.

## Features

- **Drag & Drop Interface**: Easy-to-use interface for loading images
- **Bulk Processing**: Handle multiple images at once
- **Metadata Removal**: Strip all metadata from images
- **Metadata Addition**: Add custom metadata to images
- **Multiple Save Options**: Save to new folder, overwrite originals, or choose custom location
- **Progress Tracking**: Real-time progress bar and status updates
- **Supported Formats**: JPEG, PNG, TIFF, BMP, GIF

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- Pillow (PIL)
- piexif (for advanced EXIF handling)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python metadata_manager.py
```

2. **Load Images**:
   - Click the "Drag & Drop Images Here" area and select "Browse Files"
   - Or use the "Browse Files" button
   - Multiple images can be selected at once

3. **View Metadata**:
   - Click on any image in the file list to view its current metadata
   - The metadata will be displayed in the right panel

4. **Remove Metadata**:
   - Click "Remove All Metadata" to strip metadata from all loaded images
   - This creates clean copies without any EXIF data

5. **Add Metadata**:
   - Click "Add/Edit Metadata" to open the metadata editor
   - Fill in the desired fields (Title, Artist, Copyright, Software, Comment)
   - Click "Apply" to set the metadata for all images

6. **Save Images**:
   - Choose save option:
     - **New Folder**: Creates a "processed_images" folder
     - **Overwrite Original**: Replaces the original files
     - **Custom Path**: Choose your own save location
   - Click "Save Processed Images"

## Metadata Fields

The application supports the following metadata fields:

- **Title**: Image description/title
- **Artist**: Creator/photographer name
- **Copyright**: Copyright information
- **Software**: Software used to create/edit the image
- **Comment**: Additional comments

## File Formats

- **JPEG/JPG**: Full metadata support (EXIF data)
- **PNG**: Basic metadata support
- **TIFF**: Basic metadata support
- **BMP**: Basic metadata support
- **GIF**: Basic metadata support

## Notes

- The application processes images in memory to prevent data loss
- Original files are never modified unless "Overwrite Original" is selected
- Progress bars show real-time processing status
- All operations are performed in separate threads to keep the UI responsive

## Troubleshooting

1. **Import Error**: Make sure all dependencies are installed:
   ```bash
   pip install Pillow piexif
   ```

2. **File Access Error**: Ensure you have read/write permissions for the image files and directories

3. **Memory Issues**: For very large images or bulk processing, close other applications to free up memory

## License

This project is open source and available under the MIT License.
