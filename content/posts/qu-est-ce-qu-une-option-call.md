---
title: Qu'est-ce qu'une option call ? Définition et exemples
description: Qu'est-ce qu'une option call ? Définition simple, exemple chiffré (strike, prime, point mort), achat vs vente, SPX vs SPY, risques et fiscalité 2026.
keyword: qu'est-ce qu'une option call
slug: qu-est-ce-qu-une-option-call
date: '2026-10-19'
updated: '2026-10-19'
tags:
- options
- call
- débutant
- spx
faq:
- q: Quelle est la différence entre une option call et une option put ?
  a: Un call donne le droit d'acheter le sous-jacent à un prix fixé (le strike). Un put donne le droit de le vendre à un prix fixé. On achète un call quand on anticipe une hausse et un put quand on anticipe une baisse ou qu'on veut se couvrir.
- q: Peut-on perdre plus que la prime en achetant un call ?
  a: Non. Quand vous achetez un call, votre perte maximale est la prime payée, plus les commissions. C'est le vendeur d'un call non couvert qui s'expose à une perte théoriquement illimitée.
- q: Combien coûte une option call ?
  a: 'Le prix affiché est la prime par action. Sur les options américaines sur actions et ETF, un contrat porte sur 100 actions : une prime affichée à 2,50 $ coûte donc 250 $, hors commissions. Le prix dépend du cours du sous-jacent, du strike, du temps restant et de la volatilité implicite.'
- q: Faut-il exercer son call pour encaisser le gain ?
  a: Presque jamais. Dans la plupart des cas, on revend le call sur le marché avant l'échéance, ce qui permet d'encaisser aussi la valeur temps restante. Exercer oblige en plus à disposer de 100 fois le strike en liquidités, ou en marge, pour recevoir les actions.
- q: Que se passe-t-il si mon call est dans la monnaie à l'échéance ?
  a: 'Sur une action ou un ETF comme SPY, il est en principe exercé automatiquement et vous recevez 100 actions par contrat, à condition d''avoir les fonds nécessaires. Sur SPX, le règlement se fait en espèces : vous recevez la différence entre le cours de règlement et le strike, multipliée par 100.'
---

Une option call (ou option d'achat) est un contrat qui vous donne **le droit, mais pas l'obligation, d'acheter un actif à un prix fixé à l'avance (le strike), jusqu'à une date donnée (l'échéance)**. Pour obtenir ce droit, vous payez une prime au vendeur. Si vous achetez un call, votre perte est limitée à cette prime. Si vous en vendez un, vous encaissez la prime mais vous prenez une obligation qui peut coûter très cher.

Voilà la définition. Pour savoir vous en servir, il faut surtout comprendre combien coûte un contrat, où se situe votre point mort, ce qui se passe à l'échéance et pourquoi un call peut perdre de la valeur même quand le marché monte. C'est l'objet de la suite.

## La définition d'une option call, élément par élément

Un call se définit par quatre paramètres. Vous les retrouverez sur n'importe quel ticket d'ordre, chez Interactive Brokers comme ailleurs.

