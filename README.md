# Selamat - Automated Vulnerability Scanner

## Overview

**Selamat** is a tool designed to help penetration testers detect vulnerabilities without causing harm. It automates the vulnerability scanning process and ensures no harmful payloads are used.

### Features

1. **Wayback URL Crawling**
   - Gathers URLs and pages from the **Wayback Machine**.
   - **Advantages**:
     - Bypasses Web Firewalls.
     - Avoids generating heavy traffic.

2. **SQL Injection Detection with Minimal Payload**
   - Uses a single apostrophe (`'`) to detect vulnerabilities.
   - **No harmful payloads** are used.

3. **Cross-Site Scripting (XSS) Detection**
   - Identifies XSS by checking for reflected user input using the word **"RENGOKU"**.

---

### Pros
- **Hard to detect by firewalls**
- **Safe to use**: No harmful payloads are involved.

### Cons
- **Not suitable for beginners**: Basic knowledge of web vulnerabilities is needed.
- **Requires manual verification** after detection.

