"""Streamlit dashboard for FFBB basketball analytics.

Demonstrates:
- Searching for a club via Meilisearch
- Resolving FK relationships (organisme → engagements → competition → poule)
- Using batch helpers (list_engagements_by_ids, list_rencontres_by_poule)
- Computing Elo ratings and advanced metrics
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.models.type_competition import TypeCompetition

TEAM_NAME = "PELISSANNE BASKET AVENIR"
COMPETITION_FILTERS: dict = {
    "sexe": "M",
    "type_competition": TypeCompetition.CHAMPIONNAT,
}


def _create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        meilisearch_bearer_token=tokens.meilisearch_token,
        api_bearer_token=tokens.api_token,
        debug=False,
    )


def _find_team_poule_id(
    client: FFBBAPIClientV2,
    team_name: str,
    filters: dict,
) -> int:
    """Resolve FK chain: organisme → engagements → competition → poule.

    1. Search Meilisearch for the club name.
    2. Fetch the organisme (engagements field = list of int FK IDs).
    3. Batch-fetch engagement objects via list_engagements_by_ids.
    4. For each engagement, fetch its competition and check filters.
    5. Return the matching poule ID.
    """
    search_results = client.search_organismes(name=team_name)
    if not search_results or not search_results.hits:
        raise ValueError(f"Team {team_name} not found")

    hit_id = search_results.hits[0].id
    if not hit_id:
        raise ValueError(f"Team {team_name} has no ID")
    organisme_id = int(hit_id)
    organisme = client.get_organisme(organisme_id)
    if not organisme:
        raise ValueError(f"Organisme {organisme_id} not found")

    # organisme.engagements is list[int] (FK IDs), not engagement objects
    engagement_ids = [eid for eid in organisme.engagements if isinstance(eid, int)]
    if not engagement_ids:
        raise ValueError(f"No engagements found for {team_name}")

    engagements = client.list_engagements_by_ids(engagement_ids)

    for eng in engagements:
        if not eng.idCompetition or not eng.idPoule:
            continue
        comp = client.get_competition(eng.idCompetition)
        if not comp:
            continue
        if (
            comp.sexe == filters["sexe"]
            and comp.type_competition == filters["type_competition"]
        ):
            return eng.idPoule

    raise ValueError(f"No matching poule found for {team_name}")


@st.cache_data
def load_data():
    client = _create_client()

    poule_id = _find_team_poule_id(client, TEAM_NAME, COMPETITION_FILTERS)
    poule_data = client.get_poule(poule_id)
    if not poule_data:
        raise ValueError(f"Poule {poule_id} not found")

    rankings_data = []
    for ranking in poule_data.classements or []:
        if not ranking.id_engagement:
            continue
        rankings_data.append(
            {
                "position": ranking.position,
                "team_name": ranking.id_engagement.nom,
                "points": ranking.points,
                "wins": ranking.gagnes,
                "losses": ranking.perdus,
                "games_played": ranking.match_joues,
                "points_scored": ranking.paniers_marques,
                "points_allowed": ranking.paniers_encaisses,
                "point_diff": ranking.difference,
            }
        )

    rankings_df = pd.DataFrame(rankings_data)
    rankings_df.set_index("position", inplace=True)

    # Fetch actual rencontre objects (poule_data.rencontres is list[int])
    rencontres = client.list_rencontres_by_poule(poule_id)

    def calculate_advanced_metrics(df):
        metrics_df = df.copy()
        metrics_df["ppg"] = metrics_df["points_scored"] / metrics_df["games_played"]
        metrics_df["papg"] = metrics_df["points_allowed"] / metrics_df["games_played"]
        metrics_df["win_pct"] = metrics_df["wins"] / metrics_df["games_played"]
        metrics_df["point_diff_pg"] = metrics_df["ppg"] - metrics_df["papg"]

        metrics_df["est_ts_pct"] = metrics_df["ppg"] / 2
        league_avg_games = metrics_df["games_played"].mean()
        metrics_df["est_ortg"] = (
            (metrics_df["points_scored"] / metrics_df["games_played"])
            * (league_avg_games / 2)
            * 100
        )
        metrics_df["est_drtg"] = (
            (metrics_df["points_allowed"] / metrics_df["games_played"])
            * (league_avg_games / 2)
            * 100
        )
        metrics_df["net_rating"] = metrics_df["est_ortg"] - metrics_df["est_drtg"]
        metrics_df["pythagorean_win_pct"] = metrics_df["points_scored"] ** 2 / (
            metrics_df["points_scored"] ** 2 + metrics_df["points_allowed"] ** 2
        )
        metrics_df["pythagorean_wins"] = (
            metrics_df["pythagorean_win_pct"] * metrics_df["games_played"]
        )
        metrics_df["performance_vs_pythag"] = (
            metrics_df["wins"] - metrics_df["pythagorean_wins"]
        )

        team_win_pct = dict(zip(metrics_df["team_name"], metrics_df["win_pct"]))
        metrics_df["sos"] = 0.0
        for idx, row in metrics_df.iterrows():
            team_name = row["team_name"]
            opponents = metrics_df[metrics_df["team_name"] != team_name]["team_name"]
            opponent_win_pcts = [team_win_pct[opp] for opp in opponents]
            metrics_df.loc[idx, "sos"] = (
                sum(opponent_win_pcts) / len(opponent_win_pcts)
                if opponent_win_pcts
                else 0
            )

        league_avg_win_pct = metrics_df["win_pct"].mean()
        metrics_df["srs"] = (
            metrics_df["point_diff_pg"] + (metrics_df["sos"] - league_avg_win_pct) * 10
        )
        metrics_df["ortg_adj"] = metrics_df["est_ortg"] + metrics_df["srs"] * 2
        metrics_df["drtg_adj"] = metrics_df["est_drtg"] + metrics_df["srs"] * 2
        metrics_df["net_rating_adj"] = metrics_df["ortg_adj"] - metrics_df["drtg_adj"]
        return metrics_df

    advanced_df = calculate_advanced_metrics(rankings_df)
    return rankings_df, advanced_df, rencontres, poule_id


rankings_df, advanced_df, rencontres, poule_id = load_data()

st.title("🏀 FFBB Basketball Analytics Dashboard")

st.sidebar.header("Team Selection")
team_list = rankings_df["team_name"].tolist()
default_team_index = team_list.index(TEAM_NAME) if TEAM_NAME in team_list else 0
selected_team = st.sidebar.selectbox("Select Team", team_list, index=default_team_index)

team_data = rankings_df[rankings_df["team_name"] == selected_team].iloc[0]

st.header(f"📊 {selected_team} Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Position", f"{team_data.name}")
col2.metric("Record", f"{team_data['wins']}-{team_data['losses']}")
col3.metric("Win %", f"{team_data['wins'] / team_data['games_played']:.1%}")
col4.metric("PPG", f"{team_data['points_scored'] / team_data['games_played']:.1f}")

team_advanced = advanced_df[advanced_df["team_name"] == selected_team].iloc[0]

st.header("Advanced Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Net Rating", f"{team_advanced['net_rating_adj']:+.1f}")
col2.metric("SRS", f"{team_advanced['srs']:+.1f}")
col3.metric("SOS", f"{team_advanced['sos']:.1%}")

st.header("League Comparison")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=rankings_df, x="team_name", y="wins", ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_title("Wins by Team")
st.pyplot(fig)

# ── Rating Evolution ─────────────────────────────────────────────────

st.header("📈 Rating Evolution")


def _calculate_expected_score(rating_a: float, rating_b: float) -> float:
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


@st.cache_data
def calculate_rating_evolution(_rencontres, _classements_names):
    """Compute Elo ratings from actual rencontre objects."""
    team_ratings: dict[str, float] = {}
    rating_history: dict[str, list[dict]] = {}

    for name in _classements_names:
        team_ratings[name] = 1500.0
        rating_history[name] = []

    # rencontres are GetRencontresResponse objects with .joue, .date_rencontre, etc.
    played_matches = [r for r in _rencontres if r.joue]
    played_matches.sort(key=lambda x: x.date_rencontre or x.date or x.id)

    K = 32
    for match_idx, match in enumerate(played_matches):
        team1 = match.nomEquipe1
        team2 = match.nomEquipe2
        if not team1 or not team2:
            continue
        if team1 not in team_ratings or team2 not in team_ratings:
            continue

        score1 = match.resultatEquipe1 or 0
        score2 = match.resultatEquipe2 or 0
        if score1 > score2:
            actual1, actual2 = 1, 0
        elif score1 < score2:
            actual1, actual2 = 0, 1
        else:
            actual1, actual2 = 0.5, 0.5

        rating1 = team_ratings[team1]
        rating2 = team_ratings[team2]
        expected1 = _calculate_expected_score(rating1, rating2)
        expected2 = _calculate_expected_score(rating2, rating1)
        team_ratings[team1] = rating1 + K * (actual1 - expected1)
        team_ratings[team2] = rating2 + K * (actual2 - expected2)

        for team in team_ratings:
            rating_history[team].append(
                {"match": match_idx + 1, "rating": team_ratings[team]}
            )

    rating_dfs = {team: pd.DataFrame(h) for team, h in rating_history.items()}
    return rating_dfs, team_ratings


classement_names = rankings_df["team_name"].tolist()

rating_dfs, final_ratings = calculate_rating_evolution(rencontres, classement_names)

fig, ax = plt.subplots(figsize=(12, 8))
colors = plt.cm.tab20(np.linspace(0, 1, len(rating_dfs)))
color_map = {team: colors[i] for i, team in enumerate(rating_dfs.keys())}
color_map[selected_team] = "red"

for team, df in rating_dfs.items():
    if df.empty:
        continue
    ax.plot(
        df["match"],
        df["rating"],
        "-",
        color=color_map[team],
        linewidth=1.5,
        alpha=0.8 if team != selected_team else 1,
        label=team if team == selected_team else "",
    )

if selected_team in rating_dfs and not rating_dfs[selected_team].empty:
    ax.plot(
        rating_dfs[selected_team]["match"],
        rating_dfs[selected_team]["rating"],
        "r-",
        linewidth=3,
        label=f"{selected_team} (Selected)",
    )

ax.axhline(
    y=1500, color="black", linestyle="--", alpha=0.5, label="Initial Rating (1500)"
)
ax.set_xlabel("Match #")
ax.set_ylabel("Elo Rating")
ax.set_title("Rating Evolution Over Season")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ── Rating comparison ────────────────────────────────────────────────

st.subheader("Current Rating Rankings")
rating_comparison = pd.DataFrame(
    {"team": list(final_ratings.keys()), "rating": list(final_ratings.values())}
).sort_values("rating", ascending=False)

rating_comparison["rank"] = range(1, len(rating_comparison) + 1)
rating_comparison["change"] = rating_comparison["rating"] - 1500
rating_comparison["normalized_rating"] = (
    rating_comparison["rating"] - rating_comparison["rating"].min()
) / (rating_comparison["rating"].max() - rating_comparison["rating"].min())

st.dataframe(
    rating_comparison[["rank", "team", "rating", "normalized_rating", "change"]]
    .style.format(
        {"rating": "{:.1f}", "normalized_rating": "{:.3f}", "change": "{:+.1f}"}
    )
    .apply(
        lambda x: [
            "background-color: lightcoral" if v == selected_team else "" for v in x
        ],
        axis=0,
    )
)

selected_rating = final_ratings.get(selected_team, 1500.0)
selected_change = selected_rating - 1500
selected_rank_row = rating_comparison[rating_comparison["team"] == selected_team]
selected_rank = (
    selected_rank_row["rank"].iloc[0] if not selected_rank_row.empty else "?"
)
selected_normalized = (
    selected_rank_row["normalized_rating"].iloc[0] if not selected_rank_row.empty else 0
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Rating", f"{selected_rating:.1f}")
with col2:
    st.metric("Normalized Rating", f"{selected_normalized:.3f}")
with col3:
    st.metric("Rating Change", f"{selected_change:+.1f}")
with col4:
    st.metric("Rating Rank", f"{selected_rank}/{len(final_ratings)}")

# ── Season End Projection ────────────────────────────────────────────

st.header("🎯 Projection de Fin de Saison")


def project_season_end(current_ratings, all_rencontres, team_name):
    """Project end-of-season ratings assuming wins vs similar-rated opponents."""
    projected_ratings = current_ratings.copy()
    remaining = [r for r in all_rencontres if not r.joue]
    target_remaining = [
        m for m in remaining if m.nomEquipe1 == team_name or m.nomEquipe2 == team_name
    ]

    K = 32
    for match in target_remaining:
        opponent = (
            match.nomEquipe2 if match.nomEquipe1 == team_name else match.nomEquipe1
        )
        if not opponent or opponent not in projected_ratings:
            continue
        rating_diff = abs(projected_ratings[team_name] - projected_ratings[opponent])
        if rating_diff <= 100:
            rating_team = projected_ratings[team_name]
            rating_opp = projected_ratings[opponent]
            expected_team = _calculate_expected_score(rating_team, rating_opp)
            expected_opp = _calculate_expected_score(rating_opp, rating_team)
            projected_ratings[team_name] = rating_team + K * (1 - expected_team)
            projected_ratings[opponent] = rating_opp + K * (0 - expected_opp)

    return projected_ratings


projected_ratings = project_season_end(final_ratings, rencontres, selected_team)

projected_df = (
    pd.DataFrame(
        {
            "team": list(projected_ratings.keys()),
            "projected_rating": list(projected_ratings.values()),
        }
    )
    .sort_values("projected_rating", ascending=False)
    .reset_index(drop=True)
)

projected_df["projected_normalized"] = (
    projected_df["projected_rating"] - projected_df["projected_rating"].min()
) / (projected_df["projected_rating"].max() - projected_df["projected_rating"].min())
projected_df["rank"] = projected_df.index + 1
projected_df["change_from_current"] = (
    projected_df["projected_rating"] - rating_comparison.set_index("team")["rating"]
)

selected_projected = projected_df[projected_df["team"] == selected_team]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Projected Rating",
        f"{projected_ratings.get(selected_team, 1500):.1f}",
        f"{projected_ratings.get(selected_team, 1500) - final_ratings.get(selected_team, 1500):+.1f}",
    )
with col2:
    if not selected_projected.empty:
        st.metric(
            "Projected Normalized",
            f"{selected_projected['projected_normalized'].iloc[0]:.3f}",
        )
with col3:
    if not selected_projected.empty:
        st.metric(
            "Projected Rank",
            f"{selected_projected['rank'].iloc[0]}/{len(projected_df)}",
        )
with col4:
    remaining_similar = len(
        [
            m
            for m in rencontres
            if not m.joue
            and (m.nomEquipe1 == selected_team or m.nomEquipe2 == selected_team)
            and (
                opp := (m.nomEquipe2 if m.nomEquipe1 == selected_team else m.nomEquipe1)
            )
            and opp in final_ratings
            and abs(final_ratings[selected_team] - final_ratings[opp]) <= 100
        ]
    )
    st.metric("Simulated Wins", f"{remaining_similar}")

st.subheader("Projected Final Rankings")
st.dataframe(
    projected_df[
        [
            "rank",
            "team",
            "projected_rating",
            "projected_normalized",
            "change_from_current",
        ]
    ]
    .style.format(
        {
            "projected_rating": "{:.1f}",
            "projected_normalized": "{:.3f}",
            "change_from_current": "{:+.1f}",
        }
    )
    .apply(
        lambda x: [
            "background-color: lightgreen" if v == selected_team else "" for v in x
        ],
        axis=0,
    )
)
