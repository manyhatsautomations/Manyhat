import csv
import html
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse

import requests

OUT_DIR = r"C:\Users\paulr\Desktop\Leads"
ACTIVE_CSV = os.path.join(OUT_DIR, "bc_roofing_active_with_websites.csv")
NO_WEBSITE_CSV = os.path.join(OUT_DIR, "bc_roofing_no_website_opportunities.csv")
AUDIT_CSV = os.path.join(OUT_DIR, "bc_roofing_full_audit.csv")
CITY_AUDIT_CSV = os.path.join(OUT_DIR, "bc_roofing_city_search_audit.csv")

# User-requested cities plus missing nearby/market-adjacent BC cities.
CITIES = [
    "Vancouver", "Burnaby", "Richmond", "Coquitlam", "Surrey", "Abbotsford",
    "Maple Ridge", "Langley", "White Rock", "Chilliwack", "Port Coquitlam",
    "Kelowna", "West Vancouver", "North Vancouver", "Whistler", "Delta",
    # missing Metro Vancouver / Fraser Valley / Sea-to-Sky / Okanagan cities
    "New Westminster", "Port Moody", "Pitt Meadows", "Mission", "Squamish",
    "Pemberton", "Hope", "West Kelowna", "Lake Country", "Vernon", "Penticton",
]

CHECKBOX_COLS = ["Called", "Answered", "Voicemail", "Not interested", "Wants demo"]
BASE = "https://www.yellowpages.ca"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-CA,en;q=0.9",
}

session = requests.Session()
session.headers.update(HEADERS)

phone_re = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})(?!\d)")
roof_re = re.compile(r"roof|roofing|roofer|shingle|torch[- ]?on|waterproof|gutter|siding|exterior|sheet metal|membrane|drainage", re.I)
# Remove non-call targets and obvious unrelated late-page noise.
exclude_name_re = re.compile(
    r"\b(union local|roofing supply|roofing supplies|cedar supply|kitchen cabinets|donut|restaurant|dentist|law office|insurance broker|apartment|real estate|hotel|motel)\b",
    re.I,
)
parked_re = re.compile(
    r"defaultwebpage\.cgi|window\.location\.href=\"/lander\"|checking your browser|domain parked|buy this domain|this domain is for sale|sedo domain parking|not acceptable!|future home of something quite cool",
    re.I,
)
known_city_names = sorted(set(CITIES + [
    "Aldergrove", "Anmore", "Belcarra", "Bowen Island", "Lions Bay", "Tsawwassen", "Ladner", "Cloverdale", "Fleetwood",
    "Fort Langley", "Yarrow", "Agassiz", "Harrison Hot Springs", "Summerland", "Peachland", "Oyama", "Winfield",
]), key=len, reverse=True)


def clean(s):
    if s is None:
        return ""
    return " ".join(html.unescape(re.sub(r"<[^>]*>", " ", str(s))).split())


def normalize_name(name):
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower().replace("&", "and"))


def digits(s):
    return re.sub(r"\D", "", s or "")


def normalize_phone(s):
    nums = re.findall(r"\d", s or "")
    if len(nums) == 11 and nums[0] == "1":
        nums = nums[1:]
    if len(nums) == 10:
        return f"{nums[0]}{nums[1]}{nums[2]}-{nums[3]}{nums[4]}{nums[5]}-{nums[6]}{nums[7]}{nums[8]}{nums[9]}"
    return clean(s)


def walk_list_items(obj, out):
    if isinstance(obj, dict):
        if obj.get("@type") == "ListItem" and isinstance(obj.get("item"), dict):
            out.append(obj["item"])
        for value in obj.values():
            walk_list_items(value, out)
    elif isinstance(obj, list):
        for value in obj:
            walk_list_items(value, out)


def parse_address(addr):
    if not isinstance(addr, dict):
        return ""
    parts = []
    for key in ["streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry"]:
        value = addr.get(key)
        if value:
            parts.append(str(value))
    loc = ", ".join(parts)
    return loc.replace("BC, BC,", "BC,").replace(", CA", ", Canada")


def infer_city(location, fallback=""):
    loc = location or ""
    for city in known_city_names:
        if re.search(r"\b" + re.escape(city) + r"\b", loc, re.I):
            # Normalize neighbourhoods to municipality where useful.
            if city in {"Tsawwassen", "Ladner"}:
                return "Delta"
            if city in {"Cloverdale", "Fleetwood"}:
                return "Surrey"
            if city == "Fort Langley":
                return "Langley"
            if city in {"Oyama", "Winfield"}:
                return "Lake Country"
            return city
    return fallback


