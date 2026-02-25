# Architecture API FFBB v2

## Vue d'ensemble

Le client FFBB v2 est compose de 3 couches :

```
┌──────────────────────────────────────────────────┐
│             FFBBAPIClientV2 (Facade)             │
│   69 methodes publiques — point d'entree unique  │
├────────────────────┬─────────────────────────────┤
│  ApiFFBBAppClient  │   MeilisearchFFBBClient     │
│  (Directus REST)   │   (Meilisearch Search)      │
│  get/list + FK     │   search + objets inline     │
│  bruts (int IDs)   │   denormalises               │
├────────────────────┴─────────────────────────────┤
│               API FFBB (serveur)                 │
│        Directus CMS + Meilisearch engine         │
└──────────────────────────────────────────────────┘
```

### Repartition des 69 methodes

| Categorie | Nombre | Exemples |
|-----------|--------|----------|
| get (single item) | 13 | `get_organisme`, `get_competition`, `get_poule` |
| list (paginated) | 10 | `list_rencontres`, `list_communes`, `list_entraineurs` |
| list_all (auto-paginated) | 10 | `list_all_salles`, `list_all_engagements` |
| search (Meilisearch) | 9 | `search_organismes`, `search_competitions` |
| search_multiple (batch) | 9 | `search_multiple_organismes`, `search_multiple_rencontres` |
| search_geo | 4 | `search_organismes_by_geo`, `search_engagements_filtered` |
| composite | 2 | `get_engagement_contacts`, `get_club_contacts` |
| batch helpers | 5 | `list_engagements_by_ids`, `list_rencontres_by_poules` |
| settings | 4 | `get_index_settings`, `get_filterable_attributes` |
| factory + asset | 2 | `create()`, `get_asset_url` |

---

## Directus REST — Pattern Fields et FK

### Principe

Les `*_fields.py` controlent la morphologie de la reponse Directus via le
parametre `fields[]` :

- **FK-only** (`"commune"`, `"salle"`, `"entraineur"`) : pas de dot notation
  → retourne un **int ID brut** → doit etre resolu par un appel facade
- **Embedded** (`"cartographie.*"`, `"categorie.*"`, `"membres.*"`) : dot notation
  → Directus expanse l'objet inline → deja present dans la reponse
- **Embedded hybride** (`"phases.*"`, `"classements.*"`) : objet expanse
  contenant des FK implicites vers d'autres entites

### FK par endpoint

#### GetOrganismeResponse (`get_organisme`)

| Champ | Type | Resolution |
|-------|------|------------|
| `commune` | int | `list_communes(filter={"id":{"_eq":N}})` |
| `salle` | int | `get_salle(id)` |
| `saison` | int | `get_saisons()` |
| `organisme_id_pere` | int | `get_organisme(id)` (recursif) |
| `engagements` | list[int] | `list_engagements_by_ids(ids)` |
| `competitions` | list[int] | `get_competition(id)` par item |
| `organismes_fils` | list[int] | `get_organisme(id)` par item |
| `logo` | UUID | `get_asset_url(uuid)` |
| *cartographie* | Cartographie | EMBEDDED |
| *membres* | list[Membre] | EMBEDDED |
| *offres_pratiques* | list[OffrePratique] | EMBEDDED |
| *labellisation* | list[LabellisationItem] | EMBEDDED |

#### GetCompetitionResponse (`get_competition`)

| Champ | Type | Resolution |
|-------|------|------------|
| `saison` | int | `get_saisons()` |
| `competition_origine` | int | `get_competition(id)` (recursif) |
| `idCompetitionPere` | int | `get_competition(id)` (recursif) |
| `organisateur` | int | `get_organisme(id)` |
| `logo` | UUID | `get_asset_url(uuid)` |
| `poules` | list[int] | `get_poule(id)` par item |
| *categorie* | Categorie | EMBEDDED |
| *phases* | list[CompetitionPhase] | EMBEDDED HYBRIDE (contient FK implicites) |

#### GetPouleResponse (`get_poule`)

| Champ | Type | Resolution |
|-------|------|------------|
| `id_competition` | int | `get_competition(id)` |
| `rencontres` | list[int] | `list_rencontres_by_poule(id)` |
| `engagements` | list[int] | `list_engagements_by_poule(id)` |
| *classements* | list[TeamRanking] | EMBEDDED HYBRIDE |

