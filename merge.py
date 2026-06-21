import urllib.request
import os

PLAYLISTS = [
    {"url": "https://iptv-org.github.io/iptv/countries/tj.m3u", "name": "Tajikistan"},
    {"url": "https://iptv-org.github.io/iptv/countries/ru.m3u", "name": "Russia"},
    {"url": "https://iptv-org.github.io/iptv/countries/uz.m3u", "name": "Uzbekistan"}
]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merged_playlist.m3u")

def download_playlist(url):
    try:
        print(f"Downloading {url}...")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

def merge():
    merged_lines = ["#EXTM3U"]
    
    for pl in PLAYLISTS:
        content = download_playlist(pl["url"])
        if not content:
            continue
        
        lines = content.splitlines()
        channel_count = 0
        
        # We need to parse pairs of #EXTINF and the following URL stream
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF:"):
                # Check if next line is the stream URL
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line and not next_line.startswith("#"):
                        # Add the channel entry
                        merged_lines.append(line)
                        merged_lines.append(next_line)
                        channel_count += 1
                        i += 2
                        continue
            i += 1
            
        print(f"Added {channel_count} channels from {pl['name']}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_lines))
        
    print(f"\nSuccessfully merged! Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge()