def yp_search_page(city, page):
    url = f"{BASE}/search/si/{page}/Roofers/{quote_plus(city + ' BC')}"
    r = session.get(url, timeout=35)
    r.raise_for_status()
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', r.text, re.S)
    if not match:
        return []
    data = json.loads(match.group(1))
    items = []
    walk_list_items(data, items)
    rows = []
    for item in items:
        name = clean(item.get("name"))
        if not name or exclude_name_re.search(name):
            continue
        typ = str(item.get("@type", ""))
        if "RoofingContractor" not in typ and not roof_re.search(name):
            continue
        detail = item.get("url") or ""
        if detail.startswith("/"):
            detail = urljoin(BASE, detail)
        addr = parse_address(item.get("address") or {})
        city_from_addr = infer_city(addr, city)
        rows.append({
            "Name": name,
            "Website": "",
            "Phone number": "",
            "City": city_from_addr,
            "Location": addr or f"{city}, BC",
            "Search cities": city,
            "Detail URL": detail,
            "Source": "YellowPages",
            "Website active": "",
            "Website check": "",
            "Final URL": "",
        })
    return rows


def decode_yp_website(text):
    candidates = []
    for match in re.finditer(r'href="([^"]*?/gourl/[^"]+)"', text):
        href = html.unescape(match.group(1))
        redirected = parse_qs(urlparse(href).query).get("redirect", [""])[0]
        if redirected:
            candidates.append(unquote(redirected))
    bad = ("facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com", "yellowpages.ca", "pagesjaunes.ca", "google.com", "youtube.com")
    for url in candidates:
        if not any(b in url.lower() for b in bad):
            return url
    return ""


def parse_yp_detail(row):
    row = row.copy()
    detail = row.get("Detail URL", "")
    if not detail:
        return row
    try:
        r = session.get(detail, timeout=35)
        if r.status_code != 200:
            row["Detail error"] = f"HTTP {r.status_code}"
            return row
        text = r.text
        # Visible phone numbers; JSON-LD phone is often masked.
        phones = []
        for match in re.finditer(r'<span class="mlr__sub-text"[^>]*>(.*?)</span>', text, re.S):
            candidate = clean(match.group(1))
            if phone_re.search(candidate):
                phones.append(candidate)
        if not phones:
            phones = [m.group(0) for m in phone_re.finditer(text) if "****" not in m.group(0)]
        if phones:
            row["Phone number"] = normalize_phone(phones[0])
        website = decode_yp_website(text)
        if website:
            row["Website"] = website
        # Fill address from detail JSON-LD if richer.
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                data = json.loads(match.group(1))
            except Exception:
                continue
            graphs = data.get("@graph", []) if isinstance(data, dict) else []
            for graph in graphs:
                if not isinstance(graph, dict):
                    continue
                gname = clean(graph.get("name"))
                if gname and normalize_name(gname) == normalize_name(row["Name"]):
                    addr = parse_address(graph.get("address") or {})
                    if addr and (not row.get("Location") or row["Location"].endswith(", BC")):
                        row["Location"] = addr
                        row["City"] = infer_city(addr, row["City"])
    except Exception as exc:
        row["Detail error"] = str(exc)[:120]
    return row


def nominatim_city_search(city):
    rows = []
    # Nominatim is sparse for contractors; use it as supplement/cross-reference only.
    query = f"roofing {city} BC"
    try:
        r = session.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 50, "addressdetails": 1, "extratags": 1},
            headers={**HEADERS, "User-Agent": "HermesLeadGen/1.0"},
            timeout=30,
        )
        if r.status_code != 200:
            return rows
        for item in r.json():
            tags = item.get("extratags") or {}
            name = (item.get("display_name", "").split(",")[0]).strip()
            if not name or exclude_name_re.search(name):
                continue
            if item.get("type") != "roofer" and not roof_re.search(name):
                continue
            addr = item.get("address") or {}
            road = " ".join([addr.get("house_number", ""), addr.get("road", "")]).strip()
            loc_parts = [road, addr.get("city") or addr.get("town") or addr.get("municipality") or addr.get("suburb"), addr.get("state"), addr.get("postcode"), addr.get("country")]
            loc = ", ".join([part for part in loc_parts if part]) or item.get("display_name", "")
            rows.append({
                "Name": name,
                "Website": tags.get("website", "") or tags.get("contact:website", ""),
                "Phone number": normalize_phone(tags.get("phone", "") or tags.get("contact:phone", "")),
                "City": infer_city(loc, city),
                "Location": loc,
                "Search cities": city,
                "Detail URL": "OpenStreetMap/Nominatim",
                "Source": "OpenStreetMap",
                "Website active": "",
                "Website check": "",
                "Final URL": "",
            })
        time.sleep(1.05)  # Nominatim courtesy delay.
    except Exception:
        pass
    return rows


