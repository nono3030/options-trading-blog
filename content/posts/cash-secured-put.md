---
title: 'Cash secured put : guide complet, exemples et risques'
description: 'Cash secured put : fonctionnement, exemple chiffré complet, choix du strike, assignation, fiscalité 2026 et erreurs à éviter avant de vendre un put.'
keyword: cash secured put
slug: cash-secured-put
date: '2026-11-04'
updated: '2026-11-04'
tags:
- options
- vente de put
- stratégies
faq:
- q: Combien de capital faut-il pour un cash secured put ?
  a: 'Il faut bloquer le strike multiplié par 100 pour chaque contrat d''options américaines standard : 9 500 $ pour un put de strike 95. La prime encaissée réduit légèrement l''effort net, mais la règle prudente est de garder l''intégralité du montant en cash, non utilisé ailleurs.'
- q: Quelle est la différence entre un cash secured put et un put nu (naked put) ?
  a: 'Le profil de gain et de perte à l''échéance est identique : c''est une vente de put. La différence tient au financement. Le cash secured put bloque la totalité du montant d''achat, alors que le put nu n''immobilise qu''une marge, ce qui crée un effet de levier et un risque d''appel de marge si le marché baisse.'
- q: Que se passe-t-il si je suis assigné sur mon put ?
  a: Sur une option sur action ou ETF américaine, vous achetez 100 titres par contrat au prix d'exercice, quel que soit le cours du moment. Votre prix de revient économique est le strike moins la prime encaissée. Vous pouvez ensuite garder les titres, les revendre ou vendre des calls couverts dessus.
- q: Peut-on faire un cash secured put sur le SPX ?
  a: 'Techniquement oui, mais un put SPX représente l''indice multiplié par 100 $, soit plusieurs centaines de milliers de dollars à sécuriser. Le SPX se règle en espèces : en cas de perte, vous payez la différence en cash, sans recevoir d''actions. Le Mini-SPX (XSP), dix fois plus petit, est plus accessible.'
- q: Le cash secured put est-il une stratégie sans risque ?
  a: Non. Le gain est plafonné à la prime alors que la perte peut aller jusqu'au strike moins la prime si le sous-jacent s'effondre. Le cash évite l'appel de marge, pas la perte. Le risque est proche de celui d'un achat d'actions, avec un potentiel de hausse limité.
---

Un cash secured put consiste à **vendre une option put** tout en gardant de côté **assez de liquidités pour acheter les actions** si on est assigné : strike × 100 par contrat. Vous encaissez une prime tout de suite, et en échange vous vous engagez à acheter le sous-jacent au prix d'exercice s'il passe en dessous à l'échéance. C'est une stratégie pour qui *veut vraiment* détenir le titre à ce prix. Le risque est proche de celui d'un achat d'actions, mais avec un gain limité à la prime.

## Comment fonctionne un cash secured put

Si la notion de put n'est pas encore claire pour vous, commencez par mon [explication simple de l'option put avec exemples chiffrés](/option-put-explication-simple/). Ici, on se place du côté du **vendeur**.

En vendant un put, vous prenez trois engagements :

1. **Vous encaissez la prime** immédiatement (prime × 100 par contrat).
2. **Vous acceptez l'obligation** d'acheter 100 actions par contrat au strike si l'acheteur exerce.
3. **Vous immobilisez le cash** nécessaire (strike × 100) pendant toute la durée de la position. C'est ce qui rend le put « cash secured ».

À l'échéance, deux scénarios :

- **Le cours est au-dessus du strike** : le put expire sans valeur, vous gardez la prime et le cash redevient libre.
- **Le cours est en dessous du strike** : vous êtes assigné, vous achetez les actions au strike. Votre prix de revient économique = **strike − prime**.

L'Options Industry Council (OIC) insiste sur un point : contrairement au vendeur de put nu, qui ne cherche que la prime, le vendeur de cash secured put **voit l'assignation comme un résultat acceptable**. Tout le reste découle de là. Si vous ne voulez pas posséder l'action à ce prix, ce n'est pas un cash secured put. C'est de la vente de prime déguisée.

### Les formules à connaître

| Élément | Formule |
|---|---|
| Capital à bloquer | Strike × 100 × nombre de contrats |
| Gain maximum | Prime × 100 (si le cours finit au-dessus du strike) |
| Point mort à l'échéance | Strike − prime |
| Perte maximale théorique | (Strike − prime) × 100, si l'action tombe à 0 |
| Rendement sur la période | Prime ÷ (strike − prime) |

## Exemple chiffré complet

Exemple **hypothétique** : l'action XYZ cote 100 $. Vous l'avez étudiée et vous seriez prêt à l'acheter vers 95 $.

