import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.models.categorie_type import CategorieType
from ffbb_api_client_v2.models.competition_origine_type_competition import (
    CompetitionOrigineTypeCompetition,
)
from ffbb_api_client_v2.models.niveau_type import NiveauType as NiveauTypeEnum


@st.cache_data
def load_data():
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        meilisearch_bearer_token=tokens.meilisearch_token,
        api_bearer_token=tokens.api_token,
        debug=False,
    )
    TEAM_NAME = "PELISSANNE BASKET AVENIR"
    COMPETITION_FILTERS = {
        "sexe": "M",
        "zone": NiveauTypeEnum.REGIONAL.value,
        "division": 2,
        "niveau_competition": CompetitionOrigineTypeCompetition.DIV.value,
        "categorie": CategorieType.SENIOR.value,
    }

    def find_team_poule_id(client, team_name, filters):
        search_results = client.search_organismes(name=team_name)
        if not search_results or not search_results.hits:
            raise ValueError(f"Team {team_name} not found")

        organisme_id = int(search_results.hits[0].id)
        organisme_response = client.get_organisme(organisme_id)

        for engagement in organisme_response.engagements:
            if not engagement.id_competition:
                continue
            comp = engagement.id_competition
            if (
                comp.sexe == filters["sexe"]
                and comp.type_competition == filters["niveau_competition"]
            ):
                if comp.niveau and comp.niveau.type.value == filters["zone"]:
                    if engagement.id_poule:
                        return int(engagement.id_poule.id)

        raise ValueError(f"No poule found for {team_name}")

    poule_id = find_team_poule_id(client, TEAM_NAME, COMPETITION_FILTERS)
    poule_data = client.get_poule(poule_id)

    rankings_data = []
    for ranking in poule_data.classements:
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

    # Calculate advanced metrics

    def calculate_advanced_metrics(df):
        metrics_df = df.copy()

        # Basic calculations
        metrics_df["ppg"] = metrics_df["points_scored"] / metrics_df["games_played"]
        metrics_df["papg"] = metrics_df["points_allowed"] / metrics_df["games_played"]
        metrics_df["win_pct"] = metrics_df["wins"] / metrics_df["games_played"]
        metrics_df["point_diff_pg"] = metrics_df["ppg"] - metrics_df["papg"]

        # Approximations
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

        # Pythagorean
        metrics_df["pythagorean_win_pct"] = metrics_df["points_scored"] ** 2 / (
            metrics_df["points_scored"] ** 2 + metrics_df["points_allowed"] ** 2
        )
        metrics_df["pythagorean_wins"] = (
            metrics_df["pythagorean_win_pct"] * metrics_df["games_played"]
        )
        metrics_df["performance_vs_pythag"] = (
            metrics_df["wins"] - metrics_df["pythagorean_wins"]
        )

        # Enhanced Metrics
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

    return rankings_df, advanced_df


rankings_df, advanced_df = load_data()

st.title("🏀 FFBB Basketball Analytics Dashboard")

st.sidebar.header("Team Selection")

team_list = rankings_df["team_name"].tolist()
default_team_index = (
    team_list.index("PELISSANNE BASKET AVENIR")
    if "PELISSANNE BASKET AVENIR" in team_list
    else 0
)

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

# Rating Evolution Section
st.header("📈 Rating Evolution")


