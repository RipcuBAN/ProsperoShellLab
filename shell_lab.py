"""Read-only artifact identification and public ShellUI evidence inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

REPO = 'etaHEN/etaHEN'
SOURCE = 'Source%20Code/shellui/src/HookFunctions.cpp'


def classify(header):
    if header.startswith(b'\x7fELF'):
        return 'ELF'
    if header.startswith(b'MZ'):
        return 'DOS/PE candidate'
    if header.startswith(b'PK\x03\x04'):
        return 'ZIP container'
    if header.startswith(b'\x4f\x15\x3d\x1d'):
        return 'Sony SELF candidate'
    return 'unknown'


def inspect(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open('rb') as source:
        header = source.read(64)
        digest.update(header)
        size += len(header)
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
            size += len(chunk)
    return {'name': Path(path).name, 'bytes': size, 'sha256': digest.hexdigest(),
            'format': classify(header), 'executed': False, 'portability': 'not established'}


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'ProsperoShellLab/0.1'}), timeout=30) as response:
        return response.read()


def extract(text):
    patterns = {
        'managed_namespaces': r'"(Sce\.[A-Za-z0-9_.]+)"',
        'mono_api_references': r'\b(mono_[A-Za-z0-9_]+)\b',
        'integration_identifiers': r'\b(GetManifestResourceStream\w*|CxmlUri|LaunchApp\w*|DecryptRnpsBundle\w*)\b',
    }
    return {key: sorted(set(re.findall(pattern, text))) for key, pattern in patterns.items()}


def public_inventory():
    revision = json.loads(fetch(f'https://api.github.com/repos/{REPO}/commits/main'))['sha']
    url = f'https://raw.githubusercontent.com/{REPO}/{revision}/{SOURCE}'
    payload = fetch(url)
    return {'repository': f'https://github.com/{REPO}', 'revision': revision,
            'source': url, 'source_sha256': hashlib.sha256(payload).hexdigest(),
            'evidence': 'Identifiers referenced in public hook code; original implementations unavailable here',
            'references': extract(payload.decode('utf-8-sig')),
            'next_required_artifacts': ['ShellUI executable', 'referenced managed assemblies',
                                        'UI resources', 'service dependency inventory']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('public').add_argument('--output', type=Path)
    local = commands.add_parser('inspect')
    local.add_argument('path', type=Path)
    local.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = public_inventory() if args.command == 'public' else inspect(args.path)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')


if __name__ == '__main__':
    main()