| Élément | Ce que c'est | Exemple |
|---|---|---|
| **Sous-jacent** | L'actif sur lequel porte l'option : action, ETF ou indice | Action XYZ, ETF SPY, indice SPX |
| **Strike (prix d'exercice)** | Le prix auquel vous pouvez acheter | 105 $ |
| **Échéance** | La date limite du droit | Dans 45 jours |
| **Prime** | Le prix de l'option, coté **par action** | 2,50 $ |
| **Multiplicateur** | Le nombre d'unités couvertes par un contrat | 100 (options US standard) |

Le multiplicateur est le premier piège pour un débutant. Each contract represents 100 shares of the underlying stock. Une prime affichée à 2,50 $ vous coûte donc **250 $ par contrat**, hors commissions. Il n'est pas nécessaire de détenir l'action pour acheter ou vendre un call sur ce titre.

### Dans la monnaie, à la monnaie, hors de la monnaie

- **Dans la monnaie (ITM)** : le cours du sous-jacent est au-dessus du strike. Le call a une valeur intrinsèque.
- **À la monnaie (ATM)** : le cours est égal ou très proche du strike.
- **Hors de la monnaie (OTM)** : le cours est sous le strike. Le call n'a aucune valeur intrinsèque, seulement une valeur temps.

### Valeur intrinsèque et valeur temps

La prime se décompose en deux parties :

- **Valeur intrinsèque** = cours du sous-jacent − strike (si ce montant est positif, sinon zéro).
- **Valeur temps** = prime − valeur intrinsèque. C'est ce que vous payez pour le temps restant et pour l'incertitude, mesurée par la volatilité implicite.

Prenons XYZ à 108 $, à 20 jours de l'échéance, avec un call 105 coté 4,20 $. La valeur intrinsèque est de 3,00 $ et la valeur temps de 1,20 $. Si XYZ reste à 108 $ jusqu'à l'échéance, le call ne vaudra plus que 3,00 $ : la valeur temps tombe à zéro le jour de l'échéance. On appelle cette érosion le **theta**. En pratique, elle s'accélère nettement dans les dernières semaines.

## Exemple chiffré complet : l'achat d'un call

Les chiffres ci-dessous sont **illustratifs**. Ce ne sont pas des cotations réelles.

**Situation** : l'action XYZ cote 100 $. Vous pensez qu'elle peut monter dans les prochaines semaines.

- Achat de **1 call XYZ strike 105, échéance 45 jours**
- Prime : **2,50 $**, soit **250 $ payés** (2,50 × 100)
- **Point mort à l'échéance** : strike + prime = 105 + 2,50 = **107,50 $**
- **Perte maximale** : **250 $**, plus les commissions
- **Gain maximal** : théoriquement illimité

Le tableau compare le résultat à l'échéance avec l'achat direct de 100 actions à 100 $, soit 10 000 $ investis.

| Cours de XYZ à l'échéance | Valeur du call | Résultat du call | Rendement sur 250 $ | Résultat de 100 actions |
|---|---|---|---|---|
| 95 $ | 0 $ | −250 $ | −100 % | −500 $ (−5 %) |
| 100 $ | 0 $ | −250 $ | −100 % | 0 $ |
| 105 $ | 0 $ | −250 $ | −100 % | +500 $ (+5 %) |
| 107,50 $ | 250 $ | 0 $ | 0 % | +750 $ (+7,5 %) |
| 110 $ | 500 $ | +250 $ | +100 % | +1 000 $ (+10 %) |
| 115 $ | 1 000 $ | +750 $ | +300 % | +1 500 $ (+15 %) |
| 120 $ | 1 500 $ | +1 250 $ | +500 % | +2 000 $ (+20 %) |

### Ce que ce tableau montre

1. **L'effet de levier joue dans les deux sens.** Avec 250 $, vous profitez de la hausse de 100 actions. Mais si XYZ termine à 105 $, donc en hausse de 5 %, vous perdez **100 %** de votre mise, alors que l'actionnaire gagne 500 $.
2. **Il ne suffit pas d'avoir raison sur la direction.** Il faut une hausse **assez forte** (+7,5 % pour seulement atteindre le point mort) et **assez rapide** (avant l'échéance).
3. **Le risque en dollars est plus faible, mais le risque en pourcentage est total.** C'est ce qui pousse beaucoup de débutants à acheter trop de contrats « parce que ce n'est pas cher ».

### Revendre ou exercer ?

Dans la grande majorité des cas, on **revend le call** au lieu de l'exercer. Reprenons XYZ à 108 $ et le call 105 coté 4,20 $ :

- **Revente** : vous encaissez 420 $.
- **Exercice** : vous payez 10 500 $ (105 × 100) pour recevoir des actions qui valent 10 800 $. Cela fait 300 $ de valeur, et vous abandonnez les 120 $ de valeur temps.

Exercer avant l'échéance détruit la valeur temps. Il y a aussi une contrainte de trésorerie : pour recevoir 100 actions, il faut 100 fois le strike en cash ou en marge disponible.

## Vendre un call : l'autre côté du contrat

Chaque call acheté a été vendu par quelqu'un. Le vendeur (ou l'émetteur de l'option) a l'obligation de vendre l'actif sous-jacent au prix défini si l'acheteur exerce. Avec le même exemple, vu du vendeur :

- Prime encaissée : **250 $** = **gain maximal**
- Point mort : **107,50 $**
- À 110 $ : −250 $. À 115 $ : −750 $. À 120 $ : −1 250 $. **Plus le titre monte, plus la perte grossit, sans limite théorique.**

Le risque dépend de ce que le vendeur détient à côté :

- **Call couvert (covered call)** : vous détenez déjà 100 actions XYZ. Si le call est exercé, vous livrez vos actions au strike. Le risque est celui de l'action, moins la prime encaissée. En contrepartie, votre hausse est plafonnée au-dessus du strike.
- **Call nu (naked call)** : vous vendez sans détenir le titre. La perte est théoriquement illimitée. La plupart des courtiers réservent ce type de position aux comptes avec les niveaux d'autorisation les plus élevés, et je le déconseille formellement à un débutant.

