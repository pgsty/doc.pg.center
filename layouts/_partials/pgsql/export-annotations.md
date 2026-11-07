{{- /* Preserve imported collection source notices in text exports without duplicating
     the visible HTML credit. OINK resolves and validates the same metadata
     for the page annotation; this adapter only formats its links as Markdown. */ -}}
{{- if in (slice "orioledb" "citus") .Section -}}
  {{- range partial "annotation-items.html" . -}}
    {{- if in (slice "upstream" "translation") .key -}}
      {{- $text := replaceRE `<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>` "[$2]($1)" .html -}}
      {{- printf "\n\n---\n\n%s\n" ($text | htmlUnescape) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