def canonical_urls(url):
    url = (url or "").strip()
    if not url:
        return []
    if url.startswith("//"):
        url = "https:" + url
    if not re.match(r"https?://", url, re.I):
        url = "https://" + url
    parsed = urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"
    bare = host[4:] if host.startswith("www.") else host
    www = "www." + bare
    candidates = [url]
    for scheme in ["https", "http"]:
        for h in [host, bare, www]:
            candidate = f"{scheme}://{h}{path}"
            if candidate not in candidates:
                candidates.append(candidate)
    return candidates


def name_tokens(name):
    stop = {"roofing", "roofers", "roof", "limited", "ltd", "inc", "company", "services", "service", "and", "the", "co", "corp", "corporation", "group", "drains", "drainage"}
    return [w.lower() for w in re.findall(r"[A-Za-z]{4,}", name or "") if w.lower() not in stop]


def fetch_best_website(url):
    errors = []
    for candidate in canonical_urls(url):
        try:
            resp = session.get(candidate, timeout=16, allow_redirects=True, verify=True)
        except requests.exceptions.SSLError:
            try:
                resp = session.get(candidate, timeout=16, allow_redirects=True, verify=False)
            except Exception as exc:
                errors.append(f"{candidate}: {exc}")
                continue
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
            continue
        text = resp.text or ""
        if resp.status_code < 400 and not parked_re.search(text) and len(text) > 500:
            return candidate, resp.url, resp.status_code, text, ""
        errors.append(f"{candidate}: status={resp.status_code} len={len(text)} parked={bool(parked_re.search(text))}")
    return url, "", "", "", " | ".join(errors)[:350]


def validate_website(row):
    row = row.copy()
    url = row.get("Website", "")
    row["Website active"] = "No"
    row["Website check"] = ""
    row["Final URL"] = ""
    if not url:
        row["Website check"] = "no website listed"
        return row
    chosen, final_url, status, text, error = fetch_best_website(url)
    row["Website"] = chosen
    row["Final URL"] = final_url
    if not text:
        row["Website check"] = "not reachable or parked: " + error
        return row
    plain = clean(text)
    checks = []
    if roof_re.search(plain):
        checks.append("roofing content")
    phone_digits = digits(row.get("Phone number", ""))
    if phone_digits and phone_digits[-7:] in digits(plain):
        checks.append("phone match")
    tokens = name_tokens(row.get("Name", ""))
    if tokens and any(token in plain.lower() for token in tokens[:4]):
        checks.append("name match")
    if row.get("City") and re.search(r"\b" + re.escape(row["City"]) + r"\b", plain, re.I):
        checks.append("city match")
    if re.search(r"lower mainland|metro vancouver|greater vancouver|fraser valley|okanagan|british columbia|\bBC\b", plain, re.I):
        checks.append("regional match")
    if "roofing content" in checks and ("phone match" in checks or "name match" in checks or "city match" in checks or "regional match" in checks):
        row["Website active"] = "Yes"
    row["Website check"] = ", ".join(checks) if checks else "active HTTP but no roofing/company/local cross-reference"
    return row


