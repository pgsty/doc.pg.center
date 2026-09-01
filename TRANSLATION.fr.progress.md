# Progression de la traduction française

Mise à jour : 2026-08-31

La traduction française de l'ensemble du contenu est achevée. L'anglais reste
la source de vérité pour les mises à jour ultérieures.

## Progression du contenu

| Collection | Terminé | Total | État |
| --- | ---: | ---: | --- |
| Patroni | 24 | 24 | terminé |
| PgBouncer | 9 | 9 | terminé |
| pgBadger | 16 | 16 | terminé |
| Pages générales du site | 3 | 3 | terminé |
| pgBackRest | 29 | 29 | terminé |
| HAProxy | 38 | 38 | terminé |
| etcd | 99 | 99 | terminé |
| **Total** | **218** | **218** | **100 %** |

Le shell du site est déjà prêt pour le français : langue `fr-FR` dans
`hugo.yaml`, page d'accueil `data/home/fr.yaml`, pied de page
`data/footer/fr.yaml` et traductions d'interface fournies par OINK 1.0.

## Validation au point d'arrêt

- Les 218 sources anglaises possèdent chacune un unique fichier `*.fr.md`
  correspondant.
- La parité des métadonnées, blocs de code, shortcodes, notes de bas de page,
  liens de référence et autres structures protégées a été validée pour les
  218 paires anglaises et françaises.
- Le contrôle du texte français, hors blocs de code et configurations conservés
  en anglais, a réussi sur l'ensemble du contenu. Le texte anglais de la licence
  PostgreSQL intégrée à pgBadger est volontairement conservé comme texte légal
  faisant autorité.
- `make check` a réussi avec Hugo Extended 0.165.0 : 496 pages françaises ont
  été générées, les liens internes de 1 344 fichiers HTML ont été validés et les
  routes HTML, Markdown, impression, LLMS et navigation françaises ont été
  vérifiées.
- Les contrôles de syntaxe Python et `git diff --check` ont réussi.

## Maintenance

Le générateur est `scripts/translate-component-docs.py`. Le cache français
reprenable se trouve dans `.hugo_cache/translation-cache-fr.json`. Après une
modification de la source anglaise, la collection concernée peut être régénérée,
par exemple :

```sh
python3 scripts/translate-component-docs.py etcd \
  --language fr \
  --scalar-model qwen3:30b-a3b-instruct-2507-q4_K_M
```

Pour une page contenant une longue liste de paramètres sans lignes vides,
relancer la page avec `--max-chars 1000`, puis `--max-chars 500` si nécessaire.
Les traductions sont écrites atomiquement uniquement après validation complète
de la page.

Cette livraison locale n'inclut ni commit, ni push, ni déploiement public.
