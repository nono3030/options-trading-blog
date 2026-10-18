# Options & Volatilité : blog SEO en pilote automatique

Blog statique en français sur le trading d'options, hébergé sur GitHub Pages.
Chaque jour, un workflow GitHub Actions :

1. **récupère les données Google Search Console** (requêtes, pages, clics, impressions, CTR, position) et soumet le sitemap ;
2. **calcule la stratégie** (`scripts/strategy.py`) :
   - *nouveaux articles* : requêtes avec beaucoup d'impressions où l'on est mal classé (position > 8) et qu'aucun article ne cible encore ; sinon le backlog de mots-clés (`data/keywords.yaml`), enrichi automatiquement par Claude (avec recherche web) quand il se vide ;
   - *articles à améliorer* : pages en « striking distance » (positions 4 à 25) ou dont le CTR est inférieur à l'attendu pour leur position ;
3. **écrit un nouvel article** avec Claude + recherche web (analyse des pages concurrentes, faits vérifiés, sources citées, FAQ, liens internes) ;
4. **réécrit un article sous-performant** à partir des requêtes réelles pour lesquelles il apparaît (titre et meta pour le CTR, nouvelles sections pour les requêtes mal couvertes) ;
5. **mesure l'impact** de chaque réécriture environ 30 jours après (clics avant/après) et réinjecte ces enseignements dans les prompts suivants : c'est la boucle d'auto-amélioration ;
6. commit le contenu, reconstruit le site et le déploie.

SEO technique inclus : URLs propres, balise canonical, Open Graph, JSON-LD (`BlogPosting`, `BreadcrumbList`, `FAQPage`), sitemap avec `lastmod`, RSS, robots.txt, sommaire, articles liés, page auteur (E-E-A-T) et avertissement sur les risques.

## Mise en route

### 1. GitHub Pages
*Settings → Pages → Source : **GitHub Actions***.

### 2. Secrets et variables (*Settings → Secrets and variables → Actions*)

| Type | Nom | Valeur |
|---|---|---|
| Secret | `ANTHROPIC_API_KEY` | clé API Anthropic |
| Secret | `GSC_SERVICE_ACCOUNT_JSON` | contenu JSON de la clé du compte de service Google (étape 3) |
| Variable | `SITE_URL` | `https://nono3030.github.io/options-trading-blog` (ou votre domaine) |
| Variable | `GSC_PROPERTY` | `https://nono3030.github.io/options-trading-blog/` (ou `sc-domain:mondomaine.fr`) |
| Variable | `GSC_VERIFICATION` | le code de la balise meta de vérification Search Console |

### 3. Google Search Console
1. Dans [Search Console](https://search.google.com/search-console), ajoutez une propriété **préfixe d'URL** avec l'URL du site, méthode **balise HTML** : copiez le `content="…"` dans la variable `GSC_VERIFICATION`, relancez le workflow (*Run workflow*, case « Déployer seulement »), puis cliquez sur *Valider*.
2. Dans [Google Cloud Console](https://console.cloud.google.com/) : créez un projet, activez l'**API Google Search Console**, créez un **compte de service**, puis générez une clé JSON et collez son contenu dans le secret `GSC_SERVICE_ACCOUNT_JSON`.
3. Dans Search Console, *Paramètres → Utilisateurs et autorisations → Ajouter* : l'adresse e-mail du compte de service, avec l'autorisation **Propriétaire** (nécessaire pour soumettre le sitemap).

Tant que la GSC n'est pas configurée ou n'a pas encore de données (comptez 2 à 4 semaines), le pipeline publie à partir du backlog de mots-clés.

### 4. Lancer
*Actions → SEO autopilot & deploy → Run workflow*. Ensuite, il tourne seul tous les jours à 05:17 UTC.

## Réglages
`config.yaml` : nombre d'articles et de réécritures par jour, seuils d'impressions, délai entre deux réécritures, modèle et niveau d'effort.

## En local
```bash
pip install -r requirements.txt
python scripts/build.py              # génère dist/
python -m http.server -d dist 8000
```

## Points de vigilance
- **Qualité avant volume.** Google pénalise le contenu produit en masse sans valeur ajoutée (*scaled content abuse*), et la finance est un sujet YMYL. Le pipeline est réglé sur 1 article par jour, avec recherche web, sources et validation. Relisez régulièrement les articles, surtout ceux qui parlent de fiscalité.
- **Coût API** : environ 1 article plus 1 réécriture par jour avec recherche web. Suivez votre consommation dans la console Anthropic.
- **Domaine personnalisé** : recommandé pour le SEO à long terme. Ajoutez-le dans *Settings → Pages*, puis mettez à jour `SITE_URL` et `GSC_PROPERTY`.
