#!/usr/bin/env python3
"""
Extract candidate taxonomy terms from Obsidian vault or markdown files.

Usage:
    python analyze_vault_terms.py <vault-path> --output candidate_terms.csv --min-frequency 2
"""

import os
import re
import csv
import argparse
from pathlib import Path
from collections import Counter
import yaml

def extract_yaml_tags(file_path):
    """Extract tags from YAML frontmatter."""
    tags = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                try:
                    data = yaml.safe_load(frontmatter)
                    if data and 'tags' in data:
                        tag_data = data['tags']
                        if isinstance(tag_data, list):
                            tags.extend(tag_data)
                        elif isinstance(tag_data, str):
                            tags.append(tag_data)
                except:
                    pass
    except:
        pass

    return tags

def extract_inline_tags(content):
    """Extract inline #tags from content."""
    return re.findall(r'#([\w-]+)', content)

def extract_headings(content):
    """Extract headings (H1-H3)."""
    headings = []
    for match in re.finditer(r'^#{1,3}\s+(.+)$', content, re.MULTILINE):
        heading = match.group(1).strip()
        # Remove markdown formatting
        heading = re.sub(r'[*_`\[\]]', '', heading)
        headings.append(heading)
    return headings

def extract_noun_phrases(content):
    """Extract potential noun phrases (simple heuristic)."""
    # Remove code blocks and inline code
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)

    # Extract capitalized phrases (potential proper nouns)
    phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', content)
    return phrases

def analyze_vault(vault_path, min_frequency=2):
    """Analyze vault and extract candidate terms."""
    terms = Counter()
    term_sources = {}  # Track which files contain each term

    vault_path = Path(vault_path)

    # Find all markdown files
    md_files = list(vault_path.rglob('*.md'))

    print(f"Analyzing {len(md_files)} markdown files...")

    for md_file in md_files:
        rel_path = md_file.relative_to(vault_path)

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract tags from YAML
            yaml_tags = extract_yaml_tags(md_file)
            for tag in yaml_tags:
                terms[tag] += 1
                term_sources.setdefault(tag, set()).add(str(rel_path))

            # Extract inline tags
            inline_tags = extract_inline_tags(content)
            for tag in inline_tags:
                terms[tag] += 1
                term_sources.setdefault(tag, set()).add(str(rel_path))

            # Extract headings
            headings = extract_headings(content)
            for heading in headings:
                terms[heading] += 1
                term_sources.setdefault(heading, set()).add(str(rel_path))

            # Extract noun phrases
            phrases = extract_noun_phrases(content)
            for phrase in phrases:
                if len(phrase.split()) >= 2:  # Multi-word phrases only
                    terms[phrase] += 1
                    term_sources.setdefault(phrase, set()).add(str(rel_path))

            # Add folder names
            for part in md_file.parent.parts:
                if part not in ['.', '..'] and not part.startswith('.'):
                    terms[part] += 1
                    term_sources.setdefault(part, set()).add(str(rel_path))

        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            continue

    # Filter by minimum frequency
    filtered_terms = {term: count for term, count in terms.items() if count >= min_frequency}

    return filtered_terms, term_sources

def main():
    parser = argparse.ArgumentParser(description='Extract candidate taxonomy terms from Obsidian vault')
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--output', default='candidate_terms.csv', help='Output CSV file')
    parser.add_argument('--min-frequency', type=int, default=2, help='Minimum term frequency')

    args = parser.parse_args()

    # Analyze vault
    terms, sources = analyze_vault(args.vault_path, args.min_frequency)

    # Write results to CSV
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Term', 'Frequency', 'Source Files'])

        # Sort by frequency (descending)
        for term, count in sorted(terms.items(), key=lambda x: x[1], reverse=True):
            source_list = '; '.join(sorted(sources[term])[:3])  # First 3 sources
            if len(sources[term]) > 3:
                source_list += f' (+{len(sources[term]) - 3} more)'
            writer.writerow([term, count, source_list])

    print(f"\nExtracted {len(terms)} candidate terms (min frequency: {args.min_frequency})")
    print(f"Results written to: {args.output}")
    print(f"\nTop 10 terms:")
    for term, count in sorted(terms.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {term}: {count}")

if __name__ == '__main__':
    main()
