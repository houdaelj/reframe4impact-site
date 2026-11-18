# Site ReFrame 4Impact

Site vitrine de ReFrame 4Impact (conseil ESG et durabilité, Maroc – France), en français et en anglais.
L'Académie 4Impact reste un site séparé : https://academie-reframe4impact.netlify.app/

## Structure

- `public/` : le site publié par Netlify (HTML statique, aucune compilation).
  - `/fr/` et `/en/` : une adresse par page (accueil, expertises/services, méthode/approach, académie/academy, contact, mentions légales, confidentialité).
  - `/` redirige vers `/fr/` ou `/en/` selon la langue du navigateur (voir `netlify.toml`).
- `tools/` : la source et le générateur.
  - `maquette.html` : maquette FR/EN, source unique des textes et du style.
  - `build.sh` : régénère `public/` (nécessite Python 3 et `beautifulsoup4`, `lxml`).

## Formulaire de contact

Le formulaire « contact » utilise Netlify Forms. Les messages arrivent dans Netlify > Forms ; activer une notification email vers contact@reframe4impact.com.

## À compléter

- Mentions légales : forme juridique, adresse du siège, numéro RC.
