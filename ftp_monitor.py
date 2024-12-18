import os
import time
import logging
from ftplib import FTP
import requests
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# FTP settings
FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
FTP_DIR = os.getenv('FTP_DIR', '/')

# HTTP endpoint and authorization
HTTP_ENDPOINT = os.getenv('HTTP_ENDPOINT')
HTTP_AUTH_TOKEN = os.getenv('HTTP_AUTH_TOKEN')

# Sleep duration between checks (in seconds)
SLEEP_DURATION = int(os.getenv('SLEEP_DURATION', 60))

# Tags that get added to the uploaded documents
TAGS = os.getenv('TAGS', '').split(',')

def process_file(ftp, filename):
    logging.info(f"Processing file: {filename}")
    
    # Download the file content
    content = []
    ftp.retrbinary(f"RETR {filename}", content.append)
    file_content = b''.join(content)
    
    # Prepare headers with Authorization token
    headers = {
        'Authorization': f'Token {HTTP_AUTH_TOKEN}'
    } if HTTP_AUTH_TOKEN else {}
    
    # Prepare multipart form data
    fields = {'document': (filename, file_content, 'application/octet-stream')}
    
    # Add tags to the fields, with multiple 'tags' entries for multiple tags
    for tag in TAGS:
        if tag.strip():  # Only add non-empty tags
            fields[f'tags'] = (None, tag.strip())
    
    multipart_data = MultipartEncoder(fields=fields)
    
    # Update headers with content type
    headers['Content-Type'] = multipart_data.content_type
    
    # Send HTTP POST request
    try:
        response = requests.post(HTTP_ENDPOINT, data=multipart_data, headers=headers)
        response.raise_for_status()
        
        # Log the UUID from the response
        response_text = response.text
        logging.info(f"Response: {response_text}")
        if response_text:
            logging.info(f"Successfully uploaded file {filename}. Document UUID: {response_text}")
        else:
            logging.info(f"Successfully uploaded file {filename}, but no UUID was returned in the response.")
        
        # Delete the file after successful HTTP POST
        ftp.delete(filename)
        logging.info(f"Deleted file {filename} from FTP server")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send file {filename} to HTTP endpoint: {str(e)}")

def monitor_ftp():
    while True:
        try:
            with FTP(FTP_HOST) as ftp:
                ftp.login(user=FTP_USER, passwd=FTP_PASS)
                ftp.cwd(FTP_DIR)
                
                logging.info("Connected to FTP server")
                
                # Get list of files
                files = ftp.nlst()
                
                for file in files:
                    process_file(ftp, file)
                
        except Exception as e:
            logging.error(f"Error connecting to FTP server: {str(e)}")
        
        # Wait before next check
        logging.info(f"Sleeping for {SLEEP_DURATION} seconds before next check")
        time.sleep(SLEEP_DURATION)

if __name__ == "__main__":
    logging.info(f"Starting FTP monitor. Sleep duration between checks: {SLEEP_DURATION} seconds")
    logging.info(f"Tags to be added to documents: {TAGS}")
    monitor_ftp()