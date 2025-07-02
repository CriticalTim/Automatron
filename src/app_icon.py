"""
Simple icon generator for the application
Creates a basic icon using PIL/Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple application icon"""
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (45, 55, 72, 255))  # Dark blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a circle for the main icon
    circle_margin = 20
    circle_coords = [circle_margin, circle_margin, size - circle_margin, size - circle_margin]
    draw.ellipse(circle_coords, fill=(59, 130, 246, 255))  # Blue circle
    
    # Draw inner circle
    inner_margin = 40
    inner_coords = [inner_margin, inner_margin, size - inner_margin, size - inner_margin]
    draw.ellipse(inner_coords, fill=(147, 197, 253, 255))  # Light blue
    
    # Draw center circle
    center_margin = 80
    center_coords = [center_margin, center_margin, size - center_margin, size - center_margin]
    draw.ellipse(center_coords, fill=(255, 255, 255, 255))  # White center
    
    # Try to add text
    try:
        # Try to use a system font
        font_size = 60
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
                
        # Add "A" for Automatron
        text = "A"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 10
        
        draw.text((x, y), text, fill=(45, 55, 72, 255), font=font)
        
    except Exception as e:
        print(f"Could not add text to icon: {e}")
    
    return img

def save_icon():
    """Save the icon in multiple formats"""
    try:
        icon = create_app_icon()
        
        # Save as ICO (Windows)
        icon.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        
        # Save as PNG (cross-platform)
        icon.save('app_icon.png', format='PNG')
        
        print("Icon files created: app_icon.ico, app_icon.png")
        return True
        
    except Exception as e:
        print(f"Failed to create icon: {e}")
        return False

if __name__ == "__main__":
    save_icon()