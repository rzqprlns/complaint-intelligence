import pandas as pd
import streamlit as st

from analysis import (
    prepare_analysis_dataset,
    calculate_overall_kpi,
    complaint_type_summary,
    outlet_summary,
    responsible_area_summary,
    daily_complaint_trend,
    outlet_issue_hotspots,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Complaint Intelligence",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --cream:#fffaf2;
    --ink:#172033;
    --muted:#707783;
    --yellow:#ffd95a;
    --mint:#ccefe3;
    --blue:#e6edff;
    --peach:#ffd9ca;
    --line:#ddd8cf;
}

html, body, [class*="css"] {
    font-family:'DM Sans',sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 94% 4%, #e6edff 0, transparent 22%),
        radial-gradient(circle at 3% 15%, #fff1b8 0, transparent 18%),
        var(--cream);
    color:var(--ink);
}

.block-container {
    max-width:1120px;
    padding-top:2rem;
    padding-bottom:5rem;
}

h1 {
    font-weight:700 !important;
    letter-spacing:-0.055em !important;
    line-height:.98 !important;
}

h2, h3 {
    letter-spacing:-0.03em !important;
}

p {
    color:var(--muted);
    line-height:1.75;
}

div[data-testid="stMetric"] {
    background:rgba(255,255,255,.72);
    border:1px solid var(--ink);
    padding:1rem;
    min-height:108px;
}

div[data-testid="stMetricLabel"] {
    font-family:'IBM Plex Mono',monospace;
    text-transform:uppercase;
    letter-spacing:.05em;
    font-size:.68rem;
}

div[data-testid="stMetricValue"] {
    font-weight:700;
}

div[data-testid="stDataFrame"] {
    border:1px solid var(--line);
}

div[data-testid="stExpander"] {
    border-radius:0;
    border:1px solid var(--line);
    background:rgba(255,255,255,.55);
}

hr {
    border:none;
    border-top:1px solid var(--line);
    margin:3rem 0;
}

#MainMenu, footer {
    visibility:hidden;
}

header[data-testid="stHeader"] {
    background:transparent;
}