#### GetEngagementsResponse (`get_engagement`)

| Champ | Type | Resolution |
|-------|------|------------|
| `idCompetition` | int | `get_competition(id)` |
| `idOrganisme` | int | `get_organisme(id)` |
| `idOrganismeCtc` | int | `get_organisme(id)` |
| `idPoule` | int | `get_poule(id)` |
| `entraineur` | int | `get_entraineur(id)` |
| `entraineurAdjoint` | int | `get_entraineur(id)` |
| `logo`, `photo`, `logo_genius` | UUID | `get_asset_url(uuid)` |
| `rencontres_domiciles` | list[int] | `get_rencontre(id)` |
| `rencontres_exterieur` | list[int] | `get_rencontre(id)` |
| *niveau* | Categorie | EMBEDDED |
| *positions* | list[EngagementPosition] | EMBEDDED |

#### GetRencontresResponse (`get_rencontre`)

| Champ | Type | Resolution |
|-------|------|------------|
| `competitionId` | int | `get_competition(id)` |
| `idEngagementEquipe1` | int | `get_engagement(id)` |
| `idEngagementEquipe2` | int | `get_engagement(id)` |
| `idOrganismeEquipe1` | int | `get_organisme(id)` |
| `idOrganismeEquipe2` | int | `get_organisme(id)` |
| `idPoule` | int | `get_poule(id)` |
| `saison` | int | `get_saisons()` |
| `salle` | int | `get_salle(id)` |

*100% FK-only — pas d'embedded hybride.*

#### Endpoints feuilles

| Endpoint | FK | Embedded |
|----------|-----|----------|
| `get_salle` | commune (int) | cartographie |
| `get_terrain` | commune (int) | natureSol, cartographie |
| `get_tournoi` | commune (int) | cartographie, document_flyer |
| `get_entraineur` | commune (int) | — |
| `get_formation` | image (UUID) | domain, theme |
| `get_lives` | match_id (int) | clock, external_id, team_engagements |

---

## Meilisearch — Index et Objets Denormalises

### 9 index disponibles

| Index UID | Hits type | Attributs filtrable cles |
|-----------|-----------|--------------------------|
| `ffbbserver_organismes` | OrganismesMultiSearchResult | commune.*, salle.*, _geo, type |
| `ffbbserver_competitions` | CompetitionsMultiSearchResult | categorie.*, sexe, saison.* |
| `ffbbserver_rencontres` | RencontresMultiSearchResult | competitionId.*, joue, saison.* |
| `ffbbserver_salles` | SallesMultiSearchResult | commune.*, _geo |
| `ffbbserver_terrains` | TerrainsMultiSearchResult | commune.*, natureSol.*, _geo |
| `ffbbserver_tournois` | TournoisMultiSearchResult | sexe, commune.*, _geo |
| `ffbbnational_pratiques` | PratiquesMultiSearchResult | type, label, _geo |
| `ffbbserver_engagements` | EngagementsMultiSearchResult | idCompetition.*, niveau.*, _geo |
| `ffbbserver_formations` | FormationsMultiSearchResult | domain, theme, mode |

### Geo-search

4 methodes utilisent `_geoRadius(lat, lng, radius_m)` :

- `search_organismes_by_geo(lat, lng, radius_km)`
- `search_salles_by_geo(lat, lng, radius_km)`
- `search_engagements_by_geo(lat, lng, radius_km)`
- `search_engagements_filtered(lat, lng, radius_km, sexes, niveau_codes)`

Le tri par distance utilise `_geoPoint(lat, lng):asc|desc` via `GeoSortOrder`.

---

## Convergence Meilisearch ↔ Directus

### Correspondance des IDs

L'`id` d'un hit Meilisearch correspond au PK Directus :

```python
# Meilisearch → Directus
hit = client.search_organismes("Paris").hits[0]
organisme = client.get_organisme(int(hit.id))
```

### Objets denormalises vs FK bruts

| Champ | Hit Meilisearch | Response Directus |
|-------|-----------------|-------------------|
| commune | `Commune` objet (libelle, code_postal) | `int` (FK brut) |
| salle | `Salle` objet (libelle, adresse) | `int` (FK brut) |
| geo | `Geo` objet (lat, lng) | absent (Cartographie embedded) |
| organisateur | `Organisateur` objet | `int` FK |
| saison | `Saison` objet (code, libelle) | `int` FK |

