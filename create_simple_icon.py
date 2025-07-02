"""
Simple icon creation script that doesn't require PIL
Creates a basic ICO file manually
"""

def create_basic_ico():
    """Create a very basic ICO file manually"""
    # This is a minimal 16x16 pixel ICO file with a simple pattern
    # ICO format is complex, but this creates a basic working icon
    
    ico_data = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x18\x00\x68\x05\x00\x00\x16\x00\x00\x00'
    
    # Add bitmap data for a simple blue icon
    bitmap_data = b'\x40\x00\x00\x00\x10\x00\x00\x00\x20\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    # Blue pixel data (16x16 pixels, 3 bytes per pixel BGR format)
    blue_pixel = b'\xFF\x7F\x00'  # Orange-ish color
    pixels = blue_pixel * 256  # 16x16 = 256 pixels
    
    # AND mask (transparency mask)
    and_mask = b'\x00' * 32  # 32 bytes for 16x16 1-bit mask
    
    ico_data += bitmap_data + pixels + and_mask
    
    with open('app_icon.ico', 'wb') as f:
        f.write(ico_data)
    
    print("Basic icon created: app_icon.ico")

if __name__ == "__main__":
    create_basic_ico()