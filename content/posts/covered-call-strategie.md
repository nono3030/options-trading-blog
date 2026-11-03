---
title: 'Covered call : stratégie, exemples chiffrés et risques'
description: 'Stratégie covered call expliquée pas à pas : choix du strike, exemple chiffré complet, assignation, roll, dividendes, fiscalité 2026 et erreurs à éviter.'
keyword: covered call stratégie
slug: covered-call-strategie
date: '2026-11-03'
updated: '2026-11-03'
tags:
- covered call
- vente de prime
- stratégies options
faq:
- q: Le covered call est-il une stratégie sans risque ?
  a: Non. Vous gardez presque tout le risque de baisse de l'action, car la prime encaissée ne compense qu'une petite partie de la chute. En échange, votre gain est plafonné au strike plus la prime.
- q: Peut-on faire un covered call avec moins de 100 actions ?
  a: Non, pas avec des options standard sur actions ou ETF américains, car un contrat porte sur 100 actions. Avec 60 actions, le call vendu ne serait couvert qu'en partie, et la plupart des courtiers le refusent sans marge suffisante.
- q: Que se passe-t-il si mon call couvert est assigné ?
  a: Vos 100 actions sont vendues au prix d'exercice et vous gardez la prime encaissée au départ. Vous touchez alors le gain maximal de la stratégie, mais vous ne détenez plus les titres et ne profitez plus d'une hausse au-delà du strike.
- q: Quel strike et quelle échéance choisir pour un covered call ?
  a: Beaucoup de vendeurs de prime travaillent entre 30 et 45 jours d'échéance avec un delta de 0,20 à 0,35, mais aucun réglage ne convient à tout le monde. Plus le strike est proche du cours, plus la prime est élevée et plus le risque d'être assigné augmente.
- q: Comment sont imposées les primes de covered call en France ?
  a: 'Pour un particulier qui opère à titre occasionnel sur un compte-titres, les profits sur options relèvent de l''article 150 ter du CGI et sont imposés comme les plus-values mobilières : PFU de 31,4 % sur les revenus 2026 ou, sur option, barème progressif. Le gain est en principe constaté quand l''option se dénoue, pas quand la prime est encaissée.'
---

Le covered call (ou « call couvert ») consiste à détenir 100 actions et à vendre une option call sur ces mêmes actions. Vous encaissez une prime tout de suite. En échange, vous vous engagez à vendre vos titres au prix d'exercice si le cours le dépasse à l'échéance. C'est une stratégie neutre à modérément haussière : elle améliore le rendement quand l'action stagne ou monte un peu, mais elle **plafonne vos gains** et ne vous protège à la baisse qu'à hauteur de la prime. Le risque principal reste donc celui de l'action elle-même.

## Comment fonctionne un covered call

Un covered call combine deux positions :

- **Long 100 actions** du sous-jacent (une action ou un ETF comme SPY ou QQQ) ;
- **Short 1 call** sur ce sous-jacent. Sur les marchés américains, un contrat d'options standard sur action ou ETF porte sur 100 titres.

Acheter les actions et vendre le call en même temps s'appelle un *buy-write*. Vendre un call sur des titres que vous détenez déjà s'appelle un *overwrite*. Le résultat économique est le même.

On dit que le call est « couvert » parce que, si l'acheteur exerce, vous livrez des actions que vous possédez déjà. Votre courtier ne demande donc pas de marge supplémentaire pour le call. Si vous voulez revoir les bases, mon article [qu'est-ce qu'une option call](/qu-est-ce-qu-une-option-call/) explique à quoi s'engagent l'acheteur et le vendeur.

Les trois chiffres à connaître avant d'ouvrir la position :

| Indicateur | Formule (par action) |
|---|---|
| Point mort | Prix d'achat de l'action − prime reçue |
| Gain maximal | (Strike − prix d'achat) + prime reçue |
| Perte maximale | Prix d'achat − prime reçue (si l'action tombe à zéro) |

On l'oublie souvent : d'après la parité call-put, un covered call a à peu près le même profil de gain qu'une **vente de put** de même strike et de même échéance. Si vous connaissez déjà le profil d'un [put expliqué avec exemples chiffrés](/option-put-explication-simple/), vous comprenez le risque d'un covered call : vous gagnez une prime limitée et vous subissez presque toute la baisse.

## Exemple chiffré complet

Hypothèses (action fictive XYZ, pas une recommandation) :

- Achat de 100 actions XYZ à **100 $**, soit 10 000 $ investis ;
- Vente d'**1 call XYZ strike 105**, échéance dans **35 jours**, au prix de **1,70 $**, soit **170 $** encaissés ;
- Volatilité implicite supposée : 28 %. Les primes de cet article sont calculées avec le modèle de Black-Scholes, à titre d'illustration. En réalité, vous traitez entre le bid et l'ask, et les primes changent en permanence.

