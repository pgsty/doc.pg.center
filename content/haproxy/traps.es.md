---
title: "11. Trampas conocidas que conviene evitar"
linkTitle: "11. Trampas comunes"
weight: 350
description: "Errores operativos y comportamientos sorprendentes que conviene evitar"
icon: fa-solid fa-triangle-exclamation
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/traps/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 11"
---

De vez en cuando, alguien reporta que, tras reiniciar el sistema, el servicio haproxy no se inició, y
que en cuanto lo inicia manualmente, funciona. La mayoría de las veces, estas personas ejecutan un
mecanismo de dirección IP en clúster, como keepalived, para asignar la dirección IP del servicio
únicamente al nodo maestro, y aunque antes funcionaba cuando enlazaban haproxy a la dirección
0.0.0.0, dejó de funcionar después de enlazarlo a la dirección IP virtual. Lo que ocurre aquí es
que, cuando el servicio se inicia, la dirección IP virtual todavía no pertenece al nodo local, de
modo que cuando HAProxy quiere enlazarse a ella, el sistema lo rechaza porque no es una dirección IP
local. La solución no consiste en retrasar el arranque del servicio haproxy (ya que no resistiría un
reinicio), sino en configurar correctamente el sistema para permitir el enlace a direcciones no
locales. Esto se hace fácilmente en Linux estableciendo el sysctl net.ipv4.ip_nonlocal_bind a 1.
Esto también es necesario para interceptar de forma transparente el tráfico IP que atraviesa HAProxy
con destino a una dirección específica.

Las configuraciones multiproceso que implican rangos de puertos de origen pueden aparentar funcionar,
pero provocarán fallos aleatorios bajo cargas elevadas, porque más de un proceso podría intentar usar
el mismo puerto de origen para conectarse al mismo servidor, lo cual no es posible. El sistema
informará de un error y se hará un nuevo intento, eligiendo otro puerto. Un valor alto del parámetro
«retries» puede ocultar el efecto hasta cierto punto, pero esto también conlleva un mayor uso de CPU
y tiempo de procesamiento. Los registros también informarán de un cierto número de reintentos. Por
esta razón, los rangos de puertos deberían evitarse en configuraciones multiproceso.

Dado que HAProxy usa SO_REUSEPORT y admite tener múltiples procesos independientes enlazados a la
misma IP:puerto, durante la resolución de problemas puede ocurrir que un proceso antiguo no se haya
detenido antes de iniciar uno nuevo. Esto produce resultados de prueba absurdos que tienden a
indicar que cualquier cambio en la configuración se ignora. La razón es que, de hecho, aunque el
proceso nuevo se reinicie con una configuración nueva, el antiguo también recibe algunas conexiones
entrantes y las procesa, devolviendo resultados inesperados. En caso de duda, simplemente detén el
proceso nuevo e inténtalo de nuevo. Si sigue funcionando, muy probablemente significa que queda un
proceso antiguo vivo y que debe detenerse. El «netstat -lntp» de Linux es de gran ayuda aquí.

Al añadir entradas a una ACL desde la línea de comandos (por ejemplo, al añadir una dirección de
origen a una lista negra), es importante tener en cuenta que estas entradas no se sincronizan con el
archivo y que, si alguien recarga la configuración, estas actualizaciones se perderán. Aunque a
menudo este es el efecto deseado (para las listas negras), puede no coincidir necesariamente con lo
esperado cuando el cambio se hizo como solución a un problema. Consulta la acción «add acl» de la
interfaz CLI.
