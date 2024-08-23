# All Scan UI 🔍

## Overview
**All Scan UI** is a comprehensive vulnerability detection tool designed to identify and report various web application security vulnerabilities, including SSRF, CSRF, XXE, SQL Injection, and XSS. This tool is built with an intuitive user interface to simplify the scanning process for security professionals and developers.

## Features
- **SSRF (Server-Side Request Forgery) Detection**: Identify vulnerabilities that allow attackers to send crafted requests from the server.
- **CSRF (Cross-Site Request Forgery) Detection**: Detect weaknesses that can enable unauthorized actions on behalf of authenticated users.
- **XXE (XML External Entity) Detection**: Scan for vulnerabilities that exploit XML parsers and expose sensitive data or allow remote code execution.
- **SQL Injection Detection**: Identify SQL Injection points that could allow attackers to interfere with the application's database.
- **XSS (Cross-Site Scripting) Detection**: Detect potential XSS vulnerabilities that could allow attackers to inject malicious scripts into web pages.

 **Install Dependencies**:
    - Ensure you have Python installed. Install required Python packages using:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Start the Application**:
    ```bash
    python app.py
    ```
2. **Access the UI**:
    - Open your browser and go to `http://localhost:5000`.
3. **Run Scans**:
    - Choose the vulnerability type (SSRF, CSRF, XXE, SQL Injection, XSS) you want to scan for.
    - Input the target URL and initiate the scan.
    - View detailed results and reports in the UI.
  
## Contact
- **GitHub**: [Kkarrnn](https://github.com/Kkarrnn)
