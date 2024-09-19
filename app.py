import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64
import re
import time
import json

# Set SEO data: title and description
st.set_page_config(page_title="Instagram Data Scraper & Extractor", page_icon="🔍", layout="wide")

# Add meta tags for SEO (using HTML and markdown)
st.markdown(
    """
    <meta name="description" content="Instagram Hashtag Scraper: Extract Instagram data by hashtag with profile pictures, likes, and posts. Export the data in CSV format.">
    """, 
    unsafe_allow_html=True
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Dark background for the app */
    .stApp {
        background-color: #1c1c1c;
        color: #f0f0f0;
    }

    /* Main title styling */
    h1 {
        color: #ff6347;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
    }

    /* Text input styling */
    input {
        background-color: #333;
        color: #f0f0f0;
        border: 2px solid #ff6347;
        padding: 10px;
        border-radius: 8px;
        width: 100%;
        font-size: 1.1rem;
    }

    /* Button styling */
    .stButton button {
        background-color: #ff6347;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1.1rem;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .stButton button:hover {
        background-color: #ff4500;
        transform: translateY(-2px);
    }

    /* Table styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        padding: 14px;
        text-align: left;
        border-bottom: 1px solid #555;
    }

    th {
        background-color: #ff6347;
        color: white;
        font-size: 1.1rem;
    }

    td {
        background-color: #2c2c2c;
        color: #f0f0f0;
    }

    /* Image resizing */
    img {
        max-height: 80px;
        border-radius: 50%;
        border: 2px solid #ff6347;
    }

    /* Scrollable content for the table */
    .stDataFrame {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #444;
        background-color: #1c1c1c;
    }

    /* Placeholder text styling */
    ::placeholder {
        color: #bbb;
        opacity: 0.8;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Streamlit app title
st.title("Instagram Data Scraper & Extractor")

# Input for search keyword
input_keyword = st.text_input("Enter Instagram Hashtag (without #)", "angelone")

# Run button
run_button = st.button("Run Scraper")

# Headers for scraping requests
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8,ta;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'datr=FFT_ZI12g2KH5isaLvprsdij; ig_did=522B81A8-1728-4C51-AC88-6F4DA81E89F3; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; mid=Za52NgALAAHMFyBddpxZaR-9gR33; ps_n=1; ps_l=1; csrftoken=X4XkPapy87MnhhcIYZFmHW7Nwt5hduQX; ds_user_id=41090787118; wd=1920x911; shbid="9828\\05441090787118\\0541757484026:01f750a01ef110ca80ca1d722c5870c4fda170931d4f5816f14a5a0bc2c4cc1c1a2b48f9"; shbts="1725948026\\05441090787118\\0541757484026:01f756770c88b0f94cc70998aa2784dbc88165b3b285453d2f95cd65ff6b4f24c87af358"; sessionid=41090787118%3ASNinb86ADemqLg%3A27%3AAYeidBvuA2UcAy1h-6wMZDn1bQBB8Sk4OBGuB7tURA; fbsr_124024574287414=z0SOtqPlPtBdAq5DyYejXC80Gp2f0AsBSO-wDAR-Clk.eyJ1c2VyX2lkIjoiMTAwMDE0ODc5NjQyOTUwIiwiY29kZSI6IkFRQjNFUnJua2pTdFNOTFpweEJuVDRUR1NaZnRqamJQX080WUNja19JY0ZzcjdrbXJyOUR2ZU5tZ1M2QjkzTk5ESzE2cmtGUUpHTWdNbnRwajg0ZGpYSDZ3VHBnZmpiQXVsWDBIamJtcTRIUm05S04tUXVySzdGc19TUTNvZnhWNk9IdmMtRVZCalVKbWs2eHk0cFpITE1NT2liemdjRzY2NGdkMVByb2RZMmI5MmNxTVFzTGk3cU42UWtfSUNtSVdkczNuYUVWcEZNbU41aU85dnFTVTQ0dXhUMlFaMFNIQnJpZXhWTVhCMlBLTERtZk5WUXJoUllnaGJJNEFZek9oTHYtUDB1NXJYYkJvUVlMMFcyVFFRajVQdFUxTU1NVXVVUjdKMllQYVVwVGcyYUJ2cUVnSWhpQnl3UVdLeXR6MDBlVy1zQmZIQnZ3eWUwbXg2XzhnUElMQTFjTVFsMC1aRmRLV1RQdmplcGhZZyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQk8xblM1RTdWWWN1VTljNEhaQ00ycHp4bnM4SHNtVVRibndlVXhaQ3FySHFUM1ZSQW9SUGZyUFl3WkNHV0xERkZRRGN0VmkyNjdLT2VaQ3kyRG03NDlSdzFROFBsUFRlRlFFR3dDMHVBcUlpZ2gzZjZFWkNoRHBPaWlJRjgxS0hJY0RTUUUzOWM5TTA0a3FZTHdsMzJiN3ZFQW9CQVNTbG1TbEM5NjVYYVF4aHpGZ05tTXRjVTlUOFpBWkFQM1pDM3VRWkRaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzI1OTQ4NDUxfQ; rur="EAG\\05441090787118\\0541757484598:01f748c52fe26563dff3ec6f0d9860173071d4c70eb234c6f371f7ce2dddf724c45e73e0"; csrftoken=PFvNnpEptUZYJIrsI7BIox83B6xozkcJ; ds_user_id=41090787118; rur="EAG\\05441090787118\\0541757486201:01f7f9e14ca8c6c275d123d8374bb7b169fdc5ca690c5b395ccf84d394c9b13ec4a03554"',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.instagram.com/explore/search/keyword/?q=%23angelone',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.120", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-asbd-id': '129477',
    'x-csrftoken': 'X4XkPapy87MnhhcIYZFmHW7Nwt5hduQX',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR1aSIzQ6bGIL7SwywrOszXyZz1m4YDCfnDDHLHmUrlr7dXl',
    'x-requested-with': 'XMLHttpRequest'
}

# Function to make request and get data
def scrape_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None
        
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("Failed to parse JSON from the response.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error during request: {e}")
        return None

# Function to extract rank_token and next_max_id
def extract_values(response_text):
    try:
        rank_token = re.search(r'"rank_token":\s?"([a-z0-9\-]+)"', response_text).group(1)
        next_max_id = re.search(r'"next_max_id":\s?"([a-z0-9]+)"', response_text).group(1)
        return rank_token, next_max_id
    except AttributeError:
        return None, None

# Function to extract relevant data from the scraped JSON
def extract_data_from_json(json_data):
    extracted_data = []
    
    def process_json_part(data):
        if isinstance(data, dict):
            if "media" in data:
                media = data["media"]
                user = media.get("user", {})
                profile_pic_url = user.get("hd_profile_pic_url_info", {}).get("url", "N/A")
                like_count = media.get("like_count", "N/A")
                created_at = convert_utc_to_date(media.get("taken_at"))
                post_url = f"https://www.instagram.com/p/{media.get('code', 'N/A')}/"

                extracted_data.append({
                    "username": user.get("username", "N/A"),
                    "full_name": user.get("full_name", "N/A"),
                    "profile_pic_url": profile_pic_url,
                    "like_count": like_count,
                    "created_at": created_at,
                    "post_url": post_url
                })

            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    process_json_part(value)

        elif isinstance(data, list):
            for item in data:
                process_json_part(item)

    process_json_part(json_data)
    return extracted_data

# Function to convert UTC timestamp to human-readable date
def convert_utc_to_date(utc_timestamp):
    try:
        return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (TypeError, ValueError):
        return "N/A"

# Function to display data in a table with circular profile images
def display_data_in_table(extracted_data):
    df = pd.DataFrame(extracted_data)

    if not df.empty:
        # Resize profile pictures to a max height
        df['profile_pic_url'] = df['profile_pic_url'].apply(lambda url: f'<img src="{url}" style="max-height:100px;" />')

        # Display as HTML table with images
        st.write(df.to_html(escape=False), unsafe_allow_html=True)

        # Export to CSV
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="instagram_data.csv">Download CSV file</a>'
        st.markdown(href, unsafe_allow_html=True)

# Main functionality based on input
if run_button and input_keyword:
    base_url = f"https://www.instagram.com/api/v1/fbsearch/web/top_serp/?query=%23{input_keyword}"
    all_extracted_data = []
    next_max_id = None
    rank_token = None
    max_requests = 10  # Limit to max 10 requests
    
    # Keep making requests and paginating until no more data or max_requests is reached
    for i in range(max_requests):
        if next_max_id and rank_token:
            url = f"{base_url}&next_max_id={next_max_id}&rank_token={rank_token}"
        else:
            url = base_url
        
        scraped_data = scrape_data(url, headers)
        
        if not scraped_data:
            break
        
        extracted_data = extract_data_from_json(scraped_data)
        if extracted_data:
            all_extracted_data.extend(extracted_data)
        else:
            st.warning("No relevant data extracted.")
            break
        
        # Get the response text and extract rank_token and next_max_id
        response_text = json.dumps(scraped_data)
        rank_token, next_max_id = extract_values(response_text)
        
        if not next_max_id:
            break
    
    # Display all extracted data in the table
    if all_extracted_data:
        display_data_in_table(all_extracted_data)
    else:
        st.warning("No data was fetched.")