### L'alternative à risque défini : le call spread

Comme je vends surtout de la prime en stratégies à risque défini, voici la version « encadrée » d'un pari haussier : le **bull call spread**.

- Achat du call 105 à 2,50 $ et vente du call 110 à 1,00 $
- **Débit net** : 1,50 $, soit **150 $** = **perte maximale**
- **Gain maximal** : (110 − 105 − 1,50) × 100 = **350 $**, atteint si XYZ termine au-dessus de 110 $
- **Point mort** : 105 + 1,50 = **106,50 $**

Vous renoncez à la hausse au-delà de 110 $. En échange, le pari coûte moins cher et le point mort est plus bas. Ce type de construction est détaillé dans mon [guide concret pour débuter le trading d'options](/trading-options-debutant/).

## Call sur action, sur SPY ou sur SPX : des différences importantes

Les options les plus traitées par les particuliers francophones sont sur les indices US. Le mot « call » y désigne le même droit, mais les règles de fonctionnement changent.

| Caractéristique | Call sur action US | Call sur SPY (ETF) | Call sur SPX (indice) |
|---|---|---|---|
| Style d'exercice | Américain (à tout moment) | Américain | Européen (à l'échéance seulement) |
| Règlement | Livraison de 100 actions | Livraison de 100 parts de SPY | En espèces |
| Multiplicateur | 100 | 100 | 100 |
| Taille relative | Selon l'action | Environ 1/10 du SPX | Indice complet |
| Risque d'assignation anticipée pour le vendeur | Oui | Oui | Non |

Sur SPX, SPX Options are exchange-traded European exercise cash settled options based on the value of the S&P 500. La taille est importante : selon Cboe, avec un indice à 6 500 points, le notionnel d'un contrat SPX est d'environ 650 000 $, contre environ 65 000 $ pour le mini-SPX (XSP). Cboe donne un exemple de règlement en espèces : un acheteur détient un call SPX 4500, l'indice est réglé à 4540 à l'échéance, et son compte est crédité de 4 000 $. Le calcul est (4540 − 4500) × 100.

Un détail compte quand on garde ses positions jusqu'à l'échéance. With an AM-settled option, the value is set by the opening price on the expiration date: the last trade occurs Thursday night, but the settlement value isn't known until Friday's open, leaving some overnight risk. Les SPX mensuels standard sont réglés le matin (AM). Les SPXW (hebdomadaires et quotidiens) sont réglés à la clôture (PM). Trade weekly options up to the last day of expiration at market close every trading day of the week.

**En pratique** : un call SPY dans la monnaie à l'échéance vous fait recevoir 100 parts de SPY, ce qui représente plusieurs dizaines de milliers de dollars. Un call SPX vous verse simplement la différence en cash. Avant de garder une position jusqu'à l'échéance, je vérifie toujours le mode de règlement.

## Ce qui fait bouger le prix d'un call

Pas besoin de maîtriser toutes les « grecques » pour commencer. Trois notions suffisent :

