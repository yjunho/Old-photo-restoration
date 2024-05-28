import zipfile
import os
import shutil
from PIL import Image, ImageOps
from tqdm import tqdm

# Set paths for the zip files
train_zip_path = '/root/IGNN-master/Train.zip'
test_zip_path = '/root/IGNN-master/Test.zip'

# Set paths for extraction
train_extract_path = 'train_extracted'
test_extract_path = 'test_extracted'

# Step 1: Unzip the provided files
print("Unzipping train and test files...")
with zipfile.ZipFile(train_zip_path, 'r') as zip_ref:
    zip_ref.extractall(train_extract_path)

with zipfile.ZipFile(test_zip_path, 'r') as zip_ref:
    zip_ref.extractall(test_extract_path)

# Step 2: Create necessary directories
div2k_base_path = '/root/IGNN-master/DIV2K'
train_hr_path = os.path.join(div2k_base_path, 'DIV2K_train_HR_sub')
train_lr_x2_path = os.path.join(div2k_base_path, 'DIV2K_train_LR_bicubic_sub/x2')
train_lr_x3_path = os.path.join(div2k_base_path, 'DIV2K_train_LR_bicubic_sub/x3')
train_lr_x4_path = os.path.join(div2k_base_path, 'DIV2K_train_LR_bicubic_sub/x4')
test_hr_path = os.path.join(div2k_base_path, 'testset/HR')
test_lr_x2_path = os.path.join(div2k_base_path, 'testset/LR/x2')
test_lr_x4_path = os.path.join(div2k_base_path, 'testset/LR/x4')

# Clear existing images
print("Clearing existing images...")
for path in [train_hr_path, train_lr_x2_path, train_lr_x3_path, train_lr_x4_path, test_hr_path, test_lr_x2_path, test_lr_x4_path]:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

# Ensure images are square by padding
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im

def downsample_image(image, scales, save_paths):
    for scale, save_path in zip(scales, save_paths):
        scaled_image = image.resize((image.width // scale, image.height // scale), Image.BICUBIC)
        scaled_image.save(save_path)

def process_image(image_path, hr_save_path, lr_save_paths, scales):
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)  # Handle orientation issues
    image = image.convert('RGB')  # Ensure no incorrect sRGB profile
    image = make_square(image)  # Ensure the image is square
    image.save(hr_save_path, "PNG")

    downsample_image(image, scales, lr_save_paths)

# Process train images
print("Processing train images...")
train_images = [img for img in os.listdir(train_extract_path) if img.endswith(('.jpg', '.png'))]
for img in tqdm(train_images, desc="Train Images"):
    img_path = os.path.join(train_extract_path, img)
    base_name = os.path.splitext(img)[0]
    hr_save_path = os.path.join(train_hr_path, f'{base_name}.png')
    
    lr_save_paths = [
        os.path.join(train_lr_x2_path, f'{base_name}.png'),
        os.path.join(train_lr_x3_path, f'{base_name}.png'),
        os.path.join(train_lr_x4_path, f'{base_name}.png')
    ]
    process_image(img_path, hr_save_path, lr_save_paths, [2, 3, 4])

# Process test images
print("Processing test images...")
test_images = [img for img in os.listdir(test_extract_path) if img.endswith(('.jpg', '.png'))]
for img in tqdm(test_images, desc="Test Images"):
    img_path = os.path.join(test_extract_path, img)
    base_name = os.path.splitext(img)[0]
    hr_save_path = os.path.join(test_hr_path, f'{base_name}.png')
    
    lr_save_paths = [
        os.path.join(test_lr_x2_path, f'{base_name}.png'),
        os.path.join(test_lr_x4_path, f'{base_name}.png')
    ]
    process_image(img_path, hr_save_path, lr_save_paths, [2, 4])

# Clean up the extracted files
print("Cleaning up extracted files...")
shutil.rmtree(train_extract_path)
shutil.rmtree(test_extract_path)

print("Done!")
