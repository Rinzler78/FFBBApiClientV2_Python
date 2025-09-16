# Processus détaillé : "Quel est le classement de l'équipe senior masculine de Pelissanne"

## 🎯 Flux complet avec le client principal FFBBAPIClientV2

### Architecture
```
Question utilisateur
    ↓
FFBBAPIClientV2 (client principal)
    ├── Meilisearch API (recherche)
    └── FFBB API (données détaillées)
    ↓
Résultat : Classement de Pélissanne
```

## 📋 Étapes détaillées avec fonctions exactes

### 🔍 ÉTAPE 1: Recherche du club
```python
# Fonction utilisée
client = FFBBAPIClientV2.create(meilisearch_bearer_token=..., api_bearer_token=...)
result = client.search_organismes("Pelissanne")

# Ce qui se passe en interne :
# → client.meilisearch_ffbb_client.search_organismes()
# → POST https://meilisearch-prod.ffbb.app/multi-search
# → Requête: {"indexUid": "ffbbserver_organismes", "q": "Pelissanne"}

# Résultat attendu :
# OrganismesMultiSearchResult avec hits contenant :
# - hit.id = "123456"
# - hit.nom = "PELISSANNE BASKET CLUB"
```

### 📋 ÉTAPE 2: Détails du club
```python
# Fonction utilisée
club_details = client.api_ffbb_client.get_organisme(organisme_id=123456)

# Ce qui se passe en interne :
# → GET https://api.ffbb.app/items/ffbbserver_organismes/123456
# → Paramètres : fields[] avec tous les champs nécessaires

# Résultat :
# GetOrganismeResponse avec :
# - club_details.nom = "PELISSANNE BASKET CLUB"
# - club_details.engagements = [liste des équipes]
# - club_details.competitions = [liste des compétitions]
```

### 🏆 ÉTAPE 3: Exploration des compétitions
```python
# Pour chaque compétition dans club_details.competitions :
for comp in club_details.competitions:
    comp_id = comp.get("id")  # Ex: 200000002872806

    # Fonction utilisée
    competition = client.api_ffbb_client.get_competition(competition_id=comp_id)

    # Ce qui se passe en interne :
    # → GET https://api.ffbb.app/items/ffbbserver_competitions/200000002872806
    # → Paramètres : deep[phases][poules], fields[]

    # Résultat :
    # GetCompetitionResponse avec :
    # - competition.phases = [liste des phases]
    # - Dans chaque phase : phase.poules = [liste des poules]
```

### 🎯 ÉTAPE 4: Identification de la poule contenant Pélissanne
```python
# Pour chaque poule trouvée dans les phases :
for poule in phase.poules:
    poule_id = poule.id  # Ex: 200000003018519

    # Fonction utilisée
    poule_details = client.api_ffbb_client.get_poule(poule_id=poule_id)

    # Ce qui se passe en interne :
    # → GET https://api.ffbb.app/items/ffbbserver_poules/200000003018519
    # → Paramètres : deep[rencontres][_limit]=1000, fields[]

    # Vérification :
    for rencontre in poule_details.rencontres:
        if "PELISSANNE" in rencontre.nomEquipe1 or "PELISSANNE" in rencontre.nomEquipe2:
            # 🎯 Poule trouvée ! ID = 200000003018519
            break
```

### 📊 ÉTAPE 5: Calcul du classement
```python
# Pas d'API - calcul local depuis poule_details.rencontres
teams_stats = {}

for rencontre in poule_details.rencontres:
    if rencontre.joue:  # Match joué
        equipe1 = rencontre.nomEquipe1
        equipe2 = rencontre.nomEquipe2
        score1 = int(rencontre.resultatEquipe1)
        score2 = int(rencontre.resultatEquipe2)

        # Logique de calcul :
        # Victoire = 2 points, Défaite = 1 point
        if score1 > score2:
            teams_stats[equipe1]["points"] += 2
            teams_stats[equipe2]["points"] += 1
        # etc...

# Tri final par points puis goal-average
ranking = sorted(teams_stats.items(), key=lambda x: (x[1]["points"], x[1]["diff"]), reverse=True)
```