- **Delta** : la variation approximative de la prime pour 1 $ de hausse du sous-jacent. Un call à la monnaie a un delta proche de 0,50 : la prime gagne environ 0,50 $ quand l'action prend 1 $. Un call très hors de la monnaie a un delta faible. Il réagit peu, même si l'action monte.
- **Theta** : la perte de valeur temps chaque jour. Elle joue contre l'acheteur et en faveur du vendeur.
- **Volatilité implicite (IV)** : plus le marché anticipe de mouvements, plus les primes sont chères. Après un événement attendu (résultats d'entreprise, réunion de la Fed), l'IV retombe souvent d'un coup. Un call peut alors **perdre de la valeur même si l'action monte un peu**. C'est le fameux « IV crush ».

## Risques et erreurs fréquentes

Voici les erreurs que je vois le plus souvent chez les débutants. J'en ai fait certaines moi-même.

1. **Acheter des calls très hors de la monnaie parce qu'ils sont « pas chers ».** Une prime de 0,20 $ coûte peu parce que la probabilité qu'elle rapporte est faible. Une série de petites pertes à −100 % finit par peser lourd.
2. **Oublier le multiplicateur.** 2,50 $ à l'écran, c'est 250 $ par contrat. Dix contrats, c'est 2 500 $.
3. **Acheter juste avant les résultats** sans tenir compte de la volatilité implicite. Vous pouvez avoir raison sur la direction et perdre quand même.
4. **Garder un call américain dans la monnaie jusqu'à l'échéance sans en avoir les moyens.** Une option dans la monnaie, même de quelques cents, est en principe exercée automatiquement. Si vous n'avez pas 100 fois le strike disponible, votre courtier peut liquider la position, parfois à un mauvais prix. Lisez la politique de votre courtier sur ce point.
5. **Vendre des calls nus.** La perte n'a pas de plafond théorique. Une annonce de rachat ou un gap de +30 % à l'ouverture suffit à faire sauter un compte.
6. **Négliger l'assignation anticipée quand on vend un call sur action.** Sur une option de style américain, le vendeur peut être assigné avant l'échéance. Le risque est plus élevé à l'approche d'une date de détachement de dividende, quand le call est dans la monnaie et que sa valeur temps est faible.
7. **Ignorer la liquidité.** Sur une option peu traitée, l'écart entre le prix acheteur et le prix vendeur peut atteindre 10 % de la prime. Je ne trade que des séries liquides et je passe des ordres à cours limité, jamais au marché.
8. **Oublier le risque de change.** Les primes sont en dollars. Pour un compte en euros, en francs suisses ou en dollars canadiens, le taux de change s'ajoute au résultat, à la hausse comme à la baisse.

Pour cadrer la taille de vos positions et la gestion du risque avant de passer votre premier ordre, la méthode est détaillée dans [Trading options débutant : le guide concret pour 2026](/trading-options-debutant/).

## Et la fiscalité ?

C'est le point qui varie le plus d'un pays à l'autre. Tout ce qui suit est **indicatif** et ne remplace pas une vérification auprès de l'administration fiscale ou d'un conseiller.

- **France** : pour un particulier, les gains sur options passés via un compte-titres sont en principe imposés comme des plus-values mobilières. Faites confirmer le traitement exact de vos opérations, notamment les primes encaissées en tant que vendeur, sur impots.gouv.fr ou auprès d'un conseiller. Côté taux, les plus-values de cession de valeurs mobilières et droits sociaux réalisées par les particuliers depuis le 1er janvier 2025 sont soumises au PFU au nouveau taux global de 31,4 %, sauf option pour le barème progressif. La hausse vient de la loi de financement de la Sécurité sociale pour 2026 ayant augmenté le taux applicable de 1,4 point. Si vous utilisez un courtier étranger comme Interactive Brokers, pensez aussi à déclarer le compte détenu à l'étranger.
- **Belgique, Suisse, Québec** : les règles sont différentes (statut d'investisseur « normal » ou « professionnel », gestion « en bon père de famille », gains en capital au Canada). Je ne les détaille pas ici, faute de pouvoir les vérifier ligne par ligne.
- **La règle « 60/40 » mise en avant par Cboe pour SPX** relève de la fiscalité américaine. Elle ne s'applique pas telle quelle à un résident fiscal français, belge, suisse ou québécois.

## Ce que je retiens après des années de pratique

- Un call acheté est un **pari sur l'ampleur et sur le délai** d'une hausse, pas seulement sur sa direction.
- Avant chaque trade, je note quatre chiffres : **coût total, point mort, perte maximale, gain maximal**. Si je ne sais pas les écrire, je ne passe pas l'ordre.
- Je préfère les structures à **risque défini** (spreads) aux positions à risque ouvert.
- Je vérifie le **style d'exercice et le mode de règlement** (SPY ou SPX) avant de garder une position jusqu'à l'échéance.

Cet article est pédagogique. Ce n'est pas un conseil en investissement. Les options sont des produits à effet de levier : vous pouvez perdre la totalité de la prime investie et, en tant que vendeur, bien davantage.

## Sources

- [Characteristics and Risks of Standardized Options (OCC, juin 2024)](https://www.theocc.com/getcontentasset/a151a9ae-d784-4a15-bdeb-23a029f50b70/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/riskstoc.pdf)
- [SPX Index Options – Fact Sheet (Cboe)](https://cdn.cboe.com/resources/spx/spx-fact-sheet.pdf)
- [Index Options Benefits: Cash Settlement (Cboe)](https://www.cboe.com/tradable_products/index-options-benefits-cash-settlement/)
- [Cboe SPX – comparatif SPX, SPXW, XSP, Nanos (Interactive Brokers)](https://www.interactivebrokers.com/en/trading/cboe.php)
- [La fiscalité des plus-values boursières sur un compte-titres (LCL, avril 2026)](https://www.lcl.fr/mag/budget/bourse-fiscalite-values-boursieres-sur-un-compte-titres)
