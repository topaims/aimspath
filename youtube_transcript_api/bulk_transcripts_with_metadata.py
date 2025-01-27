
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

# YouTube API Key (replace with your actual API key)
API_KEY = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_video_metadata(video_id):
    """Fetch metadata (title, channel name, publish date) for a YouTube video."""
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    if response['items']:
        snippet = response['items'][0]['snippet']
        return {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'published_at': snippet['publishedAt']
        }
    return {}

def download_transcripts_and_metadata(video_ids, output_folder="transcripts"):
    """Download transcripts and metadata for multiple YouTube videos."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video_id in video_ids:
        try:
            # Fetch transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Fetch metadata
            metadata = fetch_video_metadata(video_id)
            metadata['transcript'] = transcript

            # Save as JSON
            with open(f"{output_folder}/{video_id}.json", "w") as f:
                json.dump(metadata, f, indent=4)
            print(f"Saved: {output_folder}/{video_id}.json")
        except Exception as e:
            print(f"Error fetching data for {video_id}: {e}")

def create_csv(video_ids, output_folder="transcripts", csv_filename="AimsPath-MyCollection.csv"):
    """Create a CSV file indexing all video details."""
    import csv
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write headers
        writer.writerow(['Video ID', 'Title', 'SubTitle', 'Creator Channel Name', 'Date', 'URL', 'JSON File Name'])

        for video_id in video_ids:
            try:
                # Fetch metadata
                metadata = fetch_video_metadata(video_id)

                # Write to CSV
                writer.writerow([
                    video_id,
                    metadata.get('title', 'N/A'),
                    '',  # SubTitle can be added manually later
                    metadata.get('channel', 'N/A'),
                    metadata.get('published_at', 'N/A'),
                    f"https://www.youtube.com/watch?v={video_id}",
                    f"{output_folder}/{video_id}.json"
                ])
            except Exception as e:
                print(f"Error writing data for {video_id}: {e}")

if __name__ == "__main__":
    # Example video IDs (replace with your actual list of IDs)
    video_ids = ['XVY4rgZrdVs']
    download_transcripts_and_metadata(video_ids)
    create_csv(video_ids)
