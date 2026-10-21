---
title: 'Grecques des options : delta, gamma, theta, vega expliqués'
description: 'Grecques des options (delta, gamma, theta, vega) : ce qu''elles mesurent, comment les lire et les utiliser, avec exemples chiffrés sur un call et un spread.'
keyword: grecques des options delta gamma theta vega
slug: grecques-des-options-delta-gamma-theta-vega
date: '2026-10-21'
updated: '2026-10-21'
tags:
- options
- grecques
- gestion du risque
faq:
- q: Quelle est la grecque la plus importante pour un débutant ?
  a: 'Le delta, parce qu''il indique votre exposition directionnelle : combien vous gagnez ou perdez pour 1 $ de mouvement du sous-jacent. Juste après vient le theta si vous achetez des options, car le temps joue contre vous chaque jour. Le gamma et le vega deviennent essentiels dès que vous vendez de la prime ou que vous gardez des positions près de l''échéance.'
- q: Le delta est-il la probabilité qu'une option finisse dans la monnaie ?
  a: C'est seulement une approximation. Dans le modèle de Black-Scholes, la probabilité « risque-neutre » de finir dans la monnaie est N(d2), légèrement différente du delta N(d1). Dans notre exemple, un call à 30 jours a un delta de 0,41 pour une probabilité modèle de 0,39. C'est utile comme ordre de grandeur, pas comme une vraie prévision.
- q: Pourquoi mon call perd-il de la valeur alors que l'action ne baisse pas ?
  a: 'Deux causes reviennent presque toujours : le theta (la perte de valeur temps, chaque jour) et la baisse de la volatilité implicite (vega), souvent juste après une publication de résultats. Un call à la monnaie peut perdre plus de 15 % de sa valeur en une séance si la volatilité implicite passe de 18 % à 15 %, même si le cours ne bouge pas.'
- q: Les grecques affichées par mon courtier sont-elles par contrat ou par action ?
  a: 'Dans une chaîne d''options, elles sont en général affichées par action (par unité de sous-jacent). Sur les options d''actions et d''ETF US comme SPY ou QQQ, il faut multiplier par 100 (le multiplicateur standard) puis par le nombre de contrats. Les vues portefeuille affichent souvent des valeurs agrégées : vérifiez la convention de votre plateforme.'
- q: Une position delta neutre est-elle sans risque ?
  a: Non. Être delta neutre veut dire ne pas avoir d'exposition aux petits mouvements à un instant donné. Si la position a du gamma, le delta réapparaît dès que le marché bouge. Elle reste aussi exposée au vega et au theta.
---

Les grecques des options (delta, gamma, theta, vega, plus le rho) mesurent la sensibilité du prix d'une option à chacun de ses moteurs : le cours du sous-jacent, la vitesse à laquelle ce cours change, le temps qui passe et la volatilité implicite. En pratique, le **delta** indique combien vous gagnez ou perdez pour 1 $ de mouvement, le **gamma** de combien ce delta change, le **theta** combien vous coûte (ou vous rapporte) chaque jour, et le **vega** l'effet d'un point de volatilité implicite. Ce sont des estimations locales issues d'un modèle, pas des promesses : les grecques ne garantissent pas la variation exacte de la prime, elles servent de repère théorique.

La suite est construite comme je les utilise vraiment : d'abord les conventions (c'est là que la plupart des erreurs se produisent), puis chaque grecque, et enfin deux exemples complets, sur un call acheté et sur un put credit spread.

## Les grecques en un coup d'œil

| Grecque | Ce qu'elle mesure | Unité usuelle | Call acheté | Put acheté | Vendeur d'option |
|---|---|---|---|---|---|
| **Delta (Δ)** | Variation du prix de l'option pour +1 $ sur le sous-jacent | entre −1 et +1 par action | Positif (0 à 1) | Négatif (−1 à 0) | Signe inversé |
| **Gamma (Γ)** | Variation du delta pour +1 $ sur le sous-jacent | par action | Positif | Positif | Négatif |
| **Theta (Θ)** | Variation du prix pour un jour qui passe | $ par jour | Négatif | Négatif (presque toujours) | Positif |
| **Vega** | Variation du prix pour +1 point de volatilité implicite | $ par point de VI | Positif | Positif | Négatif |
| **Rho (ρ)** | Variation du prix pour +1 point de taux d'intérêt | $ par point de taux | Positif | Négatif | Signe inversé |

Petite anecdote : le vega n'est pas une lettre grecque, mais le nom est resté parce qu'il colle à la convention.

