import argparse
from pytube import YouTube
from pydub import AudioSegment
import os

# Function to extract audio from a video link and save as MP3
def extract_audio_from_video(video_link, output_dir):
    # Download the video
    yt = YouTube(video_link)

    # Get the video title and clean it for file name
    video_title = yt.title
    video_title = video_title.replace(" ", "_").replace("/", "-").replace(":", "-")

    # Generate the output file name
    output_file_name = os.path.join(output_dir, f"{video_title}.mp3")

    video_stream = yt.streams.filter(only_audio=True).first()
    video_stream.download(output_path=output_dir)

    # Convert video to MP3 using pydub
    video_path = os.path.join(output_dir, video_stream.default_filename)
    audio = AudioSegment.from_file(video_path)
    audio.export(output_file_name, format='mp3')

    # Clean up temporary files
    os.remove(video_path)

    return video_title

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract audio from a YouTube video and save it as MP3.')
    parser.add_argument('video_link', help='YouTube video link')
    parser.add_argument('--output-dir', default='.', help='Directory to save the MP3 file (default is the current directory)')
    args = parser.parse_args()

    # Call the function with command-line arguments
    title = extract_audio_from_video(args.video_link, args.output_dir)
    print(f"Audio extracted and saved as {args.output_dir}/{title}.mp3")
