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

## Tracking des visiteurs

Tout le suivi est **soumis au consentement** (RGPD / CNIL) : rien n'est chargé avant le clic sur « Accepter », le bouton « Refuser » est aussi visible que « Accepter », le choix est redemandé tous les 6 mois, et un lien « Gérer les cookies » permet de changer d'avis (les cookies sont alors effacés). Sans identifiant configuré, aucun bandeau ni script n'est ajouté.

| Outil | Ce qu'on apprend |
|---|---|
| **Google Analytics 4** | utilisateurs, nouveaux / récurrents, pays, ville, appareil, navigateur, canaux et sources de trafic, pages d'entrée, temps engagé |
| **Événements sur mesure** (`static/analytics.js`) | profondeur de défilement (25/50/75/100 %), temps de lecture *actif*, article réellement lu (`article_read`), clics sur les liens internes avec leur zone (sommaire, corps, articles liés…), clics sortants, questions de la FAQ ouvertes, texte copié ; chaque événement porte l'article et son mot-clé |
| **Microsoft Clarity** | cartes de chaleur, cartes de défilement, relecture des sessions, détection des clics de frustration |
| **Search Console** | requêtes Google, impressions, positions, CTR |

**Rapport** : chaque jour, `data/reports/latest.md` (audience, acquisition, requêtes, contenus les plus lus, contenus qui retiennent mal, questions FAQ populaires) est mis à jour dans le dépôt.

**Boucle d'amélioration** : les articles qui ont du trafic mais un faible temps de lecture ou un faible taux de lecture sont automatiquement mis en file de réécriture, et Claude reçoit ces métriques pour corriger l'article.

### Configuration
1. Créez une propriété **GA4** ([analytics.google.com](https://analytics.google.com)) avec un flux Web pour l'URL du site. Désactivez « Signaux Google » et le partage de données publicitaires.
   - Variable `GA4_MEASUREMENT_ID` : l'ID du flux (`G-XXXXXXX`).
   - Variable `GA4_PROPERTY_ID` : l'ID numérique de la propriété (*Admin → Détails de la propriété*).
   - Dans *Admin → Gestion des accès à la propriété*, ajoutez l'e-mail du compte de service (le même que pour Search Console) avec le rôle **Éditeur**, puis activez l'**API Google Analytics Data** et l'**API Google Analytics Admin** dans Google Cloud.
   - Lancez une fois le workflow **GA4 setup** : il crée les dimensions personnalisées (article, mot-clé, question FAQ, zone de lien…).
   - Dans *Admin → Conservation des données*, réglez la durée sur 14 mois.
2. Créez un projet **Microsoft Clarity** ([clarity.microsoft.com](https://clarity.microsoft.com)) et renseignez la variable `CLARITY_PROJECT_ID`. Dans ses paramètres, activez « Cookies » et laissez le masquage sur « Équilibré » ou « Strict ».

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
- **Domaine personnalisé** : voir ci-dessous.

## Domaine personnalisé
1. Chez votre registrar, créez les enregistrements DNS :
   - domaine nu (`mondomaine.fr`) : 4 enregistrements **A** vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (et les **AAAA** `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`) ;
   - `www` : un **CNAME** vers `nono3030.github.io`.
2. Recommandé : sur GitHub, *Settings du compte → Pages → Add a domain* pour **vérifier** le domaine (protection contre le détournement).
3. Dans le dépôt, *Settings → Pages → Custom domain* : saisissez `mondomaine.fr`, attendez la validation DNS, puis cochez **Enforce HTTPS**.
4. Variable `SITE_URL` = `https://mondomaine.fr` (le build génère alors le fichier `CNAME`, les URL canoniques, le sitemap et les liens sans le préfixe `/options-trading-blog`).
5. Search Console : utilisez une propriété **Domaine** (`GSC_PROPERTY` = `sc-domain:mondomaine.fr`), vérifiée par un enregistrement DNS TXT ; plus besoin de `GSC_VERIFICATION`. Dans GA4, mettez à jour l'URL du flux Web.
