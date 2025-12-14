# Web Scrapping Masterclass

## 📌 Project Objective

The objective of this project is to develop a robust and user-friendly web scraping module that enables users to extract clean, structured textual data from any website by simply providing its homepage URL. The module is designed to operate in full compliance with ethical scraping practices and technical safeguards.

### Key Goals

- **Automate discovery and scraping** of all internal pages within the target domain.
- **Parse and clean extracted text** by:
  - Splitting content into individual sentences using standard punctuation.
  - Removing excessive whitespace, hashtags, and embedded URLs.
  - Filtering out short or non-coherent fragments.
  - Ensuring each sentence is written on a new line for clarity and downstream processing.
- **Respect robots.txt directives** and store a copy locally for future reference or dispute resolution.
- **Maintain a `visited_links.xlsx` file** to track all URLs visited during the scraping process, supporting transparency and performance validation.
- **Prevent cross-domain scraping** by restricting the crawler to the original domain only.
- **Allow user-defined output format** (CSV, JSON, or plain text) and filename for saving the cleaned data.

---

### Intended Use

This module is intended for **educational and instructional use**, demonstrating scalable scraping workflows with a hands-on approach.
