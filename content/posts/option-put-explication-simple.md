---
title: 'Option put : explication simple avec exemples chiffrés'
description: 'Option put, explication simple : droit de vendre, prime, strike, point mort. Exemples chiffrés en dollars, achat vs vente de put et risques à connaître.'
keyword: option put explication simple
slug: option-put-explication-simple
date: '2026-10-20'
updated: '2026-10-20'
tags:
- options
- put
- débutant
- vente de prime
faq:
- q: Quelle est la différence entre acheter et vendre un put ?
  a: Acheter un put vous donne le droit de vendre le sous-jacent au strike. Vous payez une prime et gagnez si le cours baisse sous le point mort. Vendre un put vous oblige à acheter 100 actions au strike si l'option est exercée. Vous encaissez la prime, mais une forte baisse peut vous coûter cher.
- q: Peut-on perdre plus que la prime avec une option put ?
  a: 'Si vous achetez le put, non : votre perte maximale est la prime payée, plus les frais. Si vous le vendez, oui : la perte peut atteindre (strike − prime) × 100 par contrat si l''action tombe à zéro. C''est pour ça qu''on utilise des spreads à risque défini.'
- q: Faut-il posséder l'action pour acheter un put ?
  a: 'Non. On peut acheter un put pour parier sur une baisse sans détenir le titre. Si vous détenez déjà les actions, le put sert d''assurance contre la baisse : c''est le « protective put ».'
- q: Que se passe-t-il à l'échéance si mon put est dans la monnaie ?
  a: En général, un put dans la monnaie d'au moins 0,01 $ est exercé automatiquement. Sur une action ou un ETF, cela revient à vendre 100 titres au strike. Sur le SPX, le règlement se fait en espèces. Si vous ne voulez pas d'exercice, revendez le put avant la clôture et vérifiez la politique de votre courtier.
- q: Pourquoi mon put perd-il de la valeur alors que l'action baisse ?
  a: La prime contient de la valeur temps, qui fond chaque jour. Elle baisse aussi quand la volatilité implicite diminue. Si la baisse est trop faible ou trop lente, ces deux effets peuvent l'emporter sur le gain de valeur intrinsèque.
---

Une option put, c'est le droit (mais pas l'obligation) de vendre un actif à un prix fixé d'avance, le strike, jusqu'à une date donnée. Ce droit se paie : c'est la prime. Si vous achetez un put, vous gagnez quand le cours baisse nettement sous le strike, et vous ne pouvez pas perdre plus que la prime payée. Si vous vendez un put, c'est l'inverse : vous encaissez la prime, mais vous vous engagez à acheter 100 actions au strike si on vous le demande, et ce risque peut être lourd.

Une analogie qui marche bien : le put fonctionne comme une assurance contre la baisse. La prime, c'est la cotisation. Le strike, c'est le niveau à partir duquel vous êtes couvert. L'échéance, c'est la fin du contrat. L'acheteur du put est l'assuré, le vendeur est l'assureur.

## Les mots à connaître avant tout

Cinq notions suffisent pour lire une chaîne d'options chez votre courtier :

