---
title: "Sicherheitshinweise"
weight: 160
icon: fa-solid fa-lock
description: "Sicherheitshinweise für DCS, REST-API und den Umgang mit Zugangsdaten."
module: [PATRONI]
categories: [Konzept]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Ein Patroni-Cluster verfügt über zwei Schnittstellen, die vor unbefugtem Zugriff geschützt werden müssen: der verteilte Konfigurationsspeicher (DCS) und die REST-API von Patroni.

--------

## Schutz des DCS {#protecting-dcs}
Sowohl Patroni als auch [patronictl](/de/patroni/patronictl#patronictl) speichern Daten im DCS und lesen sie daraus.

Auch wenn der DCS keine sensiblen Informationen enthält, ermöglicht er die Änderung einiger Einstellungen von Patroni/Postgres. Daher sollte zuerst der DCS selbst geschützt werden.

Die Details zum Schutz hängen vom verwendeten Typ des DCS ab. Die Authentifizierungs- und Verschlüsselungsparameter (Token/Basic-Auth/Client-Zertifikate) für die unterstützten DCS-Typen sind in den [Einstellungen](/de/patroni/config/yaml#yaml) beschrieben.

Die allgemeine Empfehlung ist, TLS für die gesamte Kommunikation mit dem DCS zu aktivieren.

--------

## Schutz der REST-API {#protecting-the-rest-api}
Der Schutz der REST-API ist eine komplexere Aufgabe.

Patroni selbst verwendet seine REST-API während der Leader-Wahl. Das Werkzeug [patronictl](/de/patroni/patronictl#patronictl) nutzt sie für Failover, Switchover, Neuinitialisierungen, Neustarts und das Neuladen der Konfiguration. HAProxy oder andere Load-Balancer verwenden sie für HTTP-Health-Checks; außerdem kann sie zur Überwachung dienen.

Aus Sicherheitsperspektive enthält die REST-API sichere (`GET`-Anfragen, die nur Informationen abrufen) und unsichere (`PUT`-, `POST`-, `PATCH`- und `DELETE`-Anfragen, die den Zustand von Knoten ändern) Endpunkte.

Die unsicheren Endpunkte können durch HTTP-Basic-Auth geschützt werden, indem die Parameter `restapi.authentication.username` und `restapi.authentication.password` gesetzt werden. Es gibt keine Möglichkeit, die sicheren Endpunkte zu schützen, ohne TLS zu aktivieren.

Wenn TLS für die REST-API aktiviert und eine PKI eingerichtet ist, ist eine gegenseitige Authentifizierung zwischen API-Server und API-Client für alle Endpunkte möglich.

Die Parameter im Abschnitt `restapi` ermöglichen die TLS-Client-Authentifizierung beim Server. Je nach Wert des Parameters `verify_client` erfordert der API-Server eine erfolgreiche Überprüfung des Clientzertifikats sowohl für sichere als auch für unsichere API-Aufrufe (`verify_client: required`), nur für unsichere API-Aufrufe (`verify_client: optional`), oder für keine API-Aufrufe (`verify_client: none`).

Die Parameter im Abschnitt `ctl` ermöglichen die TLS-Server-Authentifizierung beim Client (dem Werkzeug [patronictl](/de/patroni/patronictl#patronictl), das dieselbe Konfiguration wie Patroni verwendet). Mit `insecure: true` wird die Überprüfung des Serverzertifikats durch den Client deaktiviert. Weitere Details zu den TLS-Client-Parametern finden Sie in [Einstellungen](/de/patroni/config/yaml#patronictl_settings).

Der Schutz der PostgreSQL-Datenbank selbst vor unbefugtem Zugriff liegt außerhalb des Umfangs dieses Dokuments und wird unter <https://www.postgresql.org/docs/current/client-authentication.html> behandelt.