Les chiffres clés :

- **Point mort** : 100 − 1,70 = **98,30 $**
- **Gain maximal** : (105 − 100 + 1,70) × 100 = **670 $**, atteint dès que XYZ termine au-dessus de 105 $
- **Perte maximale** : (100 − 1,70) × 100 = **9 830 $**, si XYZ tombe à zéro

Résultat à l'échéance selon le cours de XYZ (hors frais) :

| Cours de XYZ à l'échéance | Actions seules | Covered call | Différence |
|---|---|---|---|
| 80 $ | −2 000 $ | −1 830 $ | +170 $ |
| 90 $ | −1 000 $ | −830 $ | +170 $ |
| 98,30 $ | −170 $ | 0 $ | +170 $ |
| 100 $ | 0 $ | +170 $ | +170 $ |
| 103 $ | +300 $ | +470 $ | +170 $ |
| 105 $ | +500 $ | +670 $ | +170 $ |
| 115 $ | +1 500 $ | +670 $ | −830 $ |
| 125 $ | +2 500 $ | +670 $ | −1 830 $ |

Ce tableau résume la stratégie. Tant que XYZ reste sous 106,70 $ (105 + 1,70), vous gagnez 170 $ de plus que l'actionnaire « nu ». Au-delà, vous perdez une partie de la hausse. Et à 80 $, la prime ne réduit la perte que de 2 000 $ à 1 830 $.

**Le piège du rendement annualisé.** 170 $ sur 10 000 $ en 35 jours, c'est 1,7 %. Annualisé, on arrive à environ 17,7 % (1,7 % × 365 / 35), et c'est ce chiffre qu'on voit partout. Or il suppose que vous répétez l'opération dix fois par an sans jamais subir de baisse ni être plafonné par une forte hausse. En pratique, je ne regarde jamais ce chiffre seul : je regarde aussi ce que la position perd si l'action recule de 15 %.

## Choisir le strike et l'échéance

### Le strike : un arbitrage entre prime et plafond

Même action à 100 $, même échéance à 35 jours, même volatilité implicite :

| Strike | Prime | Delta du call | Probabilité approx. de finir dans la monnaie* | Gain max | Point mort |
|---|---|---|---|---|---|
| 100 (à la monnaie) | 3,65 $ | 0,53 | ~50 % | 365 $ | 96,35 $ |
| 105 | 1,70 $ | 0,32 | ~29 % | 670 $ | 98,30 $ |
| 110 | 0,68 $ | 0,16 | ~14 % | 1 068 $ | 99,32 $ |

*Probabilité « risque-neutre » tirée du modèle, pas une prévision.

- **Strike à la monnaie** : la prime est la plus élevée et le coussin à la baisse plus épais. Mais vous renoncez à presque toute la hausse et vous serez assigné environ une fois sur deux.
- **Strike hors de la monnaie (delta 0,20 à 0,35)** : c'est le compromis le plus courant chez les vendeurs de prime. Vous gardez une partie de la hausse.
- **Strike très éloigné** : la prime est symbolique et le risque presque inchangé.

Le delta du call vendu indique aussi quelle part de votre exposition vous cédez. Avec 100 actions (delta +100) et un call de delta 0,32 vendu, votre position a un delta net d'environ +68. Pour aller plus loin sur ces indicateurs, voir [les grecques des options : delta, gamma, theta, vega](/grecques-des-options-delta-gamma-theta-vega/).

### L'échéance : theta contre gamma

La valeur temps d'une option fond de plus en plus vite à l'approche de l'échéance (c'est le theta). Les échéances hebdomadaires rapportent donc plus de prime *par jour*. En contrepartie, leur gamma est élevé : un mouvement de quelques pourcents peut faire passer le call de nettement hors de la monnaie à dans la monnaie en une seule séance. Elles demandent aussi plus de suivi et coûtent plus en frais.

En pratique, je travaille le plus souvent entre **30 et 45 jours**. C'est une habitude répandue, pas une règle : le theta est correct et je n'ai pas besoin de surveiller la position tous les jours.

## Gérer la position : expiration, rachat, roll, assignation

### Le call expire sans valeur

Si XYZ termine sous 105 $, le call expire. Vous gardez les 170 $ et les actions, et vous pouvez vendre un nouveau call.

### Racheter le call avant l'échéance

Si le call ne vaut plus que 0,40 $ à 15 jours de l'échéance, le racheter (40 $) vous assure 130 $ de gain et libère les actions. Une fois l'essentiel de la prime encaissé, ce qui reste à gagner vaut rarement le risque.

### Rouler le call : un exemple chiffré

