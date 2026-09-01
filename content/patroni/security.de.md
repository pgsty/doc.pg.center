---
title: "Sicherheitshinweise"
weight: 160
icon: fa-solid fa-lock
description: "Sicherheitshinweise für DCS, REST API und Kennwortspeicherung."
module: [PATRONI]
categories: [Konzept]
aliases: [/docs/patroni/security/]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Ein Patroni-Cluster verfügt über zwei Schnittstellen, die vor unbefugtem Zugriff geschützt werden müssen: das verteilte Konfigurationsspeicher (DCS) und die Patroni REST-API.

--------

## Schutz des DCS {#protecting-dcs}
Sowohl Patroni als auch [patronictl](/de/patroni/patronictl#patronictl) speichern und abrufen Daten von/zum DCS.

Obwohl der DCS keine sensiblen Informationen enthält, ermöglicht er die Änderung einiger Konfigurationen von Patroni/Postgres. Daher sollte der DCS selbst daher als erstes geschützt werden.

Die Details zum Schutz hängen vom verwendeten Typ des DCS ab. Die Authentifizierungs- und Verschlüsselungsparameter (Token/Basic-Auth/Client-Zertifikate) für die unterstützten DCS-Typen sind in den [Einstellungen](/de/patroni/config/yaml#yaml) beschrieben.

Die allgemeine Empfehlung ist, TLS für alle DCS-Kommunikationen zu aktivieren.

--------

## Schutz der REST-API {#protecting-the-rest-api}
Der Schutz der REST-API ist eine komplexere Aufgabe.

Die Patroni-REST-API wird von Patroni selbst während des Leader-Wettbewerbs verwendet, von dem Tool [patronictl](/de/patroni/patronictl#patronictl) zur Durchführung von Failover, Switchover, Reinitialisierung, Neustart oder Neuladung, von HAProxy oder einem anderen Load-Balancer zur Durchführung von HTTP-Health Checks und natürlich auch für Monitoring verwendet.

Aus Sicherheitsperspektive enthält die REST-API sichere (`GET` Anfragen, nur Informationen abrufen) und unsichere (`PUT`, `POST`, `PATCH` und `DELETE` Anfragen, Zustandsänderungen an Knoten vornehmen) Endpunkte.

Die unsicheren Endpunkte können durch HTTP-Basic-Auth geschützt werden, indem die Parameter `restapi.authentication.username` und `restapi.authentication.password` gesetzt werden. Es gibt keine Möglichkeit, die sicheren Endpunkte zu schützen, ohne TLS zu aktivieren.

Wenn TLS für die REST-API aktiviert und ein PKI eingerichtet ist, ist eine gegenseitige Authentifizierung zwischen API-Server und API-Client für alle Endpunkte möglich.

Die Parameter im Abschnitt `restapi` ermöglichen die TLS-Client-Authentifizierung beim Server. Je nach Wert des Parameters `verify_client` erfordert der API-Server eine erfolgreiche Überprüfung des Clientzertifikats für sowohl sichere als auch unsichere API-Aufrufe (`verify_client: required`), nur für unsichere API-Aufrufe (`verify_client: optional`), oder für keine API-Aufrufe (`verify_client: none`).

Die Parameter im Abschnitt `ctl` ermöglichen die TLS-Server-Authentifizierung beim Client (dem Tool [patronictl](/de/patroni/patronictl#patronictl), das dieselbe Konfiguration wie Patroni verwendet). Setzen Sie `insecure: true`, um die Überprüfung des Serverzertifikats durch den Client zu deaktivieren. Weitere Details zu den TLS-Client-Parametern finden Sie in [settings](/de/patroni/config/yaml#patronictl_settings).

Den Schutz der PostgreSQL-Datenbank vor unbefugtem Zugriff liegt außerhalb des Umfangs dieses Dokuments und wird in <https://www.postgresql.org/docs/current/client-authentication.html> behandelt.