- **Sous-jacent** : l'actif sur lequel porte l'option. Ce peut être une action, un ETF comme SPY ou QQQ, ou un indice comme le SPX.
- **Strike (prix d'exercice)** : le prix auquel le détenteur du put peut vendre le sous-jacent.
- **Prime** : le prix de l'option. Elle est affichée **par action**.
- **Échéance** : la date après laquelle l'option n'existe plus.
- **Multiplicateur** : un contrat d'options sur actions US porte en général sur 100 actions. Comme la prime est affichée par action, un put coté 2,50 $ coûte 250 $ par contrat, hors frais.

On classe aussi les puts selon la position du cours par rapport au strike :

- **Dans la monnaie** : le cours du sous-jacent est inférieur au strike.
- **À la monnaie** : le cours est égal au strike.
- **Hors de la monnaie** : le cours est au-dessus du strike.

C'est l'inverse du call. Si vous avez lu notre article sur [l'option call et son fonctionnement](/qu-est-ce-qu-une-option-call/), il suffit d'inverser le sens.

## Exemple chiffré : acheter un put, pas à pas

Prenons une action fictive, XYZ, qui cote 100 $. Les chiffres sont illustratifs : ce ne sont pas des cotations réelles. La logique, elle, est exactement celle que vous retrouverez sur votre plateforme.

- Achat de 1 put XYZ, strike 95 $, échéance dans 45 jours
- Prime : 2,50 $ par action, soit **250 $ par contrat** (plus les commissions)

Voici les trois chiffres à calculer avant de cliquer :

- **Perte maximale** : 250 $, soit la prime payée. Vous la subissez si XYZ termine au-dessus de 95 $ à l'échéance.
- **Point mort à l'échéance** : strike − prime = 95 − 2,50 = **92,50 $**.
- **Gain maximal** : (95 − 2,50) × 100 = **9 250 $**, dans le cas théorique où XYZ tombe à 0.

Résultat à l'échéance selon le cours de XYZ :

| Cours de XYZ à l'échéance | Valeur du put (par action) | Résultat net par contrat |
|---|---|---|
| 110 $ | 0 $ | −250 $ |
| 100 $ | 0 $ | −250 $ |
| 95 $ | 0 $ | −250 $ |
| 94 $ | 1 $ | −150 $ |
| 92,50 $ | 2,50 $ | 0 $ |
| 90 $ | 5 $ | +250 $ |
| 85 $ | 10 $ | +750 $ |
| 75 $ | 20 $ | +1 750 $ |

La formule générale : résultat = max(0 ; strike − cours) × 100 − prime payée.

Beaucoup de débutants l'oublient : **une baisse ne suffit pas**. Si XYZ passe de 100 $ à 94 $ (−6 %), vous perdez quand même 150 $ à l'échéance. Pour gagner, il faut que le cours passe sous le point mort.

### Avant l'échéance : valeur intrinsèque et valeur temps

En pratique, on garde rarement un put acheté jusqu'à l'échéance : on le revend sur le marché. Son prix se décompose en deux parties :

- **Valeur intrinsèque** = max(0 ; strike − cours). Avec XYZ à 93 $, elle vaut 2 $ pour le put 95.
- **Valeur temps** = le reste du prix. Elle dépend du temps restant et de la volatilité implicite, et elle fond à mesure que l'échéance approche.

Exemple illustratif : 30 jours après l'achat, XYZ cote 93 $. Le put 95 pourrait valoir autour de 3,20 $ : 2 $ de valeur intrinsèque et environ 1,20 $ de valeur temps. Si vous le revendez, vous encaissez 320 $, soit un gain de 70 $ avant frais. L'action a perdu 7 % et vous ne gagnez que 70 $ : la prime payée et le temps qui passe jouent contre vous. Le chiffre exact dépend de la volatilité implicite du moment, d'où le « autour de ».

## L'autre côté du contrat : vendre un put

Chaque put acheté a un vendeur en face. Si l'acheteur exerce son droit, le vendeur est obligé d'acheter le sous-jacent au strike.

Reprenons le même put, côté vendeur :

- Vente de 1 put XYZ strike 95 $ à 2,50 $ : vous **encaissez 250 $**.
- **Gain maximal** : 250 $, si XYZ reste au-dessus de 95 $ jusqu'à l'échéance.
- **Point mort** : 92,50 $, le même que pour l'acheteur, puisque les deux positions sont exactement opposées.
- **Perte maximale** : (95 − 2,50) × 100 = **9 250 $** si XYZ tombe à 0.

Si le put est exercé, vous achetez 100 XYZ à 95 $, soit 9 500 $ à débourser. Grâce à la prime encaissée, ces actions vous reviennent en réalité à 92,50 $.

Deux cas de figure :

- **Vous gardez ces 9 500 $ en liquidités sur votre compte.** On parle alors de « cash-secured put » (put garanti par des liquidités).
- **Vous vendez le put sur un compte sur marge sans avoir cette somme.** Le courtier ne bloque qu'une fraction en garantie. Vous avez donc un effet de levier, et c'est là que la position devient dangereuse.

Le point clé est le déséquilibre : **250 $ de gain possible contre plusieurs milliers de dollars de perte possible**. Vendre un put peut être cohérent si vous acceptez vraiment d'acheter l'action à ce prix. Ce n'est en aucun cas un « revenu passif » sans risque.

### La version à risque défini : le put credit spread

C'est la structure que j'utilise le plus comme vendeur de prime pour limiter ce risque. On vend un put et on achète en même temps un put de strike inférieur, sur la même échéance :

- Vente put 95 à 2,50 $ et achat put 90 à 1,00 $ (chiffres illustratifs)
- **Crédit net** : 1,50 $, soit 150 $ encaissés. C'est le gain maximal.
- **Perte maximale** : (95 − 90 − 1,50) × 100 = **350 $**
- **Point mort** : 95 − 1,50 = **93,50 $**

Vous gagnez moins qu'avec le put vendu seul, mais votre perte est plafonnée, même en cas de krach. En général, le courtier bloque en garantie un montant égal à la perte maximale. Pour monter une première position de ce type sans vous brûler, voyez notre [guide concret du trading d'options pour débutant](/trading-options-debutant/).

## Les 4 positions de base comparées

| Position | Anticipation | Gain maximal | Perte maximale | Point mort |
|---|---|---|---|---|
| Acheter un put | Forte baisse | Strike − prime (si le cours tombe à 0) | Prime payée | Strike − prime |
| Vendre un put | Stabilité ou hausse | Prime encaissée | Strike − prime (si le cours tombe à 0) | Strike − prime |
| Acheter un call | Forte hausse | Illimité | Prime payée | Strike + prime |
| Vendre un call sans détenir les actions | Stabilité ou baisse | Prime encaissée | Illimitée | Strike + prime |

Les montants sont par action : multipliez par 100 pour un contrat standard.

## À quoi sert un put en pratique ?

### 1. Parier sur une baisse avec un risque plafonné

Si vous anticipez la baisse d'une action, vous pouvez acheter un put au lieu de la vendre à découvert. À découvert, la perte potentielle n'a pas de plafond, puisque le cours peut monter sans limite. Avec un put acheté, vous ne pouvez pas perdre plus que la prime. La contrepartie : le put expire à une date fixe. Il faut donc avoir raison sur l'ampleur de la baisse **et** sur le moment où elle arrive.

### 2. Protéger des actions que vous détenez (protective put)

Vous détenez 100 XYZ achetées à 100 $ et vous achetez un put 95 à 2,50 $ (250 $) :

- **Si XYZ chute à 70 $** : −3 000 $ sur les actions, +2 500 $ de valeur intrinsèque sur le put et −250 $ de prime. Vous perdez **750 $** au total au lieu de 3 000 $.
- **Perte maximale garantie jusqu'à l'échéance** : (100 − 95) + 2,50 = 7,50 $ par action, soit **750 $**.
- **Si XYZ monte à 120 $** : +2 000 $ − 250 $ = **+1 750 $**. La protection vous a coûté 250 $.

Racheter cette protection tous les mois revient cher sur une année. C'est une assurance à prendre ponctuellement, pas un réflexe permanent.

### 3. Vendre de la prime ou viser un prix d'achat

Vendre un put sur un titre que vous acceptez de détenir, c'est un peu comme être payé pour placer un ordre d'achat sous le cours actuel. Gardez simplement en tête le scénario de krach décrit plus haut.

## Américain ou européen : la différence qui compte sur SPY, QQQ et SPX

- **Options sur actions US et sur ETF (SPY, QQQ)** : elles sont de style américain. Elles s'exercent à tout moment jusqu'à l'échéance, avec livraison de 100 titres par contrat. Un vendeur de put peut donc être assigné, c'est-à-dire obligé d'acheter les titres, avant l'échéance. C'est surtout le cas quand le put est profondément dans la monnaie.
- **Options sur l'indice SPX** : elles sont de style européen. Elles ne s'exercent qu'à l'échéance et sont réglées en espèces, sans livraison de titres : le vendeur assigné paie la différence en cash. Le multiplicateur est de 100 $ par point d'indice, ce qui donne des montants élevés. Vérifiez les spécifications à jour sur le site de Cboe avant de trader.

Quand une option est exercée, l'OCC (l'organisme de compensation des options américaines) attribue l'exercice à un courtier membre qui a des positions vendeuses sur cette option. Le courtier le répercute ensuite à l'un de ses clients vendeurs, selon ses propres règles. Vous ne choisissez pas d'être assigné. À l'échéance, les options dans la monnaie d'au moins 0,01 $ sont en général exercées automatiquement. Vérifiez la politique exacte de votre courtier.

