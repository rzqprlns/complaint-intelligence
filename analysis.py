import pandas as pd
import numpy as np


# =========================================================
# 1. LOAD & PREPARE DATA
# =========================================================

def load_and_prepare_data(
    file_path="synthetic_complaint_data.csv"
):
    df = pd.read_csv(file_path)

    time_columns = [
        "complaint_timestamp",
        "response_timestamp",
        "resolve_timestamp",
    ]

    for col in time_columns:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

    return df


# =========================================================
# 2. SERVICE TIME METRICS
# =========================================================

def calculate_service_metrics(df):
    data = df.copy()

    # How long until the complaint receives a response?
    data["response_minutes"] = (
        data["response_timestamp"]
        - data["complaint_timestamp"]
    ).dt.total_seconds() / 60

    # How long until the complaint is resolved?
    data["resolution_minutes"] = (
        data["resolve_timestamp"]
        - data["complaint_timestamp"]
    ).dt.total_seconds() / 60

    data["resolution_hours"] = (
        data["resolution_minutes"] / 60
    )

    # Flag records that already have a resolution timestamp
    data["is_resolved"] = (
        data["resolve_timestamp"].notna()
    )

    return data


# =========================================================
# 3. OVERALL KPI
# =========================================================

def calculate_overall_kpi(df):
    data = calculate_service_metrics(df)

    total_complaints = len(data)

    solved = (
        data["ticket_status"]
        .eq("SOLVED")
        .sum()
    )

    expired = (
        data["ticket_status"]
        .eq("EXPIRED")
        .sum()
    )

    solved_rate = (
        solved / total_complaints * 100
        if total_complaints > 0
        else 0
    )

    return {
        "total_complaints": total_complaints,
        "median_response_minutes":
            data["response_minutes"].median(),

        "median_resolution_hours":
            data["resolution_hours"].median(),

        "solved_tickets": solved,
        "expired_tickets": expired,
        "solved_rate": solved_rate,
    }


# =========================================================
# 4. COMPLAINT TYPE ANALYSIS
# =========================================================

def complaint_type_summary(df):
    data = calculate_service_metrics(df)

    summary = (
        data.groupby(
            "complaint_type",
            as_index=False
        )
        .agg(
            complaints=(
                "complaint_id",
                "count"
            ),
            median_response_min=(
                "response_minutes",
                "median"
            ),
            median_resolution_hr=(
                "resolution_hours",
                "median"
            ),
        )
        .sort_values(
            "complaints",
            ascending=False
        )
    )

    return summary


# =========================================================
# 5. OUTLET ANALYSIS
# =========================================================

def outlet_summary(df):
    data = calculate_service_metrics(df)

    summary = (
        data.groupby(
            "outlet",
            as_index=False
        )
        .agg(
            complaints=(
                "complaint_id",
                "count"
            ),
            median_response_min=(
                "response_minutes",
                "median"
            ),
            median_resolution_hr=(
                "resolution_hours",
                "median"
            ),
            expired_cases=(
                "ticket_status",
                lambda x: (x == "EXPIRED").sum()
            ),
        )
    )

    summary["expired_rate"] = (
        summary["expired_cases"]
        / summary["complaints"]
        * 100
    )

    return summary.sort_values(
        "complaints",
        ascending=False
    )


# =========================================================
# 6. RESPONSIBLE AREA ANALYSIS
# =========================================================

def responsible_area_summary(df):
    data = calculate_service_metrics(df)

    summary = (
        data.groupby(
            "responsible_area",
            as_index=False
        )
        .agg(
            complaints=(
                "complaint_id",
                "count"
            ),
            median_resolution_hr=(
                "resolution_hours",
                "median"
            ),
            expired_cases=(
                "ticket_status",
                lambda x: (x == "EXPIRED").sum()
            ),
        )
        .sort_values(
            "complaints",
            ascending=False
        )
    )

    return summary


# =========================================================
# 7. DAILY COMPLAINT TREND
# =========================================================

def daily_complaint_trend(df):
    data = calculate_service_metrics(df)

    data["complaint_date"] = (
        data["complaint_timestamp"].dt.date
    )

    daily = (
        data.groupby(
            "complaint_date",
            as_index=False
        )
        .agg(
            complaints=(
                "complaint_id",
                "count"
            )
        )
    )

    daily["complaint_date"] = pd.to_datetime(
        daily["complaint_date"]
    )

    return daily


# =========================================================
# 8. ISSUE × OUTLET HOTSPOTS
# =========================================================

def outlet_issue_hotspots(df):
    data = calculate_service_metrics(df)

    hotspots = (
        data.groupby(
            [
                "outlet",
                "complaint_type"
            ],
            as_index=False
        )
        .agg(
            complaints=(
                "complaint_id",
                "count"
            ),
            median_resolution_hr=(
                "resolution_hours",
                "median"
            ),
            expired_cases=(
                "ticket_status",
                lambda x: (x == "EXPIRED").sum()
            ),
        )
    )

    hotspots["expired_rate"] = (
        hotspots["expired_cases"]
        / hotspots["complaints"]
        * 100
    )

    return hotspots.sort_values(
        [
            "complaints",
            "expired_rate"
        ],
        ascending=[
            False,
            False
        ]
    )


# =========================================================
# 9. FULL ANALYTICAL DATASET
# =========================================================

def prepare_analysis_dataset(
    file_path="synthetic_complaint_data.csv"
):
    df = load_and_prepare_data(
        file_path
    )

    return calculate_service_metrics(df)
