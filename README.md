# FTP to HTTP POST File Transfer

This project provides an automated solution for monitoring an FTP server, retrieving files, and uploading them to an HTTP endpoint (specifically designed for Paperless-ngx API). It's particularly useful for scenarios where you need to automatically process and archive documents.

I made this because I had issues with my Brother scanner's SMTP connection, which failed to deliver mails all the time. Scanning to an FTP server and using this image fixed the reliability of document delivery to Paperless greatly.

## Features

- Periodic Monitoring of an FTP server
- File retrieval from FTP
- Automatic file upload to an HTTP endpoint (Designed for Paperless-ngx)
- Support for adding tags to uploaded documents
- Configurable sleep duration between checks

## Prerequisites

- Python

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/basvanrooten/ftp-to-http-post.git
   cd ftp-to-http-post
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with the following content, or use environment variables
   ```
   FTP_HOST=your_ftp_host
   FTP_USER=your_ftp_username
   FTP_PASS=your_ftp_password
   FTP_DIR=/path/to/monitor
   HTTP_ENDPOINT=https://your-paperless-ngx-instance.com/api/documents/post_document/
   HTTP_AUTH_TOKEN=your_paperless_ngx_auth_token
   SLEEP_DURATION=60
   TAGS=1,2
   ```
   > Note that the TAGS need to be the ID of the tags you want to add, not the name.

   Adjust the values according to your setup.

## Usage

Run the script with:

```
python ftp_monitor.py
```

The script will start monitoring the specified FTP directory, process any files it finds, upload them to the specified HTTP endpoint, and then delete them from the FTP server.

## Configuration

All configuration is done through environment variables.

- `FTP_HOST`: The hostname or IP address of your FTP server
- `FTP_USER`: The username for FTP authentication
- `FTP_PASS`: The password for FTP authentication
- `FTP_DIR`: The directory on the FTP server to monitor (default is '/')
- `HTTP_ENDPOINT`: The full URL of the Paperless-ngx API endpoint
- `HTTP_AUTH_TOKEN`: The authentication token for the Paperless-ngx API
- `SLEEP_DURATION`: The number of seconds to wait between checks (default is 60)
- `TAGS`: A comma-separated list of tags to add to each uploaded document

## Disclaimer

This script is provided as-is, without any warranties. Always ensure you have backups and test thoroughly before using in a production environment.