XYZ monte à **108 $** à 10 jours de l'échéance. Le call 105 vaut environ **3,91 $** (3 $ de valeur intrinsèque + 0,91 $ de valeur temps). Pour garder les actions, vous pouvez « rouler » : racheter le call 105 et vendre un call de strike plus élevé et d'échéance plus lointaine, par exemple le **110 à 45 jours pour environ 3,57 $**.

- Débit du roll : 3,91 − 3,57 = **0,34 $** par action (34 $)
- Prime nette cumulée : 1,70 − 3,91 + 3,57 = **1,36 $**
- Nouveau gain maximal si assignation à 110 : (110 − 100 + 1,36) × 100 = **1 136 $**
- Nouveau point mort : 100 − 1,36 = **98,64 $**

Le roll n'est ni gratuit ni magique : vous payez pour relever le plafond, et vous restez exposé à une baisse 45 jours de plus. C'est une **nouvelle décision**, à juger comme si vous ouvriez la position aujourd'hui.

### L'assignation

Si le call termine dans la monnaie, attendez-vous à être assigné : vos 100 actions sont vendues au strike et vous gardez la prime. Quelques points pratiques :

- Les options sur actions et ETF américains sont de **style américain** : elles peuvent être exercées à tout moment avant l'échéance, pas seulement le dernier jour.
- Un call qui clôture un peu hors de la monnaie le jour de l'échéance peut quand même être exercé si le titre bouge après la clôture, car le détenteur dispose encore d'un court délai pour exercer. Si vous tenez à vos actions, rachetez le call avant la clôture au lieu de parier sur quelques cents.
- L'assignation entraîne la **vente** de vos actions. Vous réalisez donc une plus-value ou une moins-value, avec les conséquences fiscales qui vont avec.

## Dividendes et assignation anticipée

C'est le piège classique sur les titres qui versent un dividende, **y compris SPY et QQQ**. Le détenteur d'un call ne touche pas le dividende ; l'actionnaire, si. Quand le call est profondément dans la monnaie et que sa **valeur temps restante est inférieure au dividende**, l'acheteur a intérêt à exercer la veille du détachement pour toucher le dividende.

Exemple : XYZ cote 112 $ la veille du détachement d'un dividende de 0,50 $. Votre call 105 vaut 7,20 $ : 7 $ de valeur intrinsèque et seulement 0,20 $ de valeur temps. L'acheteur a intérêt à exercer. Vos actions partent au strike la veille du détachement et vous **ne touchez pas le dividende**.

Ce que je fais : je regarde la date de détachement avant d'ouvrir la position. Si le call est profondément dans la monnaie à l'approche de cette date, je le roule ou je le rachète.

Et le SPX ? Ses options sont de style européen et réglées en espèces, donc pas d'assignation anticipée. En revanche, on ne peut pas les « couvrir » avec des actions. Pour la plupart des courtiers, vendre des calls SPX contre un portefeuille d'ETF S&P 500 revient à vendre des calls à découvert, avec les exigences de marge correspondantes. Pour un vrai covered call, les particuliers utilisent SPY, QQQ ou des actions.

## Covered call manuel ou indice « buy-write » : ce que disent les données

Cboe calcule le **BXM** (Cboe S&P 500 BuyWrite Index), lancé en 2002. Cet indice mesure la performance théorique d'un portefeuille S&P 500 sur lequel on vend chaque mois un call S&P 500 proche de la monnaie, en général le troisième vendredi du mois. Une étude d'Ibbotson Associates publiée par Cboe décrit le profil attendu : la stratégie buy-write devrait **faire mieux que les actions en marché baissier et moins bien en marché haussier**. D'après Cboe, sa volatilité est aussi plus faible. Ces indices ne tiennent compte ni des frais de transaction ni des impôts.

Le covered call n'est donc pas une machine à battre le marché : il échange une partie de la hausse contre un revenu régulier et une volatilité un peu plus faible.

Il existe aussi des ETF qui appliquent cette stratégie automatiquement. Attention : la plupart des ETF domiciliés aux États-Unis ne sont en général pas accessibles aux particuliers de l'Union européenne, faute de document d'informations clés (DIC/KID). Des équivalents UCITS existent, mais vérifiez leur méthode et leurs frais.

## Risques et erreurs fréquentes

