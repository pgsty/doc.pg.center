#!/usr/bin/env python3
"""Update the two six-language guides from verified stable-tag execution caches.

Download doc/resource/exe.cache for both release tags outside this repository.
The old guide outputs must match before any file is written. No command in the
documentation or cache is executed. Defaults to a dry run; pass --write to save.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent / 'content/docs/pgbackrest'
LANGUAGES = ('en', 'zh', 'fr', 'ja', 'de', 'ru')
FENCE = re.compile(r'(^```[^\n]*\n)(.*?)(^```)', re.M | re.S)


def normalized(value):
    # The original HTML-to-Markdown import omitted blank output lines and
    # trailing spaces. Match that presentation without weakening token checks.
    return '\n'.join(line.rstrip() for line in value.splitlines() if line.strip())


def output(entry):
    return '\n'.join(line.rstrip() for line in entry.get('value', {}).get('output', []))


def prepare(old, new, old_version, new_version):
    changes, receipts = {}, {}
    for environment, name in [('default', 'user-guide'), ('{"os-type":"rhel"}', 'user-guide-rhel')]:
        before = old[environment]['all']['user-guide']
        after = new[environment]['all']['user-guide']
        if len(before) != len(after):
            raise ValueError(name + ': cache command sequence changed; review the new structure first')
        replacements, selectors = {}, {}
        for a, b in zip(before, after, strict=True):
            left, right = output(a), output(b)
            if left and left != right:
                key = normalized(left)
                if key in replacements and replacements[key] != right:
                    raise ValueError(name + ': ambiguous output replacement')
                replacements[key] = right
                if re.fullmatch(r'\d{8}-\d{6}F(?:_\d{8}-\d{6}[DI])?|\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\+00', left):
                    selectors[left] = right
            # PITR target timestamps include fractions and are interpolated
            # into commands rather than emitted as standalone cache outputs.
            pattern = r'--target=(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d(?:\.\d+)?\+00)'
            targets = [re.findall(pattern, '\n'.join(e['key'].get('cmd', []))) for e in (a, b)]
            for left, right in zip(*targets, strict=True):
                if left in selectors and selectors[left] != right:
                    raise ValueError(name + ': ambiguous recovery target replacement')
                selectors[left] = right
        for a, b in zip(before, after, strict=True):
            key = json.dumps(a['key'], sort_keys=True).replace(old_version, new_version)
            for left, right in sorted(selectors.items(), key=lambda pair: -len(pair[0])):
                key = key.replace(left, right)
            if a['type'] != b['type'] or key != json.dumps(b['key'], sort_keys=True):
                raise ValueError(name + ': cache command identity changed; manual review required')
        original = (ROOT / (name + '.md')).read_text()
        matched = defaultdict(int)
        def update(match):
            key = normalized(match[2])
            if key not in replacements:
                return match[0]
            matched[key] += 1
            return match[1] + replacements[key].strip('\n') + '\n' + match[3]
        updated = FENCE.sub(update, original)
        unaccounted = set(replacements) - set(matched) - set(selectors)
        if unaccounted:
            raise ValueError(name + ': changed cached output does not match the current guide: ' + repr(sorted(unaccounted)[0][:120]))
        updated = updated.replace(old_version, new_version)
        for left, right in sorted(selectors.items(), key=lambda pair: -len(pair[0])):
            updated = updated.replace(left, right)
        old_fences = list(FENCE.finditer(original))
        new_fences = list(FENCE.finditer(updated))
        for language in LANGUAGES:
            target = ROOT / (name + ('' if language == 'en' else '.' + language) + '.md')
            text = target.read_text()
            local = list(FENCE.finditer(text))
            if [m[2] for m in local] != [m[2] for m in old_fences]:
                raise ValueError(str(target) + ': protected blocks differ before synchronization')
            for before_block, after_block in reversed(list(zip(local, new_fences, strict=True))):
                text = text[:before_block.start(2)] + after_block[2] + text[before_block.end(2):]
            text = text.replace(old_version, new_version)
            for left, right in sorted(selectors.items(), key=lambda pair: -len(pair[0])):
                text = text.replace(left, right)
            changes[target] = text
        receipts[name] = {
            'changed_cached_outputs': len(replacements),
            'replaced_output_blocks': sum(matched.values()),
            'updated_selector_values': len(selectors),
            'changed_fences': sum(a[2] != b[2] for a, b in zip(old_fences, new_fences, strict=True)),
            'final_fences_sha256': hashlib.sha256('\n'.join(m[2] for m in new_fences).encode()).hexdigest(),
        }
    return changes, receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-cache', required=True, type=Path)
    parser.add_argument('--to-cache', required=True, type=Path)
    parser.add_argument('--from-version', required=True)
    parser.add_argument('--to-version', required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    changes, receipts = prepare(json.loads(args.from_cache.read_text()), json.loads(args.to_cache.read_text()), args.from_version, args.to_version)
    if args.write:
        for path, text in changes.items():
            path.write_text(text)
    print(json.dumps({'written': args.write, 'files': len(changes), 'guides': receipts}, indent=2))


if __name__ == '__main__':
    main()
