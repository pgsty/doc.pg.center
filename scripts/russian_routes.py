"""Transform complete site URL values without rewriting external URL internals."""

import re
from urllib.parse import urlsplit


PROSE_URL_RE = re.compile(
    r"(?:(?<!\S)|(?<=[(<\"']))(?:https?://|/)[^\s<>\"']+", flags=re.I,
)
HTML_TAG_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9:_-]*(?:\s[^>\n]*)?/?>")
HTML_URL_ATTRIBUTE_RE = re.compile(
    r"(?<![\w:-])(?:href|src|link|poster|action)\s*=\s*"
    r"(?:(?P<quote>[\"'])(?P<quoted>.*?)(?P=quote)|(?P<unquoted>[^\s>]+))",
    flags=re.I,
)
ASSET_RE = re.compile(
    r"\.(?:png|jpe?g|gif|webp|avif|svg|ico|pdf|zip|tar|gz|json|txt|csv|"
    r"ya?ml|toml|ini|conf)$", flags=re.I,
)


def transform_route_text(text, routes, *, localize=False, preserve_assets=False,
                         allow_site_absolute=True):
    """Only change a complete root path or an explicitly allowed same-site URL.

    The caller protects code/inline literals. Tokens include entire URLs, so a
    path or query parameter inside an external URL cannot become a new match.
    Slice only the parsed path to retain query/fragment delimiters verbatim.
    """
    def transform_value(token):
        value = token
        if not value.startswith("/") and not re.match(r"https?://", value, flags=re.I):
            return token
        try:
            parsed = urlsplit(value)
        except ValueError:
            return token
        if parsed.scheme and (parsed.scheme not in {"http", "https"} or not parsed.netloc):
            return token
        if parsed.netloc and (not allow_site_absolute or parsed.netloc.lower() != "doc.pg.center"):
            return token
        path = parsed.path
        localized = path.startswith("/ru/")
        bare = path[3:] if localized else path
        if not any(bare == "/" + route or bare.startswith("/" + route + "/") for route in routes):
            return token
        if localize:
            replacement = bare if preserve_assets and ASSET_RE.search(bare) else "/ru" + bare
        else:
            replacement = bare
        if replacement == path:
            return token
        offset = (len(parsed.scheme) + 3 if parsed.scheme else 2) + len(parsed.netloc) if parsed.netloc else 0
        return value[:offset] + replacement + value[offset + len(path):]

    def prose_url(match):
        value = match.group()
        # Keep balanced parentheses within a URL. The first unmatched closing
        # parenthesis belongs to surrounding Markdown/prose, including any
        # following punctuation; it must not affect asset classification.
        depth = 0
        for index, char in enumerate(value):
            if char == "(":
                depth += 1
            elif char == ")":
                if not depth:
                    return transform_value(value[:index]) + value[index:]
                depth -= 1
        return transform_value(value)

    def transform_tag(match):
        def attribute_value(attribute):
            group = "quoted" if attribute.group("quote") else "unquoted"
            value = attribute.group(group)
            left = attribute.start(group) - attribute.start()
            right = attribute.end(group) - attribute.start()
            original = attribute.group()
            return original[:left] + transform_value(value) + original[right:]
        return HTML_URL_ATTRIBUTE_RE.sub(attribute_value, match.group())

    result = []
    previous = 0
    for tag in HTML_TAG_RE.finditer(text):
        result.append(PROSE_URL_RE.sub(prose_url, text[previous:tag.start()]))
        result.append(transform_tag(tag))
        previous = tag.end()
    result.append(PROSE_URL_RE.sub(prose_url, text[previous:]))
    return "".join(result)
