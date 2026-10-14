# Norme de traduction française

Ce document définit la base terminologique et stylistique des pages françaises de
doc.pg.center. L'anglais est la source de vérité. Une traduction française est placée à
côté de sa source et porte le suffixe `.fr.md`.

## Périmètre et structure

- Traduire les titres, descriptions, résumés, textes de navigation, paragraphes,
  listes explicatives, en-têtes de tableau, libellés de liens et textes alternatifs.
- Conserver tels quels les noms de produits et protocoles, commandes, options,
  mots-clés de configuration, API/RPC, messages, champs, variables d'environnement,
  métriques, noms de fichiers, chemins, URL, versions et espaces réservés.
- Ne pas traduire les commandes, configurations, sources, sorties, journaux et
  messages d'erreur copiables, ni le texte des licences.
- Préserver les blocs de code clôturés ou indentés octet pour octet, y compris
  leurs commentaires, sauf les exceptions pgBadger et HAProxy enregistrées ci-dessous. Préserver
  exactement les shortcodes, notes de bas de page, balises HTML, définitions de
  référence, ancres explicites et nombres.
- Uniquement dans les blocs explicatifs `text` de `content/docs/pgbadger/`
  enregistrés et revus indépendamment, traduire l'aide des paramètres, les
  explications des codes de retour, les étapes en langue naturelle du pseudocode
  algorithmique, les descriptions de répertoires et leurs commentaires
  explicatifs d'exemples. Conserver exactement les signatures CLI réelles,
  options, valeurs autorisées, valeurs par défaut, commandes, SQL, configurations,
  expressions régulières, diagnostics, textes juridiques, noms de personnes,
  nombres et formules. Cette exception ne permet pas de traduire les
  commentaires du code réel.
- Enregistrer chaque exception dans `data/translation-fences/pgbadger.fr/` avec
  les SHA-256 exacts du bloc source et traduit (`source_sha256`, `target_sha256`),
  les littéraux protégés (`protected_literals`) et les lignes de commande ou de
  sortie réelles (`protected_lines`). Un réviseur indépendant doit vérifier le
  sens et les littéraux. Un bloc non enregistré ou dont le hachage a changé reste
  protégé octet pour octet ; l'étiquette `text` seule ne constitue pas une exception.
- Dans les blocs HAProxy clôturés ou indentés, traduire uniquement les descriptions
  d'arguments, libellés de tableaux et explications en langue naturelle enregistrés
  dans `data/translation-fences/haproxy.fr/`. Enregistrer les hachages exacts, la
  classification, la conclusion de revue indépendante et les littéraux et lignes
  protégés. Les configurations, commandes, sources, messages de protocole, sorties,
  diagnostics et commentaires du code réel restent identiques octet pour octet,
  y compris dans les blocs mixtes. Un bloc non enregistré ou modifié n'est pas exempté.
- Conserver les identifiants de type `integer`, `boolean`, `bool`, `string`, `binary`
  et `ip` dans les signatures d'échantillons HAProxy et leurs anciens alias.
  Traduire normalement les descriptions de types dans le texte explicatif.
- Le texte destiné aux lecteurs ne contient que des informations utiles à
  l'utilisation du produit. Ne pas y ajouter de politique de traduction, de
  notes du traducteur, de mention « cette page conserve le texte original » ou de
  récit du processus de correction éditoriale. Conserver les données
  d'attribution et les textes juridiques originaux.
- Ajouter aux titres traduits l'identifiant rendu par le titre anglais lorsqu'aucune
  ancre explicite n'existe, afin de conserver les liens profonds entre langues.
- Préfixer les liens vers une page traduite par `/fr/`. Les images et autres actifs
  partagés conservent leur chemin sans préfixe de langue.

## Style

- Employer le français de France, précis et naturel, destiné aux administrateurs
  Linux, réseau, PostgreSQL et systèmes distribués.
- Préférer des phrases directes et concises. Ne rien omettre, résumer ou développer.
- Rendre `must` par une obligation explicite, `should` par une recommandation et
  `may/can` par une possibilité, sans modifier la force normative.
- Conserver les graphies `Patroni`, `pgBackRest`, `PgBouncer`, `pgBadger`, `HAProxy`,
  `etcd`, `PostgreSQL`, `Prometheus`, `Grafana`, `Kubernetes` et `OpenSSL`.
