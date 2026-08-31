# Números de la revista

Un directorio por artículo, dentro de su número:

```
numeros/VOL6_NO2/
  VOL6_NO2_ART1_PRIMERAPALABRA/
    PRIMERAPALABRA.tex                    ← fuente, parte de taller/ejemplo_editorial.tex
    PRIMERAPALABRA_APM_VOL6_NO2_2026.pdf  ← camera-ready linearizado, < 600 KB
    reporte_tecnico.md                    ← el diagnóstico que lo respaldó
```

El flujo por artículo: `bash taller/componer.sh numeros/VOL6_NO2/.../ART.tex`,
sondas en verde, reporte archivado junto al PDF, y su asiento en
`REGISTRO_DE_PRODUCCION.md`. Volúmenes: 2025=Vol.5 · 2026=Vol.6 · 2027=Vol.7,
cuatrimestral (tres números por volumen).