def add_checkboxes(row):
    for col in CHECKBOX_COLS:
        row[col] = "☐"
    return row


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    city_audit = []
    raw_rows = []

    print("Searching cities one by one...")
    for city in CITIES:
        before = len(raw_rows)
        page_counts = []
        for page in range(1, 25):
            try:
                rows = yp_search_page(city, page)
            except Exception as exc:
                city_audit.append({"City": city, "Page": page, "Rows": 0, "Note": f"error: {exc}"})
                break
            city_audit.append({"City": city, "Page": page, "Rows": len(rows), "Note": ""})
            page_counts.append(len(rows))
            if not rows:
                break
            raw_rows.extend(rows)
            # If page is mostly unrelated/duplicate late pages, keep going until empty; de-dupe later.
            time.sleep(0.08)
        osm_rows = nominatim_city_search(city)
        raw_rows.extend(osm_rows)
        print(f"  {city}: +{len(raw_rows)-before} raw rows ({sum(page_counts)} YP, {len(osm_rows)} OSM)")

    # Detail scrape only unique YP detail URLs; merge search-city coverage for duplicate detail URLs.
    by_detail = {}
    for row in raw_rows:
        key = row.get("Detail URL") if row.get("Detail URL") and row.get("Detail URL") != "OpenStreetMap/Nominatim" else "osm:" + normalize_name(row["Name"])
        if key not in by_detail:
            by_detail[key] = row
        else:
            existing = by_detail[key]
            cities = set([c.strip() for c in existing.get("Search cities", "").split(";") if c.strip()])
            cities.add(row.get("Search cities", ""))
            existing["Search cities"] = "; ".join(sorted(cities))
            # Prefer richer location and direct website/phone.
            for field in ["Website", "Phone number", "Location", "City"]:
                if not existing.get(field) and row.get(field):
                    existing[field] = row[field]

    unique_seed = list(by_detail.values())
    yp_seed = [r for r in unique_seed if r.get("Detail URL") and r.get("Detail URL") != "OpenStreetMap/Nominatim"]
    osm_seed = [r for r in unique_seed if r.get("Detail URL") == "OpenStreetMap/Nominatim"]

    print(f"Fetching detail pages for {len(yp_seed)} unique YellowPages listings...")
    detailed = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(parse_yp_detail, row) for row in yp_seed]
        for idx, future in enumerate(as_completed(futures), 1):
            detailed.append(future.result())
            if idx % 100 == 0:
                print(f"  detail pages: {idx}/{len(yp_seed)}")
    detailed.extend(osm_seed)

    # De-dupe by normalized name + phone where possible. Merge website/phone/location/city/search cities.
    merged = {}
    for row in detailed:
        if exclude_name_re.search(row.get("Name", "")):
            continue
        if not (roof_re.search(row.get("Name", "")) or roof_re.search(row.get("Website", "")) or roof_re.search(row.get("Detail URL", ""))):
            continue
        key = normalize_name(row.get("Name", ""))
        if not key:
            continue
        if key not in merged:
            merged[key] = row.copy()
        else:
            current = merged[key]
            for field in ["Website", "Phone number", "Location", "City", "Final URL"]:
                if not current.get(field) and row.get(field):
                    current[field] = row[field]
            city_set = set([c.strip() for c in current.get("Search cities", "").split(";") if c.strip()])
            city_set.update([c.strip() for c in row.get("Search cities", "").split(";") if c.strip()])
            current["Search cities"] = "; ".join(sorted(city_set))
            if row.get("Source") and row["Source"] not in current.get("Source", ""):
                current["Source"] = current.get("Source", "") + "+" + row["Source"]

    rows = list(merged.values())
    for row in rows:
        row["City"] = infer_city(row.get("Location", ""), row.get("City", ""))
        if not row["City"]:
            # Use first search city as service area if exact city is unavailable.
            row["City"] = row.get("Search cities", "").split(";")[0].strip()
        if not row.get("Location"):
            row["Location"] = f"{row['City']}, BC"

    print(f"Validating websites for {len(rows)} deduped companies...")
    validated = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(validate_website, row) for row in rows]
        for idx, future in enumerate(as_completed(futures), 1):
            validated.append(future.result())
            if idx % 100 == 0:
                print(f"  website checks: {idx}/{len(rows)}")

    active_with_websites = []
    no_website = []
    for row in validated:
        if row.get("Website") and row.get("Website active") == "Yes":
            active_with_websites.append(add_checkboxes(row.copy()))
        elif not row.get("Website") and row.get("Phone number"):
            opp = row.copy()
            opp["Needs website"] = "Yes"
            no_website.append(add_checkboxes(opp))

    # Sort and write.
    active_with_websites.sort(key=lambda r: (r.get("City", ""), r.get("Name", "")))
    no_website.sort(key=lambda r: (r.get("City", ""), r.get("Name", "")))
    validated.sort(key=lambda r: (r.get("City", ""), r.get("Name", "")))

    active_fields = ["Name", "Website", "Phone number", "City", "Location"] + CHECKBOX_COLS
    no_web_fields = ["Name", "Phone number", "City", "Location", "Needs website"] + CHECKBOX_COLS
    audit_fields = ["Name", "Website", "Phone number", "City", "Location", "Search cities", "Website active", "Website check", "Final URL", "Source", "Detail URL"]

    with open(ACTIVE_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=active_fields)
        writer.writeheader()
        for row in active_with_websites:
            writer.writerow({field: row.get(field, "") for field in active_fields})

    with open(NO_WEBSITE_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=no_web_fields)
        writer.writeheader()
        for row in no_website:
            writer.writerow({field: row.get(field, "") for field in no_web_fields})

    with open(AUDIT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=audit_fields)
        writer.writeheader()
        for row in validated:
            writer.writerow({field: row.get(field, "") for field in audit_fields})

    with open(CITY_AUDIT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["City", "Page", "Rows", "Note"])
        writer.writeheader()
        writer.writerows(city_audit)

    summary = {
        "cities_searched": CITIES,
        "raw_rows": len(raw_rows),
        "unique_seed_listings": len(unique_seed),
        "deduped_companies": len(rows),
        "active_with_websites": len(active_with_websites),
        "no_website_opportunities": len(no_website),
        "active_csv": ACTIVE_CSV,
        "no_website_csv": NO_WEBSITE_CSV,
        "audit_csv": AUDIT_CSV,
        "city_audit_csv": CITY_AUDIT_CSV,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
