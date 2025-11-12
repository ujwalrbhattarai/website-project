# 📸 How to Add Teacher/Instructor Photos

This guide explains how to add instructor photos to make your courses more attractive and personal.

## 🎯 Quick Steps

### Method 1: Add Instructor Photos (Recommended)

1. **Prepare Your Photos**
   - Use clear, professional photos of instructors
   - Recommended size: 500x500 pixels (square)
   - Supported formats: JPG, PNG
   - File size: Keep under 1MB for fast loading

2. **Save Photos**
   - Place instructor photos in: `static/images/instructors/`
   - Naming convention: `instructor_[id].jpg` or `instructor_[name].jpg`
   - Example: `instructor_1.jpg`, `instructor_ramesh.jpg`

3. **Default Photo**
   - Add a default photo named `default.jpg` in the same folder
   - This will be used if a specific instructor photo is not found

### Method 2: Use Online Images (Easiest)

The system automatically generates avatar images based on instructor names if no photo is found. It uses:
- `https://ui-avatars.com/api/` service
- Automatically creates initials-based avatars
- No manual work needed!

## 📁 Folder Structure

```
project/
└── static/
    └── images/
        └── instructors/
            ├── default.jpg          # Default instructor photo
            ├── instructor_1.jpg     # Dr. Ramesh Kumar
            ├── instructor_2.jpg     # Prof. Sita Sharma
            └── [more photos...]
```

## 🖼️ How the System Works

1. **System checks** for instructor photo at: `static/images/instructors/default.jpg`
2. **If not found**, it uses the fallback: Avatar with instructor initials
3. **Avatar is generated** automatically with your brand colors

## 💡 Tips for Attractive Photos

### Professional Photos
- Use good lighting
- Plain or subtle background
- Instructor should be smiling and approachable
- Dress professionally
- Face should be clearly visible

### Photo Editing
- Crop to square format (1:1 ratio)
- Adjust brightness/contrast if needed
- Keep file size optimized (compress if needed)

### Tools to Edit Photos
- **Online**: Canva, Photopea, Remove.bg (for background removal)
- **Desktop**: GIMP (free), Photoshop
- **Mobile**: Snapseed, Adobe Lightroom Mobile

## 🎨 Adding Instructor Info to Database

To add instructor details with photos, edit the `init_db.py` file:

```python
faculty1 = User(
    username='teacher1',
    email='teacher1@theinnovativegroup.edu.np',
    password=generate_password_hash('teacher123'),
    full_name='Dr. Ramesh Kumar',  # This name appears on courses
    role='faculty'
)
```

Then save photo as: `static/images/instructors/instructor_1.jpg`

## 🌐 Using Web URLs (Alternative)

You can also use direct image URLs:

1. Upload instructor photo to image hosting (Imgur, Cloudinary, etc.)
2. Update the course detail template to use URL instead:

```html
<img src="https://your-image-url.com/photo.jpg" 
     alt="Instructor" 
     class="instructor-img">
```

## 📱 Displaying Demo Videos

Demo videos are already set up! When you create a course:

1. **Get YouTube Video**
   - Find your demo video on YouTube
   - Click "Share" → "Embed"
   - Copy the embed URL: `https://www.youtube.com/embed/VIDEO_ID`

2. **Add to Course**
   - Login as faculty
   - Create new course or edit existing
   - Paste the embed URL in "Demo Video URL" field

3. **Students Can Preview**
   - Non-enrolled students see the demo
   - After enrollment, they access all course videos

## 🎬 Sample Demo Videos Included

The system comes with demo videos for:
- Python Programming
- Flask Web Development
- Data Science
- Digital Marketing

## 🔧 Troubleshooting

### Photo Not Showing?
1. Check file name matches format: `default.jpg`
2. Ensure photo is in correct folder: `static/images/instructors/`
3. Clear browser cache (Ctrl+Shift+R)
4. Check image format (JPG/PNG only)

### Photo Too Large?
- Use online compressor: TinyPNG, Compressor.io
- Or resize using image editor before uploading

### Want Circular Photos?
Photos are automatically made circular by the CSS! Just upload square images.

## ✨ Enhancing Your Institution

### Contact Information
Already updated with:
- Institution Name: **The Innovative Group**
- Phone: **+977-9862134951**
- Located in footer and contact sections

### Social Media
Update social media links in `templates/base.html`:
```html
<a href="YOUR_FACEBOOK_URL" class="text-white me-3">
    <i class="fab fa-facebook fa-2x"></i>
</a>
```

## 🎓 Next Steps

1. ✅ Add instructor photos
2. ✅ Upload demo videos for each course
3. ✅ Update social media links
4. ✅ Test the website with real students
5. ✅ Customize colors and branding
6. 🚀 Launch your educational platform!

---

**Need Help?** Check the main README.md or QUICKSTART.md for more information!
