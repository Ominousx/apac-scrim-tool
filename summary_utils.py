import pandas as pd

def get_summary(all_region_dfs):
    TIER_1_REGIONS = ["VCT Pacific", "CN"]

    data = []
    for region_name, map_df in all_region_dfs:
        tier = "Tier 1" if region_name in TIER_1_REGIONS else "Tier 2"

        for _, row in map_df.iterrows():
            for side in [1, 2]:
                team = row[f"Team {side} Name"]
                score = row[f"Team {side} Score"]
                opp_score = row[f"Team {3 - side} Score"]
                agents = row[f"Team {side} Agents"]
                win = int(score > opp_score)
                data.append({
                    "Match Id": row["Match Id"],
                    "Team": team,
                    "Win": win,
                    "Comp": agents,
                    "Tier": tier
                })

    df_summary = pd.DataFrame(data).sort_values(["Team", "Match Id"])
    df_summary["Streak"] = df_summary.groupby("Team")["Win"].transform(
        lambda x: (x != x.shift()).cumsum().groupby(x).cumcount() + 1
    ) * df_summary["Win"]

    latest = df_summary.groupby("Team").tail(1)[["Team", "Streak"]]
    tier_map = df_summary.groupby("Team")["Tier"].first().reset_index()

    result = (
        df_summary.groupby("Team")
        .agg(
            Matches=("Win", "count"),
            Wins=("Win", "sum"),
            WinRate=("Win", lambda x: round(100 * x.mean(), 1)),
            CommonComp=("Comp", lambda x: x.mode().iloc[0] if not x.mode().empty else "N/A")
        )
        .reset_index()
        .merge(latest, on="Team", how="left")
        .merge(tier_map, on="Team", how="left")
    )

    def calculate_scrim_score(row):
        win_rate = row["WinRate"]
        matches = row["Matches"]
        streak = row["Streak"]
        tier = row["Tier"]

        wr_component = win_rate * 0.6
        match_component = min(matches / 8, 1) * 10 * 0.1
        streak_component = min(streak, 5) * 2 * 0.3
        tier_component = 2 * 0.1 if tier == "Tier 1" else 0

        return round(wr_component + match_component + streak_component + tier_component, 2)

    result["ScrimScore"] = result.apply(calculate_scrim_score, axis=1)
    result = result.sort_values("ScrimScore", ascending=False)

    return result
