# Preferencias del editor (Dr. José Carlos Medina-Rodríguez)

Aprendidas durante 8+ sesiones iterativas de producción.

1. **Idioma de feedback:** Español. Comunicación tersa, directa, frecuentemente en MAYÚSCULAS para correcciones puntuales — no lo interpretes como molestia, es su estilo de marcar cambios exactos.
2. **Borgoña oscuro** (#8B1A2B) preferido sobre rojo brillante (#C41E3A). Si alguna vez pide "más rojo" o "más vivo", confirma antes de mover el valor — el histórico de la paleta muestra que esto ya se probó y se descartó por accesibilidad.
3. **Sin íconos** en metadata (removidos todos los FontAwesome del header).
4. **Títulos en español** con Title Case APA 7.ª (no UPPERCASE completo para el título principal).
5. **Headings H1** sí en UPPERCASE — esta es la excepción a la regla anterior, no confundir.
6. **"No Comercial"** con espacio (nunca "NoComercial").
7. **Iterativo:** trabaja con renders visuales (PNG a 400+ DPI), pide ajustes milimétricos ("baja 2pt", "alinea a 0.05pt de diferencia"). Tenlo listo para pedir mediciones exactas, no aproximaciones.
8. **Espera ejecución completa** — no hand-holding. Confirma el plan una vez y ejecútalo de punta a punta; no te detengas a pedir confirmación en cada micro-paso salvo que sea una decisión de spec (cambiar color, cambiar geometría), no de ejecución.
9. **Diagnóstico siempre** después de cada cambio — no entregues un PDF "a ojo", corre el diagnóstico de 14 capas.
10. **Nomenclatura de archivos:** `PRIMERAPALABRA_APM_VOL#_NO#_AÑO`, sin excepciones.

## Contexto histórico (útil para entender el "por qué" de varias reglas)

El sistema se construyó en 8+ sesiones:

1. **Migración reportlab → pdfLaTeX** (sesiones 1–3): reportlab no pudo manejar la complejidad tipográfica requerida (microtype, control de viudas/huérfanas, hanging indent real). Migración completa a pdfLaTeX.
2. **Creación de `apm-editorial.cls`** (sesiones 3–5): separación de layout (clase) y contenido (`.tex`). Documentación de los primeros ~24 failure modes.
3. **Refinamiento de header P1** (sesiones 5–7): iteraciones sobre logo, DOI, metadata, caja de resumen, headings, alineación de columnas. Aquí se descartó la paleta Rojo #C41E3A a favor de Borgoña #8B1A2B, y se eliminó el Folio visible y los íconos.
4. **Producción del primer artículo** (sesión 8): editorial de neuromodulación completada como VOL5_NO2_ART1. Diagnóstico final 39/39 puntos verificados (100%) bajo el esquema de esa sesión.
5. **Consolidación en skill** (sesión actual): compilación del conocimiento disperso en un paquete reutilizable, con las specs contradictorias resueltas a favor del código real.

### Artículos producidos con el sistema

| Artículo | Vol/No | Estado |
|---|---|---|
| Neuromodulación en psiquiatría (Editorial) | Vol. 5, No. 2 | ✓ Completo, usa `apm-editorial.cls`, es el ejemplo canónico (`assets/ejemplo_editorial.tex`) |
| Salud Mental Digital (Editorial) | Vol. 6, No. 1 | Usa `apm-editorial.cls`, standalone — no confirmado si pasó el diagnóstico completo con la versión actual del `.cls` |
| Suicidio Jalisco (Artículo original) | Vol. 5, No. 1 | Standalone, NO usa `apm-editorial.cls` — necesita migración completa (ver `09_limitaciones_conocidas.md`) |