### Quand utiliser quel client ?

| Besoin | Client | Pourquoi |
|--------|--------|----------|
| Recherche textuelle | Meilisearch | Moteur full-text optimise |
| Recherche geo-spatiale | Meilisearch | `_geoRadius` natif |
| Resume rapide (commune, salle) | Meilisearch | Objets deja denormalises |
| Detail complet d'une entite | Directus | Tous les champs via fields[] |
| Resolution FK en profondeur | Directus | Chaque FK → appel supplementaire |
| Pagination exhaustive | Directus | `list_all_*` avec offset |
| Filtres JSON complexes | Directus | Operateurs `_eq`, `_in`, `_gt`... |

### Combinaison optimale

```python
# 1. Decouverte via Meilisearch
hits = client.search_organismes("basket Paris")

# 2. Approfondissement via Directus
for hit in hits.hits[:3]:
    org = client.get_organisme(int(hit.id))     # Detail complet
    salle = client.get_salle(org.salle)          # Resolution FK
    commune = client.list_communes(              # Resolution commune
        filter_criteria='{"id":{"_eq":' + str(org.commune) + '}}'
    )
```

---

## Chaines de Resolution FK

### Chaine 1 : Competition → Poule → Rencontre → Engagement → Entraineur

```
search_competitions("Departemental")
  └→ get_competition(int(hit.id))
       ├→ .organisateur → get_organisme(id)
       │    ├→ .commune → list_communes(filter=...)
       │    └→ .salle → get_salle(id)
       ├→ .phases[0].poules[0].id → get_poule(int(id))
       │    ├→ list_rencontres_by_poule(poule_id)
       │    │    └→ get_rencontre(id)
       │    │         ├→ .salle → get_salle(id)
       │    │         └→ .idEngagementEquipe1 → get_engagement(id)
       │    │              └→ .entraineur → get_entraineur(id)
       │    └→ list_engagements_by_poule(poule_id)
       └→ .logo → get_asset_url(uuid)
```

### Chaine 2 : Organisme (club) → resolution complete

```
search_organismes("Paris")
  └→ get_organisme(int(hit.id))
       ├→ .commune → list_communes(filter=...)
       ├→ .salle → get_salle(id) → .commune
       ├→ .organisme_id_pere → get_organisme(id)
       ├→ .engagements[:2] → list_engagements_by_ids(ids)
       │    └→ [0].entraineur → get_entraineur(id)
       ├→ .competitions[:1] → get_competition(id)
       ├→ .logo → get_asset_url(uuid)
       └→ get_club_contacts(organisme_id)
```

### Chaine 3 : Rencontre → resolution complete

```
search_rencontres("Paris")
  └→ get_rencontre(int(hit.id))
       ├→ .salle → get_salle(id) → .commune
       ├→ .idEngagementEquipe1 → get_engagement(id)
       │    └→ .entraineur → get_entraineur(id)
       ├→ .idOrganismeEquipe1 → get_organisme(id)
       ├→ .idOrganismeEquipe2 → get_organisme(id)
       └→ .competitionId → get_competition(id)
```

### Chaine 4 : Engagement profond

```
search_engagements("Paris")
  └→ get_engagement(int(hit.id))
       ├→ .idCompetition → get_competition(id)
       │    └→ .phases[0].poules[0].id → get_poule(int(id))
       ├→ .idOrganisme → get_organisme(id)
       ├→ .entraineur → get_entraineur(id) → .commune
       ├→ .logo → get_asset_url(uuid)
       └→ get_engagement_contacts(id)
```

### Chaine 5 : Live → Rencontre

```
get_lives()
  └→ [0].match_id → get_rencontre(match_id)
       └→ (resolution comme chaine 3)
```

---

## Embedded Hybrides (anomalies)

Certains objets embedded contiennent des FK implicites :

| Objet embedded | Champ FK | Resolution |
|----------------|----------|------------|
| CompetitionPhase.poules[].id | str → int | `get_poule(int(id))` |
| TeamRanking.organisme_id | str → int | `get_organisme(int(id))` |
| TeamRanking.id_engagement.id | int | `get_engagement(id)` |

Ces FK nestees sont partiellement expandues par Directus mais ne contiennent
pas toutes les donnees → appeler les methodes get_* pour l'objet complet.