**Note horaire pour fin octobre 2026** : l'Europe passe à l'heure d'hiver le dimanche 25 octobre, les États-Unis seulement le dimanche 1er novembre. Du 26 au 30 octobre, la séance américaine (9h30-16h00, heure de New York) ouvre donc à 14h30 au lieu de 15h30 à Paris, Bruxelles ou Genève. Au Québec, rien ne change.

## Risques et erreurs fréquentes

1. **Confondre acheter et vendre un put.** Les deux misent sur des scénarios opposés et n'ont pas du tout le même risque. Relisez toujours le sens de l'ordre (« Buy to Open » ou « Sell to Open ») avant de valider.
2. **Oublier le multiplicateur.** Une prime de 2,50 $ représente 250 $ de dépense. Un put vendu au strike 95 vous engage à payer 9 500 $.
3. **Croire qu'avoir raison sur la direction suffit.** On l'a vu, une baisse de 6 % peut rester perdante. Et la valeur temps de votre put diminue chaque jour.
4. **Acheter des puts quand la peur est déjà au maximum.** Après une forte baisse, la volatilité implicite grimpe et les puts deviennent chers. Si le marché se calme, leur prix peut chuter même si le cours ne remonte pas. Sur les indices, les puts hors de la monnaie sont d'ailleurs toujours plus chers que les calls situés à la même distance du cours (c'est ce qu'on appelle le « skew »).
5. **Vendre des puts sans protection avec trop de levier.** Si l'action ouvre en forte baisse, vous n'avez pas le temps de réagir. Sur un compte sur marge, un manque de garantie peut entraîner une liquidation automatique par le courtier (c'est le cas chez Interactive Brokers), au pire moment.
6. **Négliger la liquidité.** Sur des options peu échangées, l'écart entre le prix acheteur et le prix vendeur peut absorber une bonne partie du gain. Utilisez des ordres à cours limité, jamais des ordres au marché.
7. **Ignorer le risque de change et la fiscalité.** Vos gains et pertes sont en dollars, puis convertis en EUR, CHF ou CAD. La fiscalité des options varie fortement entre la France, la Belgique, la Suisse et le Québec, et selon votre statut. Renseignez-vous auprès de l'administration fiscale de votre pays ou d'un conseiller. Si vous êtes résident fiscal français, un compte ouvert chez un courtier étranger doit en plus être déclaré chaque année (formulaire 3916).

Dernier point réglementaire : aux États-Unis, les courtiers doivent remettre à leurs clients le document de l'OCC *Characteristics and Risks of Standardized Options*. Il faut l'avoir lu avant de trader des options. Il est long, mais les chapitres sur les risques valent la lecture.

## Ce que je vérifie avant toute position sur un put

- Mon scénario (baisse, protection ou vente de prime) correspond-il bien au sens du contrat, achat ou vente ?
- Ai-je calculé la perte maximale **en dollars**, multiplicateur inclus ? Puis-je l'encaisser sans stress ?
- Le point mort est-il atteignable d'ici l'échéance ?
- La volatilité implicite est-elle élevée ou basse par rapport à ses niveaux récents ?
- Y a-t-il un événement avant l'échéance : résultats de l'entreprise, réunion de la Fed, chiffres d'inflation ?
- Option américaine ou européenne : quel risque d'assignation, et ai-je de quoi acheter les titres si on me les livre ?

Rien dans cet article ne constitue un conseil en investissement. Les options sont des produits complexes qui peuvent entraîner des pertes rapides et importantes. Commencez petit, avec des positions à risque défini.

## Sources

- [OCC – Characteristics and Risks of Standardized Options (page officielle)](https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document)
- [OCC – Characteristics and Risks of Standardized Options, version juin 2024 (PDF)](https://www.theocc.com/getcontentasset/a151a9ae-d784-4a15-bdeb-23a029f50b70/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/riskstoc.pdf)
- [Charles Schwab – Basic Call and Put Options Strategies](https://www.schwab.com/learn/story/basic-call-and-put-options-strategies)
- [Saxo – How put options work](https://www.home.saxo/learn/guides/options/how-put-options-work)
