# RSS Looter — RSS Feed Maker

Simple script to generate RSS feeds from HTML pages by using CSS selectors.

**What it does**
- **Purpose**: Parses web pages with BeautifulSoup and produces RSS XML files using `feedgen`.
- **Input**: A `config.json` file that lists sources with CSS selectors, base URL, and output path.
- **Output**: RSS files (example: `feeds/example.xml`).

**Install**
Install dependencies (use a venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Configuration**
- Copy `config.example.json` to `config.json` and edit the entries for sites you want to scrape.
- `config.json` is read by `main.py` and should contain an array of source objects (see the example file).

Important fields in each source:
- `name`: human-friendly feed name
- `url`: page to download
- `selectors.item`: CSS selector for each article/container
- `selectors.title`, `selectors.summary`, `selectors.date`, `selectors.image`: CSS selectors within each item
- `selectors.link`: CSS selector for the link element (see `link_from_item` below)
- `base_url`: used to resolve relative links/images
- `rss_output`: path to save the generated RSS file
- `limit`: maximum number of items to include (default: 10)
- `date_formats`: list of `datetime.strptime` formats to try (default: `["%d.%m.%Y"]`)
- `link_from_item` (optional): `true` if the item element itself is the link (has `href` attribute); `false` if link is a child selector (default: `false`)

**Link extraction modes**

The script supports two ways to extract article links:

1. **`link_from_item: false`** (default): The item is a container and you provide a selector to find the `<a>` tag inside it.
   ```json
   "selectors": {
     "item": "article.post",
     "link": "header h2 a"
   }
   ```

2. **`link_from_item: true`**: The item element itself is the `<a>` tag with the `href` attribute.
   ```json
   "selectors": {
     "item": "a.main",
     "link": "self"
   }
   ```
   When set to `true`, the script extracts `href` directly from the item element.

**Usage**
Run the script:

```powershell
python main.py
```

The script will read `config.json`, generate RSS files and save them to the paths specified by `rss_output`.

**Security & privacy**
- Do not commit secrets or credentials into `config.json`. Keep credentials (API keys, private URLs..) out of the repo (use environment variables or a private config).

**License**
This project is licensed under the MIT License — see `LICENSE`.

**Notes & Suggestions**
- Add `config.json` to `.gitignore` to avoid leaking site-specific or private settings.
- Output directories (e.g., `feeds/`) are saved; consider ignoring them in git if you don't want generated files in the repo.

Enjoy — feel free to open issues or PRs!
