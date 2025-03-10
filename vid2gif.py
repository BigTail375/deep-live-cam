from moviepy import VideoFileClip

# Load the GIF file
gif_clip = VideoFileClip("target.gif")

# Write the result to an MP4 file
gif_clip.write_videofile("target.mp4", codec="libx264")