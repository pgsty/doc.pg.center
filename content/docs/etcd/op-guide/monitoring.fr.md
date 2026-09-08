---
title: Surveillance d’etcd
weight: 4500
description: "Surveillance d'etcd pour l'intégrité du système et le débogage du cluster"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/monitoring.md"
aliases: [/etcd/op-guide/monitoring/]
---

Chaque serveur etcd fournit des informations de surveillance locales sur son port client via des points de terminaison HTTP. Les données de surveillance sont utiles à la fois pour le contrôle de santé du système et le débogage du cluster.

## Point d'entrée de débogage {#debug-endpoint}

Si `--log-level=debug` est défini, le serveur etcd exporte des informations de débogage sur son port client sous le chemin `/debug`. Prenez garde à la définition de `--log-level=debug`, car cela entraînera une dégradation des performances et une journalisation verbose.

Le point de terminaison `/debug/pprof` est le point de terminaison standard de profilage du runtime Go. Il peut être utilisé pour profiler l'utilisation du processeur, de la mémoire, des verrous et des goroutines. Par exemple, voici comment obtenir les 10 fonctions où etcd consacre le plus de temps :

`go tool pprof`

```sh
$ go tool pprof http://localhost:2379/debug/pprof/profile
Fetching profile from http://localhost:2379/debug/pprof/profile
Please wait... (30s)
Saved profile in /home/etcd/pprof/pprof.etcd.localhost:2379.samples.cpu.001.pb.gz
Entering interactive mode (type "help" for commands)
(pprof) top10
310ms of 480ms total (64.58%)
Showing top 10 nodes out of 157 (cum >= 10ms)
    flat  flat%   sum%        cum   cum%
   130ms 27.08% 27.08%      130ms 27.08%  runtime.futex
    70ms 14.58% 41.67%       70ms 14.58%  syscall.Syscall
    20ms  4.17% 45.83%       20ms  4.17%  github.com/coreos/etcd/vendor/golang.org/x/net/http2/hpack.huffmanDecode
    20ms  4.17% 50.00%       30ms  6.25%  runtime.pcvalue
    20ms  4.17% 54.17%       50ms 10.42%  runtime.schedule
    10ms  2.08% 56.25%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).AuthInfoFromCtx
    10ms  2.08% 58.33%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).Lead
    10ms  2.08% 60.42%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/pkg/wait.(*timeList).Trigger
    10ms  2.08% 62.50%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/prometheus/client_golang/prometheus.(*MetricVec).hashLabelValues
    10ms  2.08% 64.58%       10ms  2.08%  github.com/coreos/etcd/vendor/golang.org/x/net/http2.(*Framer).WriteHeaders
```

Le point de terminaison `/debug/requests` permet d’obtenir des traces gRPC et des statistiques de performance via un navigateur web. Par exemple, voici une requête `Range` pour la clé `abc` :

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## Point d'extrémité des métriques {#metrics-endpoint}

Chaque serveur etcd exporte des métriques sous le chemin `/metrics` sur son port client, et éventuellement sur les emplacements indiqués par `--listen-metrics-urls`.

Les métriques peuvent être récupérées avec `curl` :

```sh
$ curl -L http://localhost:2379/metrics | grep -v debugging # ignore unstable debugging metrics

# HELP etcd_disk_backend_commit_duration_seconds The latency distributions of commit called by backend.
# TYPE etcd_disk_backend_commit_duration_seconds histogram
etcd_disk_backend_commit_duration_seconds_bucket{le="0.002"} 72756
etcd_disk_backend_commit_duration_seconds_bucket{le="0.004"} 401587
etcd_disk_backend_commit_duration_seconds_bucket{le="0.008"} 405979
etcd_disk_backend_commit_duration_seconds_bucket{le="0.016"} 406464
...
```

## Vérification de santé {#health-check}

Depuis la version 3.3.0, outre la réponse à l’endpoint `/metrics`, toutes les localisations spécifiées par `--listen-metrics-urls` répondent également à l’endpoint `/health`. Cela peut être utile si l’endpoint standard est configuré avec une authentification TLS mutuelle (client), mais qu’un équilibreur de charge ou un service de surveillance doit tout de même accéder à la vérification de santé.

Depuis la version 3.4, deux nouveaux points d'entrée `/livez` et `/readyz` ont été ajoutés.