- **Vente** : 1 put XYZ strike 95, échéance dans 35 jours
- **Prime encaissée** : 1,50 $ → **150 $** (hors commissions)
- **Cash bloqué** : 95 × 100 = **9 500 $**
- **Point mort** : 95 − 1,50 = **93,50 $**
- **Gain max** : 150 $, soit 1,58 % du capital bloqué sur 35 jours
- **Perte max théorique** : 9 350 $ si XYZ tombe à 0

Le rendement de 1,58 % donnerait environ 16,5 % en annualisé simple. **Ne raisonnez pas comme ça** : ce chiffre suppose que vous pourrez refaire la même opération tous les mois sans jamais encaisser de grosse perte, ce qui n'arrive pas.

### Résultat à l'échéance selon le cours de XYZ

| Cours à l'échéance | Ce qui se passe | Résultat du put vendu | Comparaison : achat de 100 actions à 100 $ |
|---|---|---|---|
| 110 $ | Expiration sans valeur | **+150 $** | +1 000 $ |
| 100 $ | Expiration sans valeur | **+150 $** | 0 $ |
| 95 $ | Zone d'incertitude (voir *pin risk*) | +150 $ si pas d'assignation | −500 $ |
| 93,50 $ | Assigné, au point mort | **0 $** | −650 $ |
| 90 $ | Assigné à 95 $ | **−350 $** latent | −1 000 $ |
| 80 $ | Assigné à 95 $ | **−1 350 $** latent | −2 000 $ |

Ce tableau montre l'arbitrage réel. Le cash secured put **perd moins** qu'un achat direct à 100 $ quand le titre baisse (strike plus bas + prime), mais il **rate toute la hausse** au-delà de la prime. À 110 $, l'acheteur d'actions gagne 1 000 $ et vous 150 $.

Autre point important : à 80 $, vous détenez des actions qui valent 8 000 $ et pour lesquelles vous avez payé 9 500 $. Le cash vous a évité un appel de marge, **pas la perte**.

### Cash secured put ou ordre limite à 95 $ ?

La comparaison la plus honnête, c'est avec un ordre d'achat à cours limité à 95 $ :

- Si XYZ ne descend jamais à 95 $ : l'ordre limite ne rapporte rien, le put vous rapporte 150 $.
- Si XYZ passe brièvement à 94 $ puis remonte à 102 $ avant l'échéance : l'ordre limite est exécuté et vous profitez du rebond. Le put, lui, expire sans valeur : vous gardez 150 $, mais vous n'avez pas les actions.
- Si XYZ s'effondre à 70 $ : dans les deux cas, vous êtes acheteur à 95 $. Le put vous laisse juste 1,50 $ de coussin en plus.

## Choisir le strike, l'échéance et le sous-jacent

### Le sous-jacent d'abord

La seule question qui compte : **est-ce que je garderais ce titre s'il perdait 30 % juste après l'assignation ?** Si la réponse est non, changez de sous-jacent. Une prime élevée signale presque toujours une volatilité implicite élevée, donc un risque perçu élevé par le marché, pas une aubaine.

### Le strike et le delta

En pratique, beaucoup de vendeurs de puts choisissent un strike hors de la monnaie avec un delta autour de 0,20 à 0,30. Le delta donne une **approximation grossière** de la probabilité de finir dans la monnaie, pas une probabilité exacte. Pour bien comprendre ce que mesurent delta, theta et vega sur une position vendeuse, voyez mon guide sur les [grecques des options](/grecques-des-options-delta-gamma-theta-vega/).

- **Strike proche du cours (delta 0,40-0,50)** : prime plus grosse, assignation plus probable. Logique si vous voulez surtout acheter le titre.
- **Strike éloigné (delta 0,10-0,15)** : prime faible, rendement souvent dérisoire au regard du capital bloqué et du risque de krach.

### L'échéance

Les échéances de 30 à 45 jours sont une habitude répandue chez les vendeurs de prime, parce que le theta s'accélère sur cette période tout en laissant du temps pour gérer la position. Ce n'est pas une règle magique. Ce que je vérifie systématiquement avant d'ouvrir :

- **Une publication de résultats tombe-t-elle avant l'échéance ?** Si oui, le risque de gap est réel, même si la prime est plus élevée.
- **L'écart bid/ask** : sur une option peu liquide, un écart de 0,20 $ sur une prime de 1,50 $, c'est plus de 13 % de votre gain potentiel perdu à l'entrée.
- **L'open interest** sur le strike visé.

## Le cas des indices : SPY, QQQ, SPX et XSP

Sur **SPY et QQQ**, les options sont de style américain et se règlent par livraison : l'assignation vous fait recevoir 100 parts d'ETF par contrat, et elle peut intervenir **à tout moment** avant l'échéance.