# Calculate rating evolution (similar to notebook)
@st.cache_data
def calculate_rating_evolution():
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        meilisearch_bearer_token=tokens.meilisearch_token,
        api_bearer_token=tokens.api_token,
        debug=False,
    )
    TEAM_NAME = "PELISSANNE BASKET AVENIR"
    COMPETITION_FILTERS = {
        "sexe": "M",
        "zone": NiveauTypeEnum.REGIONAL.value,
        "division": 2,
        "niveau_competition": CompetitionOrigineTypeCompetition.DIV.value,
        "categorie": CategorieType.SENIOR.value,
    }

    def find_team_poule_id(client, team_name, filters):
        search_results = client.search_organismes(name=team_name)
        if not search_results or not search_results.hits:
            raise ValueError(f"Team {team_name} not found")

        organisme_id = int(search_results.hits[0].id)
        organisme_response = client.get_organisme(organisme_id)

        for engagement in organisme_response.engagements:
            if not engagement.id_competition:
                continue
            comp = engagement.id_competition
            if (
                comp.sexe == filters["sexe"]
                and comp.type_competition == filters["niveau_competition"]
            ):
                if comp.niveau and comp.niveau.type.value == filters["zone"]:
                    if engagement.id_poule:
                        return int(engagement.id_poule.id)

        raise ValueError(f"No poule found for {team_name}")

    poule_id = find_team_poule_id(client, TEAM_NAME, COMPETITION_FILTERS)
    poule_data = client.get_poule(poule_id)

    def calculate_expected_score(rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    # Initialize ratings for all teams
    team_ratings = {}
    rating_history = {}

    for ranking in poule_data.classements:
        team_name = ranking.id_engagement.nom
        team_ratings[team_name] = 1500.0
        rating_history[team_name] = []

    # Get all played matches and sort by date
    played_matches = [r for r in poule_data.rencontres if r.joue]
    played_matches.sort(key=lambda x: x.date_rencontre)

    K = 32

    for match_idx, match in enumerate(played_matches):
        team1 = match.nomEquipe1
        team2 = match.nomEquipe2

        if team1 not in team_ratings or team2 not in team_ratings:
            continue

        score1 = int(match.resultatEquipe1)
        score2 = int(match.resultatEquipe2)

        if score1 > score2:
            actual1, actual2 = 1, 0
        elif score1 < score2:
            actual1, actual2 = 0, 1
        else:
            actual1, actual2 = 0.5, 0.5

        rating1 = team_ratings[team1]
        rating2 = team_ratings[team2]

        expected1 = calculate_expected_score(rating1, rating2)
        expected2 = calculate_expected_score(rating2, rating1)

        new_rating1 = rating1 + K * (actual1 - expected1)
        new_rating2 = rating2 + K * (actual2 - expected2)

        team_ratings[team1] = new_rating1
        team_ratings[team2] = new_rating2

        for team in team_ratings:
            rating_history[team].append(
                {"match": match_idx + 1, "rating": team_ratings[team]}
            )

    # Convert to DataFrames
    rating_dfs = {}
    for team, history in rating_history.items():
        rating_dfs[team] = pd.DataFrame(history)

    return rating_dfs, team_ratings


rating_dfs, final_ratings = calculate_rating_evolution()

# Rating evolution chart
fig, ax = plt.subplots(figsize=(12, 8))

colors = plt.cm.tab20(np.linspace(0, 1, len(rating_dfs)))
color_map = {team: colors[i] for i, team in enumerate(rating_dfs.keys())}
color_map[selected_team] = "red"

for team, df in rating_dfs.items():
    ax.plot(
        df["match"],
        df["rating"],
        "-",
        color=color_map[team],
        linewidth=1.5,
        alpha=0.8 if team != selected_team else 1,
        label=team if team == selected_team else "",
    )

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

# Rating comparison
st.subheader("Current Rating Rankings")

rating_comparison = pd.DataFrame(
    {"team": list(final_ratings.keys()), "rating": list(final_ratings.values())}
).sort_values("rating", ascending=False)

rating_comparison["rank"] = range(1, len(rating_comparison) + 1)
rating_comparison["change"] = rating_comparison["rating"] - 1500

# Add normalized rating (0-1 scale)
rating_comparison["normalized_rating"] = (
    rating_comparison["rating"] - rating_comparison["rating"].min()
) / (rating_comparison["rating"].max() - rating_comparison["rating"].min())

# Display table
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

# Selected team rating summary
selected_rating = final_ratings[selected_team]
selected_change = selected_rating - 1500
selected_rank = rating_comparison[rating_comparison["team"] == selected_team][
    "rank"
].iloc[0]
selected_normalized = rating_comparison[rating_comparison["team"] == selected_team][
    "normalized_rating"
].iloc[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Rating", f"{selected_rating:.1f}")
with col2:
    st.metric("Normalized Rating", f"{selected_normalized:.3f}")
with col3:
    st.metric("Rating Change", f"{selected_change:+.1f}")
with col4:
    st.metric("Rating Rank", f"{selected_rank}/{len(final_ratings)}")

# Season End Projection
st.header("🎯 Projection de Fin de Saison")


def project_season_end_dashboard(poule_data, current_ratings, team_name):
    """Project season end assuming wins against similar-rated opponents"""

    # Copy current ratings
    projected_ratings = current_ratings.copy()

    # Get remaining matches
    remaining_matches = [r for r in poule_data.rencontres if not r.joue]

    # Filter matches involving target team
    target_remaining = [
        m
        for m in remaining_matches
        if m.nomEquipe1 == team_name or m.nomEquipe2 == team_name
    ]

    K = 32

    def calculate_expected_score(rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    for match in target_remaining:
        if match.nomEquipe1 == team_name:
            opponent = match.nomEquipe2
        else:
            opponent = match.nomEquipe1

        # Skip if opponent not in ratings (shouldn't happen but safety check)
        if opponent not in projected_ratings:
            continue

        # Check if opponent is similar level (±100 Elo points)
        rating_diff = abs(projected_ratings[team_name] - projected_ratings[opponent])

        if rating_diff <= 100:  # Similar level opponent
            # Simulate target team win
            rating_team = projected_ratings[team_name]
            rating_opp = projected_ratings[opponent]

            expected_team = calculate_expected_score(rating_team, rating_opp)
            expected_opp = calculate_expected_score(rating_opp, rating_team)

            # Team wins (1-0)
            new_rating_team = rating_team + K * (1 - expected_team)
            new_rating_opp = rating_opp + K * (0 - expected_opp)

            projected_ratings[team_name] = new_rating_team
            projected_ratings[opponent] = new_rating_opp

    return projected_ratings


# Get poule_data for projection (reuse from load_data)
poule_data = (
    load_data()
)  # This needs to be adjusted, actually load_data returns processed data, not poule_data

# Actually, we need to get the raw poule_data. Let's modify the load_data to return it or create a separate function.


# For now, let's create a cached function to get poule_data
@st.cache_data
def get_poule_data():
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        meilisearch_bearer_token=tokens.meilisearch_token,
        api_bearer_token=tokens.api_token,
        debug=False,
    )
    TEAM_NAME = "PELISSANNE BASKET AVENIR"
    COMPETITION_FILTERS = {
        "sexe": "M",
        "zone": NiveauTypeEnum.REGIONAL.value,
        "division": 2,
        "niveau_competition": CompetitionOrigineTypeCompetition.DIV.value,
        "categorie": CategorieType.SENIOR.value,
    }

    def find_team_poule_id(client, team_name, filters):
        search_results = client.search_organismes(name=team_name)
        if not search_results or not search_results.hits:
            raise ValueError(f"Team {team_name} not found")

        organisme_id = int(search_results.hits[0].id)
        organisme_response = client.get_organisme(organisme_id)

        for engagement in organisme_response.engagements:
            if not engagement.id_competition:
                continue
            comp = engagement.id_competition
            if (
                comp.sexe == filters["sexe"]
                and comp.type_competition == filters["niveau_competition"]
            ):
                if comp.niveau and comp.niveau.type.value == filters["zone"]:
                    if engagement.id_poule:
                        return int(engagement.id_poule.id)

        raise ValueError(f"No poule found for {team_name}")

    poule_id = find_team_poule_id(client, TEAM_NAME, COMPETITION_FILTERS)
    poule_data = client.get_poule(poule_id)
    return poule_data


poule_data_raw = get_poule_data()
projected_ratings = project_season_end_dashboard(
    poule_data_raw, final_ratings, selected_team
)

# Calculate projected ranking
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

# Show projection for selected team
selected_projected = projected_df[projected_df["team"] == selected_team]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Projected Rating",
        f"{projected_ratings[selected_team]:.1f}",
        f"{projected_ratings[selected_team] - final_ratings[selected_team]:+.1f}",
    )
with col2:
    st.metric(
        "Projected Normalized",
        f"{selected_projected['projected_normalized'].iloc[0]:.3f}",
    )
with col3:
    st.metric(
        "Projected Rank", f"{selected_projected['rank'].iloc[0]}/{len(projected_df)}"
    )
with col4:
    remaining_similar = len(
        [
            m
            for m in poule_data_raw.rencontres
            if not m.joue
            and (m.nomEquipe1 == selected_team or m.nomEquipe2 == selected_team)
            and (m.nomEquipe2 if m.nomEquipe1 == selected_team else m.nomEquipe1)
            in final_ratings
            and abs(
                final_ratings[selected_team]
                - final_ratings[
                    m.nomEquipe2 if m.nomEquipe1 == selected_team else m.nomEquipe1
                ]
            )
            <= 100
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