*  le point de terminaison `/livez` indique si le processus est actif ou s'il nécessite un redémarrage.
*  le point de terminaison `/readyz` indique si le processus est prêt à servir le trafic.

Les détails de conception des points de terminaison sont documentés dans le [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz).

Chaque point de terminaison inclut plusieurs vérifications de santé individuelles, et vous pouvez utiliser le paramètre `verbose` pour afficher les détails des vérifications et leur état, par exemple

```bash
curl -k http://localhost:2379/readyz?verbose
```

et vous verriez une réponse similaire à

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

L'API HTTP prend également en charge l'exclusion de vérifications spécifiques, par exemple

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

Exécuter un service de surveillance [Prometheus][prometheus] est la méthode la plus simple pour ingérer et enregistrer les métriques d'etcd.

Tout d’abord, installez Prometheus :

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

Configurez l'extracteur Prometheus pour cibler les points d'accès du cluster etcd :

```sh
cat > /tmp/test-etcd.yaml <<EOF
global:
  scrape_interval: 10s
scrape_configs:
  - job_name: test-etcd
    static_configs:
    - targets: ['10.240.0.32:2379','10.240.0.33:2379','10.240.0.34:2379']
EOF
cat /tmp/test-etcd.yaml
```

Configurez le gestionnaire Prometheus :

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

Prometheus récupérera désormais les métriques etcd toutes les 10 secondes.


### Alerting {#alerting}

Il existe un ensemble d'alertes par défaut [pour les clusters etcd v3 destinées à Prometheus](https://github.com/etcd-io/etcd/tree/main/contrib/mixin).

> [!NOTE]
> Notez que les étiquettes `job` peuvent nécessiter un ajustement pour répondre à un besoin particulier. Les règles ont été rédigées pour s'appliquer à un seul cluster, il est donc recommandé de choisir des étiquettes uniques par cluster.

### Grafana {#grafana}

[Grafana][grafana] dispose d’un support intégré pour Prometheus ; ajoutez simplement une source de données Prometheus :

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

Ensuite, importez le modèle de tableau de bord par défaut [etcd dashboard template][template] et personnalisez-le. Par exemple, si le nom de la source de données Prometheus est `my-etcd`, les valeurs du champ `datasource` dans le JSON doivent également être `my-etcd`.

Tableau de bord d'exemple :

![ ](/docs/etcd/op-guide/etcd-sample-grafana.png)

## Traçage distribué {#distributed-tracing}

À partir de la version 3.5, etcd prend en charge le traçage distribué à l’aide de [OpenTelemetry](https://github.com/open-telemetry).

> [!NOTE]
> Cette fonctionnalité est encore expérimentale et peut être modifiée à tout moment.

Pour activer cette fonctionnalité expérimentale, passez le paramètre `--experimental-enable-distributed-tracing=true` au serveur etcd, ainsi que le drapeau `--experimental-distributed-tracing-sampling-rate=<number>` pour choisir le nombre d'échantillons à collecter par million de spans ; le taux d'échantillonnage par défaut est `0`.

Configurez le traçage distribué en lançant le serveur etcd avec les indicateurs facultatifs suivants :

- `--experimental-distributed-tracing-address` - (Facultatif) - « localhost:4317 » - Adresse du collecteur de traçage.

- `--experimental-distributed-tracing-service-name` - (Facultatif) - « etcd » - Nom du service de traçage distribué, doit être identique sur toutes les instances etcd.

- `--experimental-distributed-tracing-instance-id` - (Facultatif) - Identifiant d'instance ; bien qu'optionnel, il est fortement recommandé de le définir, et doit être unique par instance etcd.

Avant d’activer le traçage distribué, assurez-vous d’avoir un point de terminaison OpenTelemetry. Si cette adresse diffère de la valeur par défaut, remplacez-la à l’aide du drapeau `--experimental-distributed-tracing-address`. En raison des différentes manières de faire fonctionner OpenTelemetry, consultez la documentation du [collector](https://opentelemetry.io/docs/collector/getting-started/) pour en savoir plus.

> [!NOTE]
> Un surcroît de charge ressource existe, comme pour tout signal d'observabilité ; selon nos mesures initiales, cette surcharge pourrait s'élever entre 2 % et 4 % de la charge CPU.

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /docs/etcd/op-guide/grafana.json
