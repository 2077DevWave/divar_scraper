import Upload

if __name__ == "__main__":
    video_path = "video.mp4"
    title = "My Awesome Video"
    description = "This is a description of my video."
    tags = ["tag1", "tag2", "tag3"]
    Upload.upload_video(video_path, title, description, tags)
