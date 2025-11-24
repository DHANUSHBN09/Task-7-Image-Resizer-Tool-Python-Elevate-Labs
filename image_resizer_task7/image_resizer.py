"""Image Resizer Tool (Task 7)

Usage (CLI):
  python image_resizer.py --input ./input_images --output ./resized_images --width 800 --height 600 --format PNG --quality 85 --keep-aspect True --suffix _resized
"""

import os
import argparse
from PIL import Image, UnidentifiedImageError

SUPPORTED_EXT = ('.jpg','.jpeg','.png','.bmp','.gif','.tiff','.webp')

def process_image(in_path, out_path, target_size, keep_aspect=True, out_format=None, quality=85):
    try:
        with Image.open(in_path) as im:
            # convert RGBA to RGB for JPEG
            if out_format and out_format.upper() in ('JPG','JPEG') and im.mode in ('RGBA','LA'):
                background = Image.new('RGB', im.size, (255,255,255))
                background.paste(im, mask=im.split()[-1])
                im = background
            if keep_aspect:
                im.thumbnail(target_size, Image.LANCZOS)
            else:
                im = im.resize(target_size, Image.LANCZOS)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            save_kwargs = {}
            fmt = out_format if out_format else im.format
            if fmt:
                fmt = fmt.upper()
                if fmt in ('JPG','JPEG'):
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                    fmt = 'JPEG'
            try:
                im.save(out_path, format=fmt, **save_kwargs)
            except TypeError:
                im.save(out_path)
            return True, None
    except UnidentifiedImageError as e:
        return False, f'UnidentifiedImageError: {e}'
    except Exception as e:
        return False, str(e)

def is_image_file(path):
    return path.lower().endswith(SUPPORTED_EXT)

def main():
    parser = argparse.ArgumentParser(description='Batch image resizer (Task 7)')
    parser.add_argument('--input', '-i', required=True, help='Input folder (recursed)')
    parser.add_argument('--output', '-o', required=True, help='Output folder')
    parser.add_argument('--width', type=int, default=800, help='Target width (px)')
    parser.add_argument('--height', type=int, default=600, help='Target height (px)')
    parser.add_argument('--format', '-f', default=None, help='Output image format (PNG, JPEG, WEBP)')
    parser.add_argument('--quality', type=int, default=85, help='JPEG quality (1-100)')
    parser.add_argument('--keep-aspect', type=lambda x: (str(x).lower() == 'true'), default=True, help='Keep aspect ratio? True/False')
    parser.add_argument('--suffix', default='_resized', help='Suffix for output filenames before extension')
    args = parser.parse_args()

    input_root = os.path.abspath(args.input)
    output_root = os.path.abspath(args.output)
    target_size = (args.width, args.height)
    total = 0
    success = 0
    errors = []

    for dirpath, dirnames, filenames in os.walk(input_root):
        rel = os.path.relpath(dirpath, input_root)
        for fname in filenames:
            if not is_image_file(fname):
                continue
            total += 1
            in_file = os.path.join(dirpath, fname)
            name, ext = os.path.splitext(fname)
            out_ext = ('.' + (args.format.lower() if args.format else ext.lstrip('.')))
            out_fname = name + args.suffix + out_ext
            out_dir = os.path.join(output_root, rel) if rel!='.' else output_root
            out_file = os.path.join(out_dir, out_fname)
            ok, err = process_image(in_file, out_file, target_size, keep_aspect=args.keep_aspect, out_format=args.format, quality=args.quality)
            if ok:
                success += 1
                print(f'OK: {in_file} -> {out_file}')
            else:
                errors.append((in_file, err))
                print(f'ERR: {in_file} -> {err}')

    print('\nSummary:')
    print(f'  Total images found: {total}')
    print(f'  Successfully processed: {success}')
    print(f'  Errors: {len(errors)}')
    if errors:
        for p,e in errors:
            print(f'    {p}: {e}')

if __name__ == '__main__':
    main()