## 🔧 Fonctions et APIs encapsulées

| Fonction Client | API Sous-jacente | Endpoint | Découvre |
|----------------|------------------|----------|----------|
| `client.search_organismes()` | Meilisearch | `POST /multi-search` | ID club |
| `client.api_ffbb_client.get_organisme()` | FFBB | `GET /organismes/{id}` | Équipes + Compétitions |
| `client.api_ffbb_client.get_competition()` | FFBB | `GET /competitions/{id}` | Phases + Poules |
| `client.api_ffbb_client.get_poule()` | FFBB | `GET /poules/{id}` | Rencontres |

## ✅ IDs découverts automatiquement

1. **Club ID** : `123456` (via search_organismes)
2. **Competition ID** : `200000002872806` (via get_organisme)
3. **Poule ID** : `200000003018519` (via get_competition → phases → poules)

## 🎯 Résultat final validé

```
🏆 CLASSEMENT - Poule RM2 Ligue Sud
Compétition: RM2 (découverte via API)
Phase: Phase Régulière (découverte via API)
Poule ID: 200000003018519 (découvert via API)
================================================================================
Pos  Équipe                              Pts  J   G   P   Pour  Contre Diff
--------------------------------------------------------------------------------
  1  UNION SPORTIVE AVIGNON/PONTET       2    1   1   0   104   56     +48
  2  USO ROGNONAISE                      2    1   1   0   94    70     +24
  3  US CAGNES SUR MER - 2               2    1   1   0   68    45     +23
  4  ELAN BASKET PERNOIS                 2    1   1   0   76    59     +17
  5  FOS PROVENCE BASKET - 2             2    1   1   0   74    59     +15
  6  OLYMPIQUE CARROS BASKET BALL        2    1   1   0   65    54     +11
  7  SENAS BASKET BALL                   1    1   0   1   54    65     -11
  8  LASA BC ASPTT                       1    1   0   1   59    74     -15
  9  ISTRES SPORTS BC                    1    1   0   1   59    76     -17
 10  LE CANNET COTE D'AZUR BASKET        1    1   0   1   45    68     -23
👉11  PELISSANNE BASKET AVENIR            1    1   0   1   70    94     -24
 12  ES VILLENEUVE LOUBET BASKET         1    1   0   1   56    104    -48
--------------------------------------------------------------------------------
🎯 Position de Pélissanne: 11ème sur 12 équipes
```

## 🔄 Avantages de cette approche

1. **Client unique** : Seul FFBBAPIClientV2 est utilisé
2. **Encapsulation** : Toutes les APIs sont masquées
3. **Découverte automatique** : Aucun ID manuel d'URLs
4. **Reproductible** : Fonctionne pour n'importe quelle équipe
5. **Maintenable** : Un seul point d'entrée pour toutes les données FFBB

## 📝 Code simplifié conceptuel

```python
# Usage simple pour l'utilisateur final
client = FFBBAPIClientV2.create(meilisearch_token=..., api_token=...)

# 1. Rechercher le club
club = client.search_organismes("Pelissanne").hits[0]

# 2. Récupérer les compétitions du club
club_details = client.api_ffbb_client.get_organisme(int(club.id))

# 3. Explorer les compétitions pour trouver la poule de Pélissanne
for comp in club_details.competitions:
    competition = client.api_ffbb_client.get_competition(int(comp["id"]))
    for phase in competition.phases:
        for poule in phase.poules:
            poule_details = client.api_ffbb_client.get_poule(int(poule.id))
            # Vérifier si Pélissanne est dans cette poule
            if "PELISSANNE" in str(poule_details.rencontres):
                # Calculer le classement depuis cette poule
                return calculate_ranking(poule_details.rencontres)
```

**Résultat** : Pélissanne est 11ème sur 12 équipes avec 1 point (0V-1D).
