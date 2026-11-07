{{- .Page.Store.Set "tdOutputFormat" "markdown" -}}
{{- partial "content/markdown-document.md" . -}}
{{- partial "pgsql/export-annotations.md" . -}}