Si les notions de call, de put, de strike ou de prime ne sont pas encore claires pour vous, commencez par [la définition d'une option call avec exemples](/qu-est-ce-qu-une-option-call/) et [l'explication simple de l'option put](/option-put-explication-simple/). Les grecques ne sont utiles qu'une fois ces bases acquises.

## Les conventions à vérifier avant de lire un chiffre

Une grecque sans unité ne veut rien dire. Voici ce que je vérifie systématiquement :

- **Par action ou par contrat.** Dans une chaîne d'options, un delta de 0,54 s'entend par action. Sur SPY, QQQ ou une action US, le contrat standard porte sur 100 actions, donc 0,54 de delta représente environ 54 $ de gain ou de perte par contrat pour 1 $ de mouvement. Sur l'indice SPX, le multiplicateur est aussi de 100, mais l'indice cote environ dix fois plus cher que SPY : un contrat SPX représente donc une exposition nominale environ dix fois plus grosse.
- **Theta par jour calendaire ou par jour de bourse.** Les modèles ne traitent pas tous les week-ends de la même façon. Sur un horizon de quelques jours, l'écart se voit.
- **Vega par point de volatilité.** Un vega de 0,68 signifie +0,68 $ par action si la volatilité implicite passe, par exemple, de 18 % à 19 %.
- **Le modèle.** Toutes les grecques sont calculées à partir d'un modèle et d'une volatilité implicite. Deux plateformes peuvent afficher des valeurs légèrement différentes.

**Hypothèses de tous les exemples ci-dessous :** j'ai calculé les chiffres moi-même avec le modèle de Black-Scholes. Le sous-jacent est un ETF hypothétique (type SPY) coté 600 $, sans dividende, avec un taux sans risque de 4 % et une volatilité identique pour tous les strikes. Sur le vrai marché, les puts hors de la monnaie ont généralement une volatilité implicite plus élevée (le « skew »). Prenez ces chiffres comme des ordres de grandeur pédagogiques, pas comme des cotations réelles.

## Delta : votre exposition directionnelle

Le delta répond à la première question à se poser sur une position : « si le marché monte de 1 $, combien je gagne ou je perds ? »

- Un call à la monnaie a un delta proche de 0,50. Il monte vers 1 quand le call s'enfonce dans la monnaie et tend vers 0 quand il s'en éloigne.
- Un put a un delta négatif, entre 0 et −1.
- Le delta d'une position s'additionne : 3 calls à 0,40 de delta, c'est +120 « deltas », soit à peu près la même exposition à court terme que 120 actions.

**Delta et probabilité.** On lit souvent que le delta donne la probabilité de finir dans la monnaie. C'est une approximation utile, rien de plus. Dans notre modèle, le call de strike 610 à 30 jours a un delta de 0,41 pour une probabilité modèle (N(d2)) de 0,39. Et ces probabilités sont « risque-neutres » : elles viennent des prix du marché, ce ne sont pas des prévisions.

Ce que je surveille en pratique, c'est le **delta net du portefeuille**, pas celui de chaque option. Une vente de put à delta −0,20 vous donne un delta positif de +20 par contrat. Cinq de ces ventes sur des sous-jacents très corrélés (SPY, QQQ, grandes valeurs tech), c'est un pari directionnel haussier concentré, même si chaque position semble « loin ».

## Gamma : l'accélérateur du delta

Le gamma mesure de combien le delta change pour 1 $ de mouvement. Un call de delta 0,536 et de gamma 0,0128 aura un delta d'environ 0,549 si le sous-jacent monte de 1 $, et d'environ 0,60 après +5 $.

Trois choses à retenir :

1. **Acheteur = gamma positif.** Votre delta augmente quand le marché va dans votre sens et diminue quand il va contre vous. C'est un avantage, que vous payez par le theta.
2. **Vendeur = gamma négatif.** C'est l'inverse : votre exposition grossit quand le marché va contre vous. C'est le vrai risque de la vente de prime.
3. **Le gamma est le plus élevé à la monnaie et près de l'échéance.** C'est tout le sujet des options 0DTE et des échéances quotidiennes sur SPX : un petit mouvement peut faire basculer le delta très vite.

| Call 600 à la monnaie (VI 18 %) | 30 jours | 7 jours | 1 jour |
|---|---|---|---|
| Prix | 13,34 $ | 6,20 $ | 2,29 $ |
| Delta | 0,536 | 0,517 | 0,507 |
| Gamma | 0,0128 | 0,0266 | 0,0706 |
| Theta (par jour) | −0,24 $ | −0,46 $ | −1,16 $ |
| Vega (par point de VI) | 0,68 $ | 0,33 $ | 0,13 $ |

Le gamma est multiplié par plus de 5 entre 30 jours et 1 jour. Le theta suit le même chemin. C'est le compromis central des options : **le theta est le prix du gamma**. Celui qui encaisse le theta porte le risque de gamma, et inversement.

## Theta : le coût (ou le revenu) du temps

Le theta estime la valeur perdue par l'option en un jour, toutes choses égales par ailleurs. Sur notre call à 30 jours, −0,24 $ par action, cela fait environ 24 $ par contrat et par jour.

Ce qui compte en pratique :

- **La perte de valeur n'est pas linéaire.** Elle accélère à l'approche de l'échéance, surtout pour les options à la monnaie (voir le tableau ci-dessus).
- **Les options loin de la monnaie** ont un theta faible en dollars, mais élevé par rapport à leur prix.
- **Un theta positif n'est pas un revenu garanti.** C'est la contrepartie d'un gamma et d'un vega négatifs. Un vendeur de prime qui ne regarde que son theta oublie la moitié du tableau.

## Vega : la sensibilité à la volatilité implicite

Le vega mesure la variation du prix de l'option pour un point de volatilité implicite (VI). Il est positif pour tout acheteur, call ou put, et plus élevé sur les échéances longues : 0,68 $ à 30 jours contre 0,13 $ à 1 jour dans notre tableau.

C'est la grecque qui surprend le plus les débutants, à cause de **l'écrasement de la volatilité implicite** (le « vol crush ») après un événement attendu : résultats d'entreprise, réunion de la Fed, chiffres d'inflation. Avant l'annonce, la VI monte. Juste après, elle retombe, et la prime avec elle, même si le sous-jacent a bougé.

## Rho : le moins influent… sauf sur le long terme

Le rho mesure l'effet d'un point de taux d'intérêt. Sur notre call à 30 jours, il vaut 0,25 $ : +1 point de taux ajouterait environ 25 $ par contrat. C'est négligeable sur des échéances courtes. Le rho devient plus important sur les LEAPS (échéances à plus d'un an).

## Exemple complet n° 1 : achat d'un call à la monnaie

**Position :** achat d'un call strike 600, échéance 30 jours, sous-jacent à 600 $, VI 18 %.

- Prime : 13,34 $ → **1 334 $ payés** (perte maximale si le call expire sans valeur)
- Point mort à l'échéance : 600 + 13,34 = **613,34 $**
- Gain maximal : théoriquement illimité
- Grecques par contrat : delta +53,6 / gamma +1,28 / theta −23,9 $ par jour / vega +68,3 $ par point de VI

**Scénario A : le sous-jacent monte de 5 $ le lendemain, la VI ne bouge pas.**
Estimation avec les grecques : delta × 5 + ½ × gamma × 5² + theta = 2,68 + 0,16 − 0,24 = **+2,60 $**. Le prix estimé est de 15,94 $, et le modèle recalculé donne exactement 15,94 $. Gain : **+260 $**. Sur un petit mouvement, l'approximation delta-gamma-theta est excellente.

**Scénario B : le sous-jacent ne bouge pas, mais la VI passe de 18 % à 15 % (après une annonce).**
Estimation : −3 × 0,683 = **−2,05 $**, soit un call qui tombe à 11,29 $. Perte : **−205 $ (−15 %) en une séance, sans aucun mouvement de prix**. Et le jour suivant, le theta continue de jouer.

Ce que j'en retiens : acheter une option avant un événement, c'est parier à la fois sur la direction, sur l'ampleur du mouvement et sur la volatilité. Le mouvement doit être assez grand pour compenser la baisse de VI qui suivra.

## Exemple complet n° 2 : put credit spread (risque défini)

C'est la structure que j'utilise le plus. **Position :** vente du put 570 et achat du put 560, échéance 45 jours, sous-jacent à 600 $, VI 22 %.

- Put 570 vendu : 6,14 $ (delta −0,222)
- Put 560 acheté : 4,03 $ (delta −0,160)
- **Crédit net : 2,11 $ → 211 $ encaissés** (gain maximal)
- **Perte maximale : (10 − 2,11) × 100 = 789 $**
- **Point mort à l'échéance : 570 − 2,11 = 567,89 $**
- Grecques nettes par spread : delta +6,2 / gamma −0,12 / theta +2,4 $ par jour / vega −11,5 $ par point de VI

Notez que le theta de départ est modeste (2,40 $ par jour). La perte de valeur temps s'accélère plus tard dans la vie du trade.

| Scénario | Valeur du spread | P&L | Delta net | Ce que ça illustre |
|---|---|---|---|---|
| Départ (J0) | 2,11 $ | 0 $ | +6,2 | Position quasi neutre en apparence |
| J+21, cours stable à 600, VI 22 % | 1,39 $ | **+72 $** | +6,6 | Le theta travaille, lentement |
| J+30, cours stable à 600, VI 22 % | 0,88 $ | **+123 $** | +5,9 | Le theta accélère |
| J+10, cours à 575 (−4,2 %), VI 28 % | 4,18 $ | **−207 $** | +7,8 | Delta + vega : la perte arrive bien avant le strike |
| 2 jours avant l'échéance, cours à 571 | 2,66 $ | −55 $ | +33,7 | Le gamma a multiplié le delta par 5 |
| 2 jours avant l'échéance, cours à 566 | 4,57 $ | **−246 $** | +40,9 | 5 $ de baisse = environ 190 $ de perte de plus |

Deux leçons très concrètes :

1. **Une baisse de 4 % accompagnée d'une hausse de VI coûte déjà l'équivalent du crédit encaissé**, alors que le cours est encore au-dessus du strike vendu. Le vega négatif s'ajoute au delta.
2. **Près de l'échéance, le gamma négatif transforme une position à +6 deltas en une position à +34 deltas.** C'est pour cela que beaucoup de vendeurs de prime, moi compris, ferment ou décalent leurs positions bien avant l'échéance au lieu d'aller chercher les derniers dollars de crédit.

## Comment je lis les grecques d'un portefeuille au quotidien

- **Delta net total**, si possible pondéré par le bêta par rapport au SPX ou à SPY, pour savoir si je suis en réalité long sur le marché.
- **Rapport theta / vega** : un theta confortable avec un vega très négatif signifie qu'un pic de volatilité fera mal.
- **Gamma des positions à moins de 10 jours** : c'est là que le portefeuille peut changer de profil en une séance.
- **Scénarios plutôt que chiffres isolés** : les grecques sont locales. Pour un choc de −5 % avec +8 points de VI, je simule plutôt que d'extrapoler.

Sur Interactive Brokers, le Risk Navigator agrège ces données. Il permet aussi de définir des alertes qui préviennent quand les grecques d'une option atteignent un certain niveau, ce qui peut servir pour décider d'ouvrir ou de clôturer une position selon les valeurs de delta, gamma, vega ou theta. Pour la méthode globale (taille des positions, choix des échéances), voir aussi notre [guide concret du trading d'options pour débutant](/trading-options-debutant/).

## Risques et erreurs fréquentes

- **Oublier le multiplicateur.** Un theta de 0,24 qui paraît négligeable représente 24 $ par jour et par contrat, et 240 $ pour 10 contrats. Sur SPX, l'exposition nominale est environ dix fois celle de SPY.
- **Croire qu'un delta faible veut dire un risque faible.** Un put vendu à delta 0,10 peut perdre plusieurs fois le crédit encaissé lors d'un krach. Le delta mesure l'exposition actuelle, pas la perte possible.
- **Considérer le delta neutre comme sans risque.** Le gamma recrée du delta dès que le marché bouge, et le vega reste là.
- **Extrapoler les grecques sur de gros mouvements.** Elles sont fiables pour quelques dollars ou quelques points de VI. Au-delà, il faut recalculer ou simuler.
- **Ignorer la volatilité implicite avant un événement.** Acheter juste avant des résultats, c'est souvent payer la VI au plus haut (scénario B).
- **Garder une position vendeuse jusqu'à l'échéance par réflexe.** Le rapport rendement/risque se dégrade à mesure que le gamma grimpe.
- **Faire une confiance aveugle aux chiffres de la plateforme.** Ils dépendent du modèle, de la VI utilisée et de la qualité des cotations, qui peut être mauvaise à l'ouverture ou sur des options peu liquides.

Les options comportent un risque de perte important et ne conviennent pas à tous les investisseurs. Avant de trader des options cotées aux États-Unis, la lecture du document officiel de l'OCC sur les caractéristiques et les risques des options standardisées est un minimum. Cet article est pédagogique : ce n'est pas un conseil en investissement.

## Sources

- [OCC – Characteristics and Risks of Standardized Options (juin 2024)](https://www.theocc.com/getcontentasset/a151a9ae-d784-4a15-bdeb-23a029f50b70/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/riskstoc.pdf)
- [Options Industry Council – Understanding Options Greeks](https://www.optionseducation.org/advancedconcepts/understanding-options-greeks)
- [IBKR Campus – Introduction to Options: The Greeks](https://www.interactivebrokers.com/campus/trading-lessons/introduction-to-options-the-greeks/)
- [IBKR Campus – Risk Navigator and Alarms](https://www.interactivebrokers.com/campus/trading-lessons/risk-navigator-and-alarms/)
