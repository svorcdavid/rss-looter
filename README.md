# RSS Looter — RSS Feed Maker

Simple script to generate RSS feeds from HTML pages by using CSS selectors.

**What it does**
- **Purpose**: Parses web pages with BeautifulSoup and produces RSS XML files using `feedgen`.
- **Input**: A `config.json` file that lists sources with CSS selectors, base URL, and output path.
- **Output**: RSS files (example: `feeds/something.xml`).

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
- `selectors.title`, `selectors.link`, `selectors.summary`, `selectors.date`, `selectors.image`
- `base_url`: used to resolve relative links/images
- `rss_output`: path to save the generated RSS file
- `limit`: maximum number of items to include
- `date_formats`: list of `datetime.strptime` formats to try

**Usage**
Run the script:

```powershell
python main.py
```

The script will read `config.json`, generate RSS files and save them to the paths specified by `rss_output`.

**Security & privacy**
- Do not commit secrets or credentials into `config.json`. If a site requires authentication, keep credentials out of the repo (use environment variables or a private config).

**License**
This project is licensed under the MIT License — see `LICENSE`.

**Notes & Suggestions**
- Add `config.json` to `.gitignore` to avoid leaking site-specific or private settings.
- Output directories (e.g., `feeds/`) are saved; consider ignoring them in git if you don't want generated files in the repo.

Enjoy — feel free to open issues or PRs!
