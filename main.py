#
# RSS Looter — RSS Feed Maker
# Copyright (c) 2025 Svorc David
# Licensed under the MIT License.
#

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
import os
import pytz
from datetime import datetime
import json
import sys

# --- Load config ---
CONFIG_FILE = "config.json"

def load_config(file_path):
	"""Load config from file."""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			return json.load(f)
	except FileNotFoundError:
		print(f"❌ ERR: Config file '{file_path}' not found.")
		sys.exit(1)
	except json.JSONDecodeError as e:
		print(f"ERR: bad JSON format '{file_path}'. Detail: {e}")
		sys.exit(1)

# --- Helpers ---

def extract_text(soup_element):
	return soup_element.get_text(strip=True) if soup_element else ""

def extract_attr(soup_element, attr):
	return soup_element[attr] if soup_element and soup_element.has_attr(attr) else ""

def parse_date(date_text, date_formats):
	"""Try to parse ISO"""
	if not date_text:
		return None
	
	# 1. ISO format (<time datetime="2023-12-24T08:00:00+01:00">)
	try:
		pub_date = datetime.fromisoformat(date_text)
		if pub_date.tzinfo is None:
			# UTC if not present any
			return pub_date.replace(tzinfo=pytz.UTC)
		return pub_date
	except ValueError:
		pass # Try more

	# 2. Try formats from config
	for fmt in date_formats:
		try:
			pub_date = datetime.strptime(date_text, fmt)
			# UTC if not present any, for consistency
			return pub_date.replace(tzinfo=pytz.UTC)
		except ValueError:
			continue
	
	print(f"⚠️ WAR: Date '{date_text}' can't be parsed using any known format.")
	return None

# --- Main ---

def generate_rss(source):
	print(f"\n--- 🚀 Generating RSS for: {source['name']} ({source['url']}) ---")
	
	try:
		response = requests.get(source["url"], timeout=15)
		response.raise_for_status() # Vyhodí chybu pro 4xx/5xx stav
	except requests.exceptions.RequestException as e:
		print(f"❌ ERR: downloading {source['url']}: {e}")
		return

	soup = BeautifulSoup(response.content, "html.parser")

	fg = FeedGenerator()
	fg.title(source["name"])
	fg.link(href=source["url"])
	fg.description(f"RSS feed generated for {source['name']} | Source: {source['url']}")
	# Standard timezone for feed (like UTC)
	fg.pubDate(datetime.now(pytz.UTC)) 

	items = soup.select(source["selectors"]["item"])[:source.get("limit", 10)]
	
	if not items:
		print(f"⚠️ WAR: No items found using selectors: '{source['selectors']['item']}'")

	date_formats = source.get("date_formats", ["%d.%m.%Y"]) # Default formats

	for item in items:
		fe = fg.add_entry()
		
		# Get elements
		selectors = source["selectors"]
		title_el = item.select_one(selectors.get("title", ""))
		link_el = item.select_one(selectors.get("link", ""))
		summary_el = item.select_one(selectors.get("summary", ""))
		date_el = item.select_one(selectors.get("date", ""))
		image_el = item.select_one(selectors.get("image", ""))

		# Process data
		title = extract_text(title_el) or "no title"
		# Handle link extraction based on config
		if source.get("link_from_item", False):
			link = urljoin(source["base_url"], item.get("href", "#") or "#")
		else:
			link_el = item.select_one(selectors.get("link", ""))
			link = urljoin(source["base_url"], extract_attr(link_el, "href") or "#")

		summary_text = extract_text(summary_el) or "no summary available"
		
		# Parse data
		date_text = extract_attr(date_el, "datetime") or extract_text(date_el)
		pub_date = parse_date(date_text, date_formats)
		
		# Process images
		raw_image_url = extract_attr(image_el, "src") or extract_attr(image_el, "data-src") 
		image_url = raw_image_url if raw_image_url and raw_image_url.startswith("http") else urljoin(source["base_url"], raw_image_url or "")

		# Set RSS item
		fe.title(title)
		fe.link(href=link)
		fe.description(summary_text)
		fe.guid(link, permalink=True) # Use link as GUID
		
		if pub_date:
			fe.pubDate(pub_date)
		
		if image_url:
			# MIME type - should be correct, if known, can be added to config
			fe.enclosure(image_url, None, "image/jpeg") 

	# Save RSS to file
	rss_output_path = source["rss_output"]
	os.makedirs(os.path.dirname(rss_output_path), exist_ok=True)
	fg.rss_file(rss_output_path, pretty=True) # Add pretty formatting
	print(f"✅ RSS feed saved to: {rss_output_path}")


if __name__ == "__main__":
	# Load config from external file
	feed_sources = load_config(CONFIG_FILE)
	
	# Run for every item
	for src in feed_sources:
		generate_rss(src)