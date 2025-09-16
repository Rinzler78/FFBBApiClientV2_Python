# Plan de Mise à Niveau API FFBB Client V2

## Vue d'ensemble

Suite à la mise à jour du fichier `data/api.ffbb.app.json` avec les URL officielles FFBB, ce document présente le plan de mise à niveau du code source pour supporter toutes les nouvelles fonctionnalités et champs d'API.

## 📋 Changements Configuration API

### ✅ Déjà effectué

- **ffbbserver_competitions**: Mise à jour avec tous les champs officiels (67 champs)
- **ffbbserver_poules**: Configuration complète avec classements (91 champs)
- **ffbbserver_saisons**: Configuration de base avec filtre actif
- **ffbbserver_organismes**: Configuration complète (102 champs)

## 🚀 Plan de Mise à Niveau du Code Source

### Phase 1: Analyse des nouveaux champs API

#### 1.1 Nouveaux champs identifiés dans ffbbserver_competitions
```
- gsId.* (scores par quart-temps, statut match en direct)
- officiels.* (arbitres et officiels)
- salle.* (informations détaillées des salles)
- engagements.* (nouvelles relations d'engagement)
```

#### 1.2 Nouveaux champs dans ffbbserver_organismes
```
- offresPratiques.* (offres de pratique sportive)
- labellisation.* (programmes de labellisation)
- organismes_fils.* (organismes enfants)
- communeClubPro.* (adresses club professionnel)
```

### Phase 2: Modèles de données à créer/mettre à jour

#### 2.1 Nouveaux modèles nécessaires

**A. Models pour les matchs en direct (Live)**
- `GameStatsModel` : scores par quart-temps, overtime, statut
- `OfficielsModel` : arbitres et officiels de match
- `FonctionModel` : fonctions des officiels

**B. Models pour les salles étendues**
- `SalleExtendedModel` : informations complètes (déjà partiellement présent)
- `CartographieModel` : coordonnées GPS
- `CommuneModel` : informations ville/code postal

**C. Models pour les organismes**
- `OffresPratiquesModel` : offres de pratique
- `LabellisationModel` : programmes de labellisation
- `OrganismesFilsModel` : sous-organismes
- `MembreModel` : membres des organismes

#### 2.2 Modèles à étendre

**A. CompetitionModel (competitions_models.py)**
```python
# Nouveaux champs à ajouter :
- live_stat: bool
- publication_internet: str
- phases: List[PhaseModel]
```

**B. RencontresModel**
```python
# Nouveaux champs à ajouter :
- gs_id: GameStatsModel
- officiels: List[OfficielsModel]
- salle_complete: SalleExtendedModel
```

**C. PoulesModel (poules_models.py)**
```python
# Déjà étendu avec classements ✅
# À valider : logo.id au niveau poule
```

### Phase 3: Mise à jour des champs de requête

#### 3.1 CompetitionFields (query_fields.py)
```python
# Nouveaux champs à ajouter :
PHASES_POULES_RENCONTRES_GSID_MATCH_ID = "phases.poules.rencontres.gsId.matchId"
PHASES_POULES_RENCONTRES_GSID_CURRENT_STATUS = "phases.poules.rencontres.gsId.currentStatus"
PHASES_POULES_RENCONTRES_GSID_SCORE_Q1_HOME = "phases.poules.rencontres.gsId.score_q1_home"
# ... (tous les scores par quart-temps)
PHASES_POULES_RENCONTRES_OFFICIELS_ORDRE = "phases.poules.rencontres.officiels.ordre"
PHASES_POULES_RENCONTRES_OFFICIELS_FONCTION_LIBELLE = "phases.poules.rencontres.officiels.fonction.libelle"
```

#### 3.2 OrganismeFields (query_fields.py)
```python
# Nouveaux champs à ajouter :
OFFRES_PRATIQUES_ID = "offresPratiques.ffbbserver_offres_pratiques_id.id"
OFFRES_PRATIQUES_TITLE = "offresPratiques.ffbbserver_offres_pratiques_id.title"
LABELLISATION_ID = "labellisation.id"
LABELLISATION_DEBUT = "labellisation.debut"
ORGANISMES_FILS_ID = "organismes_fils.id"
```

### Phase 4: Extension des clients API

#### 4.1 ApiFFBBAppClient (api_ffbb_app_client.py)
```python
# Nouvelles méthodes à ajouter :

def get_competition_with_live_stats(self, competition_id: int) -> GetCompetitionResponse:
    """Récupère une compétition avec statistiques en direct."""

def get_organisme_detailed(self, organisme_id: int) -> GetOrganismeResponse:
    """Récupère un organisme avec toutes les informations étendues."""
```

#### 4.2 Paramètres de requête avancés
```python
# Support des nouveaux paramètres :
- deep[rencontres][_filter][saison][actif] = true
- deep[rencontres][_sort][] = date_rencontre
```

### Phase 5: Tests et validation

#### 5.1 Tests unitaires nouveaux
- `test_competition_live_stats.py` : Test des stats en direct
- `test_organisme_extended.py` : Test des organismes étendus
- `test_query_fields_extended.py` : Test des nouveaux champs

#### 5.2 Tests d'intégration
- Validation avec `analyze_senas_ranking.py`
- Test de compatibilité ascendante
- Performance avec les nouveaux champs

## 📊 Impact et Priorités

### Priorité 1 (Critique)
1. **Modèles GameStats/Live** : Nécessaire pour les matchs en direct
2. **Extension CompetitionModel** : Support des phases/poules complètes
3. **Tests de compatibilité** : Assurer que l'existant fonctionne

### Priorité 2 (Important)
1. **Modèles Organismes étendus** : Support complet des organismes
2. **Champs Officiels/Salles** : Information complète des rencontres
3. **Performance** : Optimisation avec les nouveaux champs

### Priorité 3 (Optionnel)
1. **Labellisation/Offres pratiques** : Fonctionnalités avancées
2. **Organismes fils** : Structure hiérarchique
3. **Documentation** : Mise à jour des docs

## 🔄 Stratégie de déploiement

### Approche incrémentale
1. **Phase 1** : Modèles de base (GameStats, Officiels)
2. **Phase 2** : Extension des modèles existants
3. **Phase 3** : Nouvelles fonctionnalités avancées
4. **Phase 4** : Optimisation et documentation

### Rétrocompatibilité
- Tous les nouveaux champs sont optionnels
- Les anciens clients continuent de fonctionner
- Migration progressive possible

## 📈 Bénéfices attendus

1. **Couverture API complète** : Support de 100% des champs officiels FFBB
2. **Fonctionnalités avancées** : Stats en direct, organismes complets
3. **Performance** : Requêtes optimisées avec filtres/tris
4. **Maintenabilité** : Code aligné sur l'API officielle

## 🎯 Prochaines étapes

1. Commencer par l'analyse des nouveaux champs (Phase 1)
2. Créer les modèles GameStats/Live en priorité
3. Étendre progressivement les modèles existants
4. Valider à chaque étape avec les tests existants