- Employer une typographie française cohérente, tout en évitant les espaces
  insécables dans le code, les identifiants et les URL.

## Glossaire site

| Anglais | Français |
| --- | --- |
| documentation | documentation |
| upstream | projet amont |
| release notes | notes de version |
| search | recherche |
| section | section |
| page | page |
| language | langue |
| translation | traduction |

## Glossaire patroni

| Anglais | Français |
| --- | --- |
| cluster | cluster |
| leader | leader |
| primary | primaire |
| replica | réplique |
| failover | basculement |
| switchover | basculement planifié |
| distributed configuration store | magasin de configuration distribué |
| high availability | haute disponibilité |
| synchronous mode | mode synchrone |
| standby cluster | cluster de secours |
| watchdog | watchdog |
| bootstrap | amorçage |

## Glossaire pgbackrest

| Anglais | Français |
| --- | --- |
| backup | sauvegarde |
| restore | restauration |
| repository | dépôt |
| stanza | stanza |
| archive | archive |
| retention | rétention |
| full backup | sauvegarde complète |
| differential backup | sauvegarde différentielle |
| incremental backup | sauvegarde incrémentielle |
| point-in-time recovery | restauration à un instant donné |
| checksum | somme de contrôle |

## Glossaire pgbouncer

| Anglais | Français |
| --- | --- |
| connection pooler | pooler de connexions |
| connection pool | pool de connexions |
| target application | application cliente |
| transaction semantics | sémantique transactionnelle |
| rotating connections | rotation des connexions |
| most polite method | méthode la moins intrusive |
| most aggressive method | méthode la plus agressive |
| session pooling | pooling de sessions |
| transaction pooling | pooling de transactions |
| statement pooling | pooling d'instructions |
| authentication | authentification |
| client | client |
| server | serveur |
| routing | routage |
| console | console d'administration |

## Glossaire pgbadger

| Anglais | Français |
| --- | --- |
| log analyzer | analyseur de journaux |
| log file | fichier journal |
| report | rapport |
| query | requête |
| slow query | requête lente |
| lock | verrou |
| checkpoint | point de contrôle |
| incremental report | rapport incrémentiel |
| output format | format de sortie |

## Glossaire HAProxy

| Anglais | Français |
| --- | --- |
| frontend | frontal |
| backend | backend |
| proxy | proxy |
| load balancer | répartiteur de charge |
| load balancing | répartition de charge |
| health check | contrôle d'état |
| stick table | table de persistance |
| sample fetch | extraction d'échantillon |
| access control list | liste de contrôle d'accès |
| listener | écouteur |
| listening socket | socket d'écoute |
| graceful shutdown | arrêt progressif |
| graceful reload | rechargement sans interruption |
| runtime API | API d'exécution |
| runtime CLI | CLI d'exécution |
| troubleshooting | dépannage |
| request | requête |
| response | réponse |
| header | en-tête |
| throughput | débit |
| timeout | délai d'expiration |

## Glossaire etcd

| Anglais | Français |
| --- | --- |
| cluster | cluster |
| member | membre |
| leader | leader |
| follower | suiveur |
| learner | membre apprenant |
| key-value store | magasin clé-valeur |
| keyspace | espace de clés |
| lease | bail |
| watch | surveillance |
| watcher | observateur |
| revision | révision |
| compaction | compactage |
| defragmentation | défragmentation |
| quorum | quorum |
| consensus | consensus |
| snapshot | instantané |
| rolling upgrade | mise à niveau progressive |
| recovery | récupération |
| linearizable read | lecture linéarisable |
| serializable read | lecture sérialisable |
| write-ahead log | journal d'écriture anticipée |

## Validation

Chaque page anglaise doit posséder exactement une page française au même chemin
logique. Les métadonnées de routage, liens amont, ancres, blocs de code, shortcodes,
actifs et références doivent rester structurellement identiques. Les blocs de code
restent identiques octet pour octet, sauf les blocs explicatifs pgBadger et HAProxy
dont les hachages et littéraux exacts sont enregistrés et revus indépendamment
selon les règles ci-dessus ; le code réel et ses commentaires restent protégés.
Vérifier aussi l'absence de politique de traduction, de notes du traducteur et de
récit du travail éditorial dans le texte destiné aux lecteurs. La validation se
termine par une construction Hugo de production et un contrôle des liens internes.