**Attention pour les résidents européens** : en tant que client particulier, on ne peut généralement pas acheter directement des ETF américains comme SPY ou QQQ (faute de document d'informations clés PRIIPs). Une assignation peut quand même vous faire détenir des parts. Vérifiez la politique de votre courtier avant d'ouvrir la position, notamment pour savoir ce que vous pourrez faire ensuite avec ces parts.

Sur **SPX**, c'est différent. Selon Cboe, les options SPX sont de **style européen** (exercice uniquement à l'échéance, donc pas d'assignation anticipée) et **réglées en espèces**, avec un multiplicateur de 100 $. Conséquences :

- Pas d'actions livrées : en cas de perte, votre compte est débité de la différence. On n'est plus vraiment dans la logique « acheter le titre moins cher ».
- Un put SPX avec un indice vers 6 500 représente **650 000 $ de notionnel**. Le sécuriser entièrement en cash n'est pas réaliste pour la plupart des particuliers.
- Le **Mini-SPX (XSP)** vaut 1/10 du SPX : avec un indice vers 650, un put représente environ 65 000 $ de notionnel.

### Exemple hypothétique sur XSP

XSP à 650. Vente d'un put 620 à 40 jours pour 4,50 $ → prime de **450 $**, cash bloqué **62 000 $**, point mort **615,50**. Si XSP termine à 600, le règlement en espèces est de (620 − 600) × 100 = 2 000 $, soit une **perte nette de 1 550 $**. Le rendement sur capital est plus faible que sur une action individuelle (0,73 % ici), parce que la volatilité d'un indice est en général plus faible.

À noter : la fiscalité « 60/40 » mise en avant par Cboe pour le SPX concerne **les contribuables américains**. Elle ne s'applique pas à un résident français, belge, suisse ou canadien.

## Gérer la position : clôturer, rouler, accepter l'assignation

### Clôturer avant l'échéance

Racheter le put avant l'échéance verrouille le gain et libère le capital. Beaucoup de vendeurs rachètent quand ils ont encaissé environ la moitié de la prime : le reste du gain potentiel ne vaut souvent plus le risque de gamma en fin de vie. C'est une règle de gestion, pas une garantie.

### Rouler (roll)

Reprenons XYZ : à 10 jours de l'échéance, l'action est à 94 $ et le put 95 vaut 2,60 $. Deux options de roll (chiffres hypothétiques) :

| Roll | Opération | Crédit/débit net | Nouveau point mort |
|---|---|---|---|
| Même strike, plus loin | Rachat du 95 à 2,60 $, vente du 95 à 45 jours à 3,90 $ | +1,30 $ | 95 − (1,50 + 1,30) = 92,20 $ |
| Strike plus bas, plus loin | Rachat du 95 à 2,60 $, vente du 92 à 45 jours à 2,70 $ | +0,10 $ | 92 − (1,50 + 0,10) = 90,40 $ |

Sur le premier roll, la perte réalisée sur le put racheté est de 2,60 − 1,50 = 1,10 $ (110 $), compensée par la nouvelle prime. Un roll n'efface pas une perte : c'est **une nouvelle position**, qui prolonge votre exposition. Rouler indéfiniment un put sur un titre en chute libre, c'est la meilleure façon de transformer une petite perte en grosse perte.

### Accepter l'assignation et passer au covered call

Si vous êtes assigné, vous détenez 100 actions par contrat. Beaucoup de traders vendent alors des calls sur ces actions : c'est la stratégie dite de la « roue » (*wheel*). Je détaille cette seconde jambe dans mon article sur le [covered call, avec exemples chiffrés et risques](/covered-call-strategie/). Une précision utile : à strike et échéance identiques, un put vendu et un covered call ont un profil à l'échéance quasi identique (parité put-call). La roue n'est donc pas un « double revenu » magique. C'est la même exposition, exprimée de deux façons.

## Risques et erreurs fréquentes

**1. Croire que « cash secured » veut dire « sans risque ».** Le cash supprime le risque d'appel de marge, pas le risque de marché. Gain plafonné, perte large : c'est un profil asymétrique défavorable en cas de krach.

**2. Utiliser la marge sans le savoir.** Dans un compte marge, le courtier n'exige pas la totalité du strike pour un put vendu. La formule réglementaire de base aux États-Unis tourne autour de 20 % du sous-jacent, ajustés de la partie hors de la monnaie, avec un minimum de 10 % du strike, plus la prime. Interactive Brokers indique d'ailleurs que l'exigence pour un put vendu dans un **compte cash** correspond au strike. Si votre compte marge affiche une exigence de 2 000 $ pour un put 95, rien ne vous empêche techniquement d'en vendre quatre : c'est le piège classique. Pour rester « cash secured », gardez vous-même strike × 100 de côté.

**3. Oublier la devise.** Pour un investisseur en EUR, CHF ou CAD, le cash bloqué et les actions reçues sont en USD. Une baisse du dollar peut aggraver une perte, ou rogner un gain. Si vous êtes assigné sans avoir de USD sur le compte, le courtier crée généralement un solde USD négatif, c'est-à-dire un emprunt facturé.

**4. Ignorer l'assignation anticipée.** Le document de l'OCC sur les risques des options standardisées le rappelle : le vendeur d'une option de style américain peut être assigné **à tout moment** jusqu'à l'échéance. Pour un put, c'est surtout le cas quand il est profondément dans la monnaie et qu'il ne lui reste presque plus de valeur temps.

**5. Le pin risk le jour de l'échéance.** Si le cours finit très près du strike, vous ne savez pas avec certitude si vous serez assigné. Un détenteur peut encore exercer après la clôture en fonction des mouvements after-hours. Si vous ne voulez pas d'incertitude, rachetez le put avant la clôture.

**6. Surdimensionner.** Vendre des puts sur cinq valeurs tech corrélées, ce n'est pas se diversifier. En cas de baisse générale, tout est assigné en même temps. Personnellement, je raisonne en exposition totale assignable, pas en nombre de positions.

**7. Courir après la prime.** Les primes les plus juteuses se trouvent sur les titres les plus risqués (biotechs avant un résultat d'essai, valeurs très endettées…). Le marché ne paie pas une forte prime sans raison.

Si vous débutez, lisez d'abord le [guide concret du trading d'options pour débutant](/trading-options-debutant/) avant de vendre votre premier put.

## Fiscalité : ce qu'il faut savoir (et vérifier)

La fiscalité dépend de votre pays de résidence et de votre situation. Ce qui suit est un repère, pas un conseil fiscal.

- **France** : les gains sur titres et produits dérivés des particuliers relèvent en principe du régime des plus-values mobilières. Depuis le 1er janvier 2026, le PFU passe de 30 % à **31,4 %** (12,8 % d'impôt + 18,6 % de prélèvements sociaux), suite à la hausse de la CSG votée dans la LFSS 2026. L'option pour le barème progressif reste possible. Sur le traitement précis de la prime d'un put assigné, qui vient en principe ajuster le prix de revient des actions, et sur la conversion USD/EUR de chaque opération, faites valider vos calculs par un professionnel ou au regard du BOFiP. Un compte ouvert chez un courtier étranger (Interactive Brokers, par exemple) doit être déclaré chaque année (formulaire 3916).
- **Belgique** : depuis le 1er janvier 2026, une contribution de **10 %** s'applique aux plus-values sur actifs financiers, **produits dérivés et options compris**, avec une exonération annuelle de 10 000 € par contribuable selon les sources consultées. Le risque de requalification en gestion « anormale » ou spéculative, taxée à 33 %, n'a pas disparu pour un trading très actif.
- **Suisse** : les gains en capital sur la fortune privée sont en principe exonérés, sauf requalification en commerçant professionnel de titres. Avec une activité de vente d'options régulière, ce point mérite d'être examiné avec votre administration cantonale.
- **Québec/Canada** : le traitement des primes d'options (gain en capital ou revenu d'entreprise) dépend de votre situation. Consultez un fiscaliste.

## Ce que je retiens après plusieurs années de vente de puts

Le cash secured put n'est pas une machine à revenus. C'est **une façon d'acheter un titre que vous voulez, à un prix que vous avez choisi, en étant payé pour attendre**, avec un gain plafonné en échange. Il fonctionne bien quand le sous-jacent est solide, quand la taille de position est raisonnable et quand l'assignation est vraiment acceptable. Il fait mal quand on choisit le titre pour sa prime plutôt que pour sa qualité, quand on utilise la marge sans le savoir ou quand on roule sans fin un perdant.

Avant chaque vente, posez-vous trois questions : *Est-ce que je veux ce titre à ce prix ? Ai-je vraiment le cash, dans la bonne devise ? Que fais-je s'il perd 30 % ?* Si l'une des réponses vous gêne, ne vendez pas le put.

## Sources

- [Options Industry Council (OIC) – Cash-Secured Put](https://www.optionseducation.org/strategies/all-strategies/cash-secured-put)
- [OCC – Characteristics and Risks of Standardized Options (juin 2024)](https://www.theocc.com/getcontentasset/a151a9ae-d784-4a15-bdeb-23a029f50b70/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/riskstoc.pdf)
- [Cboe – S&P 500 Index (SPX) Options](https://www.cboe.com/tradable-products/sp-500/spx-options)
- [Interactive Brokers – Options Margin Requirements](https://www.interactivebrokers.com/en/trading/margin-options.php)
- [Legifiscal – Flat-tax (PFU) : champ d'application et taux applicables en 2026](https://www.legifiscal.fr/reperes-fiscaux/flat-tax-pfu-champ-application-taux-applicables-2026.html)
