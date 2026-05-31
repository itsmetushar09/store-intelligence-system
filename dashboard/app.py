import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")

        if response.status_code == 200:
            return response.json()

        st.error(f"API Error ({endpoint}): {response.status_code}")
        return {}

    except Exception as e:
        st.error(f"Cannot connect to API: {e}")
        return {}


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Store Intelligence Dashboard")

# --------------------------------------------------
# METRICS
# --------------------------------------------------

metrics = fetch_data("/metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Entries",
        metrics.get("entries", metrics.get("total_entries", 0))
    )

with col2:
    st.metric(
        "Exits",
        metrics.get("exits", metrics.get("total_exits", 0))
    )

with col3:
    st.metric(
        "Unique Visitors",
        metrics.get("unique_visitors", 0)
    )

st.divider()

# --------------------------------------------------
# CONVERSION FUNNEL
# --------------------------------------------------

st.subheader("📈 Conversion Funnel")

funnel = fetch_data("/funnel")

if funnel:
    funnel_df = pd.DataFrame(
        {
            "Metric": [
                "Entered Store",
                "Visited Billing"
            ],
            "Count": [
                funnel.get("entered_store", 0),
                funnel.get("visited_billing", 0)
            ]
        }
    )

    st.dataframe(
        funnel_df,
        use_container_width=True
    )

    st.metric(
        "Conversion Rate (%)",
        funnel.get("conversion_rate", 0)
    )

st.divider()

# --------------------------------------------------
# ZONE ANALYTICS
# --------------------------------------------------

st.subheader("🛍️ Zone Intelligence")

analytics = fetch_data("/analytics")

if analytics:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Most Popular Zone",
            analytics.get(
                "most_popular_zone",
                "N/A"
            )
        )

    with col2:
        st.metric(
            "Tracked Zones",
            len(
                analytics.get(
                    "zone_visits",
                    {}
                )
            )
        )

    zone_visits = analytics.get(
        "zone_visits",
        {}
    )

    if zone_visits:

        zone_df = pd.DataFrame(
            {
                "Zone": zone_visits.keys(),
                "Visits": zone_visits.values()
            }
        )

        st.bar_chart(
            zone_df.set_index("Zone")
        )

st.divider()

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

st.subheader("🔥 Store Heatmap")

heatmap = fetch_data("/heatmap")

if heatmap:

    heatmap_df = pd.DataFrame(
        {
            "Zone": heatmap.keys(),
            "Activity": heatmap.values()
        }
    )

    st.bar_chart(
        heatmap_df.set_index("Zone")
    )

st.divider()

# --------------------------------------------------
# ANOMALIES
# --------------------------------------------------

st.subheader("⚠️ Anomaly Detection")

anomalies = fetch_data("/anomalies")

if anomalies:

    anomaly_list = anomalies.get(
        "anomalies",
        []
    )

    if anomaly_list:

        for anomaly in anomaly_list:
            st.warning(anomaly)

    else:
        st.success(
            "No anomalies detected."
        )

st.divider()

# --------------------------------------------------
# EVENTS
# --------------------------------------------------

st.subheader("📋 Event Stream")

events = fetch_data("/events")

if events:

    df = pd.DataFrame(events)

    st.dataframe(
        df,
        use_container_width=True
    )