1. **Croire que la prime protège.** Dans notre exemple, elle couvre 1,7 % de baisse. Si l'action perd 30 %, le covered call perd environ 28 %.
2. **Vendre un call sous son prix de revient après une chute** pour « récupérer » de la prime. Si l'action rebondit fortement, vous êtes assigné à perte, alors que ce rebond aurait pu vous ramener à l'équilibre.
3. **Faire un covered call sur une action qu'on ne veut surtout pas vendre.** Si l'assignation vous est insupportable, pour des raisons fiscales ou personnelles, cette stratégie n'est pas faite pour vous.
4. **Ignorer les résultats et les dividendes.** Avant une publication de résultats, la volatilité implicite gonfle les primes. Mais une prime élevée reflète le risque d'un gap, à la hausse comme à la baisse.
5. **Raisonner en rendement annualisé** au lieu de regarder les scénarios de perte.
6. **Passer des ordres au marché** sur une option peu liquide. Utilisez des ordres à cours limité, vers le milieu de la fourchette.
7. **Sous-estimer la taille.** 100 actions d'un titre à 400 $, c'est 40 000 $ sur une seule ligne. Le covered call pousse à la concentration.
8. **Oublier le risque de change.** Pour un investisseur en euros, en francs suisses ou en dollars canadiens, les variations du dollar américain s'ajoutent au résultat, dans un sens comme dans l'autre.

## Fiscalité : ce qu'il faut savoir (France et ailleurs)

**Pour un résident fiscal français** qui opère à titre occasionnel sur un compte-titres ordinaire (les options ne sont pas éligibles au PEA) :

- Les profits sur options relèvent de l'**article 150 ter du CGI** et sont imposés comme les plus-values mobilières.
- Depuis le 1er janvier 2026, la CSG est passée de 9,2 % à 10,6 %, ce qui porte le **PFU à 31,4 %** (12,8 % d'impôt sur le revenu + 18,6 % de prélèvements sociaux) pour les revenus 2026, déclarés en 2027. Vous pouvez toujours opter pour le barème progressif, mais cette option vaut pour l'ensemble de vos revenus du capital.
- Le gain est en principe constaté quand l'option se **dénoue** (expiration, rachat, exercice), et non quand la prime est encaissée. Un call vendu en décembre 2026 qui expire en janvier 2027 relève donc a priori des revenus 2027.
- En cas d'**assignation**, la vente des actions est une cession de titres classique. Le traitement de la prime (intégrée au prix de cession ou imposée à part) suit des règles précises : vérifiez-les dans le BOFiP ou auprès d'un conseiller avant de déclarer.
- Les **dividendes américains** subissent une retenue à la source, en principe de 15 % si vous avez rempli le formulaire W-8BEN. Cette retenue est imputable sur l'impôt français selon la convention fiscale.
- Une activité habituelle et intensive peut être requalifiée dans une autre catégorie de revenus (BNC notamment).

**Belgique, Suisse, Québec** : les règles sont différentes (notion de gestion normale du patrimoine privé, distinction entre revenu et gain en capital, etc.) et l'imposition des primes d'options dépend de votre situation. Je ne m'avance pas : consultez un fiscaliste local.

## En pratique : ma check-list avant de vendre un covered call

- Je suis prêt à vendre ces actions au strike choisi, prime incluse.
- J'ai calculé le point mort, le gain maximal et la perte si l'action recule de 15 à 20 %.
- Aucune publication de résultats n'a lieu avant l'échéance, ou alors j'accepte ce risque en connaissance de cause.
- J'ai noté la date de détachement du dividende.
- Je ne vends pas sous mon prix de revient si je ne suis pas prêt à réaliser une perte.
- L'écart bid/ask est raisonnable (0,05 $ sur 1,70 $ de prime, oui ; 0,40 $, non). Je passe un ordre à cours limité pendant la séance américaine : 15h30-22h heure de Paris la plupart de l'année, avec une heure d'écart pendant quelques semaines en mars et à l'automne.
- Je sais à l'avance ce que je ferai si l'action monte fortement (laisser assigner ou rouler) et combien je suis prêt à payer au maximum pour rouler.

Si vous débutez, commencez par une seule ligne, sur un sous-jacent liquide, et suivez une échéance complète avant d'en ouvrir d'autres. Le [guide trading options débutant](/trading-options-debutant/) explique comment organiser cet apprentissage.

*Cet article est fourni à titre éducatif et ne constitue pas un conseil en investissement. Les options comportent un risque de perte important. Les exemples utilisent un titre fictif et des primes théoriques.*

## Sources

- [Options Industry Council (OCC) – Covered Call (Buy/Write)](https://www.optionseducation.org/strategies/all-strategies/covered-call-buy-write)
- [Cboe – Cboe BuyWrite Indices Methodology (BXM)](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf)
- [Cboe / Ibbotson Associates – Étude sur la stratégie buy-write et l'indice BXM](https://cdn.cboe.com/resources/education/research_publications/IbbotsonAug30final.pdf)
- [Charles Schwab – Options Strategy: The Covered Call](https://www.schwab.com/learn/story/options-strategy-covered-call)
- [Meilleurtaux Placement – Flat tax à 31,4 % : ce qui change depuis janvier 2026](https://placement.meilleurtaux.com/placement-financier/actualites/2026-avril/flat-tax-a-31-4-ce-qui-change-depuis-janvier-2026.html)
