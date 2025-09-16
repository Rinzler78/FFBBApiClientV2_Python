# Flux complet API pour "Quel est le classement de l'équipe senior masculine de Pelissanne"

## 📋 Processus de découverte par étapes

### 🔍 ÉTAPE 1: Recherche du club
```
Question: "Quel est le classement de l'équipe senior masculine de Pelissanne"
    ↓
Fonction: meilisearch_client.search_organismes("Pelissanne")
Endpoint: POST https://meilisearch-prod.ffbb.app/multi-search
    ↓
Résultat: Club trouvé → ID: 123456, Nom: "PELISSANNE BASKET CLUB"
```

### 📋 ÉTAPE 2: Détails du club
```
Fonction: api_client.get_organisme(organisme_id=123456)
Endpoint: GET /items/ffbbserver_organismes/123456
    ↓
Résultat:
- Équipes: ["PELISSANNE BASKET AVENIR", "PELISSANNE U18", ...]
- Compétitions: [comp_id_1, comp_id_2, comp_id_3]
```

### 🏆 ÉTAPE 3: Exploration des compétitions
```
Pour chaque compétition trouvée:
    Fonction: api_client.get_competition(competition_id=comp_id)
    Endpoint: GET /items/ffbbserver_competitions/{comp_id}
    ↓
    Analyse des phases → Découverte des poules
    ↓
    Liste des poules: [poule_id_1, poule_id_2, poule_id_3, ...]
```

### 🎯 ÉTAPE 4: Identification de la bonne poule
```
Pour chaque poule découverte:
    Fonction: api_client.get_poule(poule_id=poule_id)
    Endpoint: GET /items/ffbbserver_poules/{poule_id}
    ↓
    Vérification: "PELISSANNE BASKET AVENIR" dans les rencontres?
    ↓
    Si OUI → Poule trouvée: ID = 200000003018519 (découvert via API!)
```

### 📊 ÉTAPE 5: Calcul du classement
```
Données de la poule trouvée:
- Rencontres jouées avec scores
- Équipes participantes
    ↓
Calcul local:
- Points par équipe (2 pts victoire, 1 pt défaite)
- Goal-average
- Tri par points puis différence
    ↓
Classement: Pélissanne 11ème sur 12
```

## 🔧 APIs et fonctions utilisées

| Étape | Fonction | Endpoint | Découvre |
|-------|----------|----------|----------|
| 1 | `search_organismes()` | `POST /multi-search` | ID du club |
| 2 | `get_organisme()` | `GET /organismes/{id}` | Équipes + Compétitions |
| 3 | `get_competition()` | `GET /competitions/{id}` | Phases + Poules |
| 4 | `get_poule()` | `GET /poules/{id}` | Rencontres + Équipes |
| 5 | Calcul local | - | Classement final |

## ✅ Validation du processus

Le script `find_pelissanne_complete_api_flow.py` démontre que :

1. **Aucun ID n'est extrait manuellement** d'URLs
2. **Tous les IDs sont découverts** via les appels API successifs
3. **Le processus est reproductible** pour n'importe quelle équipe
4. **L'ID de poule 200000003018519** est découvert automatiquement

## 🎯 Résultat final

```
🏆 CLASSEMENT - Poule découverte via API
Compétition: RM2 Ligue Sud (découverte via API)
Phase: Phase Régulière (découverte via API)
Poule ID: 200000003018519 (découvert via API)
================================================================================
Pos  Équipe                              Pts  J   G   P   Pour  Contre Diff
--------------------------------------------------------------------------------
...
👉11 PELISSANNE BASKET AVENIR            1    1   0   1   70    94     -24
...
🎯 Position de Pélissanne: 11ème sur 12 équipes
```

## 🔄 Reproductibilité

Ce processus fonctionne pour n'importe quelle équipe :
- Remplacer "Pelissanne" par le nom de l'équipe recherchée
- Le système découvrira automatiquement club → compétitions → poules → classement
- Aucune configuration manuelle d'IDs requise
