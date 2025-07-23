# Pallet Tinder Web App

This project provides a simple web application for sorting images of pallets into categories using a Tinder-like interface. It is built with Flask and allows users to quickly classify images as 'Good', 'Bad', or 'Unknown' by clicking buttons or using keyboard shortcuts.

## Features
- Web interface to review and sort images from a folder
- Classify each image as Good, Bad, or Unknown
- Images are moved to corresponding folders based on classification
- Progress is tracked so already sorted images are not shown again
- Keyboard shortcuts: Left arrow (Bad), Right arrow (Good), Up arrow (Unknown)

## How It Works
- Place your images in the `Pallet_images` folder.
- Start the Flask web server by running `python image_tinder_web.py`.
- Open your browser and go to `http://localhost:5000`.
- The app will show one image at a time. Classify each image using the buttons or keyboard shortcuts.
- Sorted images are moved to `GoodPallet`, `BadPallet`, or `UnknownPallet` folders.
- The app keeps track of sorted images in `sorted_images.txt` so you don't see the same image twice.

## Setup
1. Make sure you have Python 3 installed.
2. Install Flask:
   ```bash
   pip install flask
   ```
3. Place your images in the `Pallet_images` directory (create it if it doesn't exist).
4. Run the app:
   ```bash
   python image_tinder_web.py
   ```
5. Visit [http://localhost:5000](http://localhost:5000) in your browser.

## File Structure
- `image_tinder_web.py`: Main Flask app
- `Pallet_images/`: Folder containing images to be sorted
- `GoodPallet/`, `BadPallet/`, `UnknownPallet/`: Folders for sorted images
- `sorted_images.txt`: Tracks which images have been sorted

## Notes
- The app will automatically create the necessary folders if they do not exist.
- Only image files with extensions `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp` are supported.
- You can stop and restart the app at any time; progress will be saved.
