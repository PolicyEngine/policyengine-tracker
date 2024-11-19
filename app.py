import streamlit as st
from atproto import Client
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="PolicyEngine Tracker", page_icon="📊", layout="wide"
)


class BlueskyStats:
    def __init__(self):
        self.client = Client()
        # Get credentials from secrets
        try:
            username = st.secrets["bluesky"]["username"]
            password = st.secrets["bluesky"]["password"]
            self.client.login(f"{username}.bsky.social", password)
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")

    def get_followers(self, handle):
        """Get follower count for a Bluesky handle"""
        try:
            profile = self.client.get_profile(f"{handle}.bsky.social")
            return {
                "handle": handle,
                "followers": profile.followers_count,
            }
        except Exception as e:
            st.error(f"Error fetching data for {handle}: {str(e)}")
            return None


def main():
    st.title("📊 PolicyEngine Tracker")
    st.markdown("Real-time follower tracking across Bluesky accounts")

    # Initialize Bluesky client
    bluesky = BlueskyStats()

    # List of Bluesky accounts to track (without .bsky.social)
    accounts = ["policyengine", "policyengineus", "policyengineuk"]

    # Create columns for metrics
    cols = st.columns(len(accounts))

    # Fetch and display current stats
    current_stats = []

    for acc, col in zip(accounts, cols):
        stats = bluesky.get_followers(acc)
        if stats:
            current_stats.append(stats)

            # Display follower count in card format
            col.metric(label=f"@{acc}", value=f"👥 {stats['followers']:,}")

    # Convert stats to DataFrame for visualization
    if current_stats:
        df = pd.DataFrame(current_stats)

        # Create bar chart of followers
        fig = px.bar(
            df,
            x="handle",
            y="followers",
            title="Follower Count by Account",
            labels={"handle": "Account", "followers": "Followers"},
            color_discrete_sequence=["#1f77b4"],  # Use a single blue color
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Followers",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Add timestamp
    st.caption(
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )


if __name__ == "__main__":
    main()
