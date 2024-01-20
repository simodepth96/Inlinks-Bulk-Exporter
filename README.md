# Broken Internal Links Exporter

This script filters out HTTP 2xx internal links from a bulk export performed via Screaming Frog following a website crawl.

**How to use?**
1. Screaming Frog > Bulk Exports > Links > All Inlinks
2. Upload an XLSX/CSV file

**Purpose**
Avoid annoying and lengthy data cleaning from large datasets.

**Features**
1. Filters out the rows with valid URLs (HTTP 2xx)
2. Counts how many internal links with adverse status code (Non-HTTP 2xx)
3. Plot a distribution of most common status codes
4. Provide a cleaned table with broken internal links 
