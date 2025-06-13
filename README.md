# Twitch Announcer 📢

¿Cansado de perderte los directos de tus streamers favoritos? ¡Se acabó!

Esta pequeña aplicación para tu PC te avisa justo cuando empiezan, para que no te pierdas ni un segundo de la acción.

---

## Guía rápida de uso

-   **Añadir un canal:** Escribe el nombre en la caja de texto y pulsa **"Añadir Canal"**.
-   **Eliminar un canal:** Haz clic en un canal de la lista y luego pulsa **"Eliminar Seleccionado"**.
-   **Ajustar el tiempo:** Mueve la barrita de abajo para decidir cada cuánto tiempo quieres que la app revise si hay nuevos directos (entre 30 segundos y 5 minutos).
-   **Que se inicie sola:** Marca la casilla **"Iniciar con Windows"** y la aplicación se abrirá automáticamente cada vez que enciendas el ordenador.

---

## ¿Cómo la instalo?

Fácil, ¡no se instala!

1.  Ve a la sección de **[Releases](https://github.com/Rodri2007x/Twitch-Announcer/releases)** (la encontrarás a la derecha, en esta misma página).
2.  Descarga el archivo que se llama `TwitchAnnouncer.exe`.
3.  Guárdalo donde quieras (en el Escritorio, en una carpeta...) y haz doble clic para abrirlo. ¡Listo!

---

## ¿Cómo funciona por dentro? (Para los más curiosos 🤓)

Te estarás preguntando... ¿cómo sabe la aplicación si un canal está en directo? ¿Usa magia?

Casi, pero no. El proceso es bastante ingenioso y sencillo:

1.  **Visita la página:** Cada cierto tiempo (el que tú elijas con la barrita), el programa visita la página de Twitch de cada canal que has añadido (como si lo hicieras tú en tu navegador, pero de forma invisible).
2.  **Lee el código fuente:** Una vez en la página, lee su código HTML. No te asustes, no es tan complicado como suena.
3.  **Busca una pista clave:** Dentro de todo ese código, busca una frase muy específica: `"isLiveBroadcast":true`. Esta es la señal que Twitch deja en su página para indicar que ese canal está emitiendo en directo.
4.  **¡Bingo!**
    *   Si encuentra esa frase, significa que el canal está **Online**, y te lanza la notificación.
    *   Si no la encuentra, significa que está **Offline**, y sigue esperando tranquilamente hasta la próxima comprobación.

Y ya está. Sin necesidad de contraseñas, ni de registrar la aplicación en Twitch, ni nada complicado. ¡Simple y efectivo!
