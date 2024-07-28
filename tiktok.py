import subprocess
import sys

# Function to install missing packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ['requests', 'wget', 'tqdm', 'colorama', 'pyfiglet']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install_package(package)

# Import the required packages after installation
import requests
import wget
import os
import re
import time
from tqdm import tqdm
from urllib.parse import quote
from colorama import Fore, Style, init
import pyfiglet
import random
import shutil

# Initialize colorama
init(autoreset=True)

# List of figlet fonts to choose from
figlet_fonts = ['slant', '3-d', '5lineoblique', 'alligator', 'banner', 'basic', 'block', 'bubble']

def print_with_color(text, color=Fore.WHITE):
    print(color + text)

def generate_banner():
    banner_font = random.choice(figlet_fonts)
    description_font = random.choice(figlet_fonts)
    
    banner_text = pyfiglet.figlet_format("Z0-F4C3R", font=banner_font)
    description_text = pyfiglet.figlet_format("Zora is a beginner programmer", font=description_font)
    
    return banner_text, description_text

def print_lolcat(text):
    process = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.stdin.write(text.encode('utf-8'))
    process.stdin.close()
    output = process.stdout.read()
    process.stdout.close()
    print(output.decode('utf-8'))

def center_text(text):
    term_width, _ = shutil.get_terminal_size()
    centered_lines = [line.center(term_width) for line in text.split('\n')]
    return '\n'.join(centered_lines)

def download_tiktok_video(apikey, tiktok_url):
    encoded_url = quote(tiktok_url, safe='')
    url = f"https://api.lolhuman.xyz/api/tiktok?apikey={apikey}&url={encoded_url}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 200:
            result = data['result']
            video_url = result['link']
            video_title = result.get('title', '')
            video_duration = result.get('duration', 'Unknown')
            author_name = result['author']['nickname']
            play_count = result['statistic']['play_count']
            like_count = result['statistic']['like_count']
            share_count = result['statistic']['share_count']
            comment_count = result['statistic']['comment_count']
            upload_date = result.get('create_time', 'Unknown')
            
            # Determine filename
            if video_title:
                valid_filename = re.sub(r'[\\/*?:"<>|]', '', video_title.split('#')[0].strip())
            else:
                hashtags = result.get('hashtags', [])
                if hashtags:
                    valid_filename = hashtags[0]
                else:
                    valid_filename = f"tiktok_video_{int(time.time())}"
            
            # Create directory if not exists
            output_dir = 'result/TikTok'
            os.makedirs(output_dir, exist_ok=True)
            
            # Download video
            video_filename = f"{output_dir}/{valid_filename}.mp4"
            print_with_color(f"Downloading video: {video_title}", Fore.GREEN)
            
            # Add download animation
            for _ in tqdm(range(100), desc="Downloading"):
                time.sleep(0.01)
            
            wget.download(video_url, video_filename)
            print_with_color("\nDownload complete!", Fore.GREEN)
            
            # Get video size
            video_size = os.path.getsize(video_filename)
            
            # Print video details
            print_with_color(f"\nVideo Details:", Fore.CYAN)
            print_with_color(f"Path: {video_filename}", Fore.YELLOW)
            print_with_color(f"Title: {video_title}", Fore.YELLOW)
            print_with_color(f"Size: {video_size / (1024 * 1024):.2f} MB", Fore.YELLOW)
            print_with_color(f"Duration: {video_duration} seconds", Fore.YELLOW)
            print_with_color(f"Upload Date: {upload_date}", Fore.YELLOW)
            print_with_color(f"Author: {author_name}", Fore.YELLOW)
            print_with_color(f"Views: {play_count}", Fore.YELLOW)
            print_with_color(f"Likes: {like_count}", Fore.YELLOW)
            print_with_color(f"Shares: {share_count}", Fore.YELLOW)
            print_with_color(f"Comments: {comment_count}", Fore.YELLOW)
        else:
            print_with_color(f"Error: {data['message']}", Fore.RED)
    except requests.exceptions.RequestException as e:
        print_with_color(f"Request error: {e}", Fore.RED)
    except requests.exceptions.HTTPError as e:
        print_with_color(f"HTTP error: {e}", Fore.RED)
    except Exception as e:
        print_with_color(f"An error occurred: {e}", Fore.RED)

def main():
    apikey = 'YOUR_APIKEY_HERE'
    while True:
        banner_text, description_text = generate_banner()
        full_text = banner_text + '\n' + description_text
        centered_text = center_text(full_text)
        print_lolcat(centered_text)
        
        tiktok_url = input("Masukkan URL TikTok: ").strip()
        if not tiktok_url:
            print_with_color("URL TikTok tidak boleh kosong.", Fore.RED)
            continue
        
        download_tiktok_video(apikey, tiktok_url)

if __name__ == "__main__":
    main()