@media(max-width:760px) {
    .block-container {
        padding-left:1rem;
        padding-right:1rem;
        padding-top:1.4rem;
    }

    h1 {
        font-size:3.2rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def label(text):
    st.caption(text.upper())


@st.cache_data
def load_analysis():
    return prepare_analysis_dataset(
        "synthetic_complaint_data.csv"
    )


# =========================================================
# LOAD
# =========================================================

df = load_analysis()

kpi = calculate_overall_kpi(df)
type_summary = complaint_type_summary(df)
outlets = outlet_summary(df)
areas = responsible_area_summary(df)
daily = daily_complaint_trend(df)
hotspots = outlet_issue_hotspots(df)


# =========================================================
# HERO
# =========================================================

label("Rizqi / Operations Lab · 04")

st.title(
    "Complaints are signals.\nWhere should we look?"
)

st.write(
    """
An interactive customer-experience analytics project
that turns complaint records into operational signals:
what happens most often, where it happens, how quickly
cases are handled, and which patterns deserve investigation.
"""
)

st.info(
    "Public-safe portfolio reconstruction. All customer "
    "records in this application are synthetic and contain "
    "no original personally identifiable information."
)


# =========================================================
# OVERALL KPI
# =========================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Complaints",
        f"{kpi['total_complaints']:,}"
    )

with k2:
    st.metric(
        "Median response",
        f"{kpi['median_response_minutes']:.0f} min"
    )

with k3:
    st.metric(
        "Median resolution",
        f"{kpi['median_resolution_hours']:.1f} hr"
    )

with k4:
    st.metric(
        "Solved rate",
        f"{kpi['solved_rate']:.1f}%"
    )


st.divider()


# =========================================================
# QUESTION
# =========================================================

label("01 · Diagnose")
st.header("Start with what is happening.")

st.write(
    """
Complaint analytics should not begin by assigning blame.
The first step is descriptive: understand volume, issue mix,
service speed, ticket outcomes, and recurring patterns.
"""
)


# =========================================================
# DAILY TREND
# =========================================================

st.subheader("Complaint volume over time")

daily_chart = (
    daily[
        [
            "complaint_date",
            "complaints"
        ]
    ]
    .set_index("complaint_date")
)

st.line_chart(daily_chart)


# =========================================================
# COMPLAINT MIX
# =========================================================

st.subheader("What are customers complaining about?")

complaint_chart = (
    type_summary[
        [
            "complaint_type",
            "complaints"
        ]
    ]
    .set_index("complaint_type")
)

st.bar_chart(complaint_chart)


top_issue = type_summary.iloc[0]

st.caption(
    f"The most frequent complaint category in this "
    f"synthetic dataset is “{top_issue['complaint_type']}” "
    f"with {int(top_issue['complaints'])} records."
)


with st.expander(
    "See complaint-type performance"
):

    type_display = type_summary.copy()

    type_display[
        "median_response_min"
    ] = type_display[
        "median_response_min"
    ].round(1)

    type_display[
        "median_resolution_hr"
    ] = type_display[
        "median_resolution_hr"
    ].round(2)

    st.dataframe(
        type_display,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================================
# OUTLET EXPLORER
# =========================================================

label("02 · Locate")
st.header("Move from company-wide to outlet-level.")

st.write(
    """
A high complaint count tells us where complaints appear
frequently in this dataset. It does not automatically mean
an outlet has a higher complaint rate, because total order
volume by outlet is not available.
"""
)


selected_outlet = st.selectbox(
    "Choose an outlet",
    sorted(df["outlet"].unique())
)

outlet_data = df[
    df["outlet"] == selected_outlet
].copy()


outlet_kpi = outlets[
    outlets["outlet"] == selected_outlet
].iloc[0]


o1, o2, o3, o4 = st.columns(4)

with o1:
    st.metric(
        "Complaints",
        f"{int(outlet_kpi['complaints']):,}"
    )

with o2:
    st.metric(
        "Median response",
        f"{outlet_kpi['median_response_min']:.0f} min"
    )

with o3:
    st.metric(
        "Median resolution",
        f"{outlet_kpi['median_resolution_hr']:.1f} hr"
    )

with o4:
    st.metric(
        "Expired cases",
        f"{int(outlet_kpi['expired_cases'])}"
    )


# =========================================================
# OUTLET ISSUE MIX
# =========================================================

outlet_mix = (
    outlet_data[
        "complaint_type"
    ]
    .value_counts()
    .rename_axis(
        "complaint_type"
    )
    .reset_index(
        name="complaints"
    )
)

st.subheader(
    f"What happens at {selected_outlet}?"
)

st.bar_chart(
    outlet_mix,
    x="complaint_type",
    y="complaints"
)


if len(outlet_mix) > 0:

    outlet_top_issue = outlet_mix.iloc[0]

    share = (
        outlet_top_issue["complaints"]
        / len(outlet_data)
        * 100
    )

    st.caption(
        f"“{outlet_top_issue['complaint_type']}” represents "
        f"{share:.1f}% of complaints recorded for "
        f"{selected_outlet} in this synthetic dataset."
)
st.divider()


# =========================================================
# RESPONSIBLE AREA
# =========================================================

label("03 · Trace")
st.header("Which operational areas recur?")

st.write(
    """
The responsible-area field can help trace where recurring
issues are associated operationally. It should be interpreted
as a diagnostic dimension, not as proof that an individual
or team caused a complaint.
"""
)


area_chart = (
    areas[
        [
            "responsible_area",
            "complaints"
        ]
    ]
    .set_index("responsible_area")
)

st.bar_chart(area_chart)


with st.expander(
    "See responsible-area summary"
):

    area_display = areas.copy()

    area_display[
        "median_resolution_hr"
    ] = area_display[
        "median_resolution_hr"
    ].round(2)

    st.dataframe(
        area_display,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# OUTLET × ISSUE HOTSPOTS
# =========================================================

st.subheader("Outlet × issue hotspots")

st.write(
    """
Instead of looking only at total complaints, this view
combines outlet and complaint type to identify recurring
operational patterns.
"""
)


hotspot_display = hotspots.copy()

hotspot_display[
    "median_resolution_hr"
] = hotspot_display[
    "median_resolution_hr"
].round(2)

hotspot_display[
    "expired_rate"
] = hotspot_display[
    "expired_rate"
].round(1)


st.dataframe(
    hotspot_display.head(20),
    use_container_width=True,
    hide_index=True
)


st.caption(
    "The table is ranked primarily by complaint volume. "
    "Expired rate is shown as additional context rather "
    "than being treated as proof of operational failure."
)


st.divider()


# =========================================================
# CASE EXPLORER
# =========================================================

label("04 · Inspect")
st.header("Follow one complaint from start to outcome.")

st.write(
    """
Aggregate metrics show patterns, but individual cases
help explain what those metrics actually represent.
"""
)


case_options = df[
    "complaint_id"
].tolist()

selected_case = st.selectbox(
    "Choose a complaint",
    case_options
)

case = df[
    df["complaint_id"] == selected_case
].iloc[0]


c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Response time",
        f"{case['response_minutes']:.0f} min"
    )

with c2:

    if pd.notna(
        case["resolution_hours"]
    ):
        resolution_text = (
            f"{case['resolution_hours']:.1f} hr"
        )
    else:
        resolution_text = "Not resolved"

    st.metric(
        "Resolution time",
        resolution_text
    )

with c3:
    st.metric(
        "Ticket status",
        case["ticket_status"]
    )


st.subheader("Case context")

case_context = pd.DataFrame({
    "Field": [
        "Complaint",
        "Brand",
        "Outlet",
        "Purchase channel",
        "Issue detail",
        "Responsible area",
        "Customer outcome"
    ],
    "Value": [
        case["complaint_type"],
        case["brand"],
        case["outlet"],
        case["purchase_channel"],
        case["issue_detail"],
        case["responsible_area"],
        case["customer_status"]
    ]
})

st.dataframe(
    case_context,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TIMELINE
# =========================================================

st.subheader("Case timeline")

st.write(
    f"""
**Complaint received**  
{case['complaint_timestamp']}

↓

**First response**  
{case['response_timestamp']}

↓

**Resolution**  
{
    case['resolve_timestamp']
    if pd.notna(case['resolve_timestamp'])
    else "No resolution timestamp"
}
"""
)


st.divider()


# =========================================================
# DIAGNOSTIC INSIGHT
# =========================================================

label("05 · Interpret")
st.header("From dashboard to operational question.")

st.write(
    """
The goal of this analysis is not simply to identify the
largest number on a dashboard. A useful diagnostic asks
whether several signals appear together.

For example:

- Does one complaint type repeatedly appear at the same outlet?
- Are those cases also slower to resolve?
- Do they frequently end as expired tickets?
- Does the same responsible area repeatedly appear?
- Is the pattern isolated or visible across multiple outlets?

Those questions provide a stronger basis for operational
investigation than complaint volume alone.
"""
)


# =========================================================
# IMPORTANT LIMITATION
# =========================================================

st.warning(
    "Complaint volume ≠ complaint rate. "
    "This dataset does not contain total order volume for "
    "each outlet, so the application cannot determine which "
    "outlet has the highest complaint rate."
)


# =========================================================
# EXPORT
# =========================================================

st.subheader("Download analytical dataset")

export_columns = [
    "complaint_id",
    "complaint_timestamp",
    "response_timestamp",
    "resolve_timestamp",
    "ticket_status",
    "brand",
    "outlet",
    "complaint_type",
    "issue_detail",
    "responsible_area",
    "response_minutes",
    "resolution_hours"
]

export_df = df[
    export_columns
].copy()

export_csv = (
    export_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    "Download analyzed complaint data",
    export_csv,
    "complaint_analysis.csv",
    "text/csv"
)


st.divider()


# =========================================================
# METHOD
# =========================================================

label("Method note")
st.header("Why no machine learning yet?")

st.write(
    """
This version intentionally focuses on descriptive and
diagnostic analytics.

Before building a predictive model, the analytical problem,
target variable, data quality, class distribution, and
business usefulness of the prediction should first be
established.

Adding machine learning without a defensible prediction
target would make the project more complex without
necessarily making it more useful.
"""
)


st.subheader("What could come next?")

st.write(
    """
With appropriate historical data, a later extension could
test whether complaint characteristics contain enough signal
to estimate the likelihood that a ticket becomes unresolved
or expired.

That would change the problem from diagnostic analytics
into supervised classification and would require separate
model validation.
"""
)


st.divider()

label(
    "Rizqi Aprilianes · Customer Experience / Operations Analytics"
)

st.caption(
    "Synthetic public portfolio reconstruction"
)
