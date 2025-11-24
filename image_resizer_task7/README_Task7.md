# Task 7 — Image Resizer Tool

Objective: Resize and convert images in batch using Python and Pillow (PIL).

Files included:
- image_resizer.py — CLI script to resize and convert images in a folder (recurses subfolders).
- input_images/ — sample input images for testing.
- resized_images/ — output folder for resized images.
- image_resizer_task7.zip — zip package of the tool.

How to run:
1. Create virtual env and install Pillow if not installed:
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install Pillow

2. Run example:
   python image_resizer.py --input ./input_images --output ./resized_images --width 800 --height 600

Reference: Task brief uploaded by you: `/mnt/data/task 7.pdf`. fileciteturn2file0
