# MRNT Class

App de una sola página (`index.html`, React sin build) publicada en GitHub Pages.

## Flujo de trabajo
- Después de subir la rama, **siempre** fusionar en `main` (merge `--no-ff`) y hacer push de `main`.

## Presentaciones del repaso
- Se agregan en el array `PRESENTATIONS` de `index.html` (usar `folder` para la carpeta, p. ej. `'3T 2026'`).
- Las referencias bíblicas clicables van en el array `verses` de cada slide.

## Versículos (Biblia)
- El texto de los versículos que se abren en la app vive en `BIBLE_VERSES` (`index.html`).
  **No se escribe a mano ni se busca en internet/Drive**: se genera con
  `python3 tools/biblia.py actualizar` después de agregar o cambiar referencias.
- Fuente: Biblia NVI en texto plano en `biblia/biblia.txt` (o la ruta en `BIBLIA_TXT`).
  Si no está, sacarla del repo **privado** `tomascanalesp/mrnt-biblia` (agregarlo a la
  sesión con `add_repo` y clonarlo en `biblia/`, que tiene el archivo `biblia.txt`).
  No usar Drive ni internet para los textos.
  Esa carpeta está en `.gitignore`: la NVI tiene derechos de autor y el repo es público,
  así que el texto completo **nunca** se sube a este repositorio.
- Consultar un pasaje: `python3 tools/biblia.py "Juan 3:16"`.
