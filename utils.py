import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import numpy as np

# Define plotting and analysis functions
def plot_time_series():
    fig, axes = plt.subplots(4, 1, figsize=(16, 20))
    fig.suptitle('Polgolla Reservoir - Key Metrics Over Time', fontsize=16)

    axes[0].plot(df['DATE'], df['WATER_LEVEL(MSL)'], 'b-')
    axes[0].set_title('Water Level (MSL) Over Time')
    axes[0].set_ylabel('Water Level (MSL)')

    axes[1].plot(df['DATE'], df['STORAGE__PERCENTAGE'], 'g-')
    axes[1].set_title('Storage Percentage Over Time')
    axes[1].set_ylabel('Storage (%)')

    axes[2].plot(df['DATE'], df['INFLOW(MCM)'], 'r-', label='Inflow')
    axes[2].plot(df['DATE'], df['TOTAL_RELESE(MCM)'], 'c-', label='Release')
    axes[2].set_title('Inflow and Release Over Time')
    axes[2].set_ylabel('Volume (MCM)')
    axes[2].legend()

    axes[3].plot(df['DATE'], df['ENERGY(MWh)'], 'y-')
    axes[3].set_title('Energy Generation Over Time')
    axes[3].set_ylabel('Energy (MWh)')
    axes[3].set_xlabel('Date')

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    st.pyplot(fig)

def plot_rajarata_vs_victoriya():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['DATE'], df['RAJARATA_POWER_RELEASE(MCM)'], label='Rajarata Power Release (MCM)', marker='o')
    ax.plot(df['DATE'], df['VICTORIYA_SPILLWAY_RELEASE(MCM)'], label='Victoriya Spillway Release (MCM)', marker='x')
    ax.set_title('Rajarata vs Victoriya Releases Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Release (MCM)')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_monthly_inflow_vs_rajarata(df):
    """
    Plots monthly inflow versus Rajarata Power Release over multiple years.
    """
    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])
    # Create a 'Year-Month' column
    df['Year-Month'] = df['DATE'].dt.to_period('M')

    # Initialize the figure
    fig = go.Figure()

    # Loop through each year-month to add traces
    for period in df['Year-Month'].unique():
        period_data = df[df['Year-Month'] == period]
        fig.add_trace(go.Scatter(
            x=period_data['Year-Month'].astype(str),
            y=period_data['INFLOW(MCM)'],
            mode='lines+markers',
            name=f'Inflow {period}'
        ))
        fig.add_trace(go.Scatter(
            x=period_data['Year-Month'].astype(str),
            y=period_data['RAJARATA_POWER_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Rajarata Release {period}',
            line=dict(dash='dash')
        ))

    # Update the layout
    fig.update_layout(
        title='Monthly Inflow vs Rajarata Release (2000-2025)',
        xaxis_title='Year-Month',
        yaxis_title='Volume (MCM)',
        template='plotly_dark',
        width=1000,
        height=700,
        xaxis=dict(tickmode='array', tickvals=df['Year-Month'].astype(str).unique())
    )

    # Display the plot
    st.plotly_chart(fig)

def plot_monthly_inflow_vs_victoriya(df):
    """
    Plots monthly inflow versus Victoria Spillway Release over multiple years.
    """
    # Ensure 'DATE' is in datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])
    # Create a 'Year-Month' column
    df['Year-Month'] = df['DATE'].dt.to_period('M')

    # Initialize the figure
    fig = go.Figure()

    # Loop through each year-month to add traces
    for period in df['Year-Month'].unique():
        period_data = df[df['Year-Month'] == period]
        fig.add_trace(go.Scatter(
            x=period_data['Year-Month'].astype(str),
            y=period_data['INFLOW(MCM)'],
            mode='lines+markers',
            name=f'Inflow {period}'
        ))
        fig.add_trace(go.Scatter(
            x=period_data['Year-Month'].astype(str),
            y=period_data['VICTORIYA_SPILLWAY_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Victoria Release {period}',
            line=dict(dash='dash')
        ))

    # Update the layout
    fig.update_layout(
        title='Monthly Inflow vs Victoria Release (2000-2025)',
        xaxis_title='Year-Month',
        yaxis_title='Volume (MCM)',
        template='plotly_dark',
        width=1000,
        height=700,
        xaxis=dict(tickmode='array', tickvals=df['Year-Month'].astype(str).unique())
    )

    # Display the plot
    st.plotly_chart(fig)


# def plot_monthly_inflow_vs_rajarata():
#     fig = go.Figure()
#     for year in df['YEAR'].unique():
#         yearly_data = df[df['YEAR'] == year]
#         fig.add_trace(go.Scatter(
#             x=yearly_data['MONTH'],
#             y=yearly_data['INFLOW(MCM)'],
#             mode='lines+markers',
#             name=f'Inflow {year}'
#         ))
#         fig.add_trace(go.Scatter(
#             x=yearly_data['MONTH'],
#             y=yearly_data['RAJARATA_POWER_RELEASE(MCM)'],
#             mode='lines+markers',
#             name=f'Rajarata Release {year}',
#             line=dict(dash='dash')
#         ))
#     fig.update_layout(
#         title='Monthly Inflow vs Rajarata Release (2000-2025)',
#         xaxis_title='Month',
#         yaxis_title='Volume (MCM)',
#         template='plotly_dark',
#         width=1000,
#         height=700
#     )
#     st.plotly_chart(fig)

# def plot_monthly_inflow_vs_victoriya():
#     fig = go.Figure()
#     for year in df['YEAR'].unique():
#         yearly_data = df[df['YEAR'] == year]
#         fig.add_trace(go.Scatter(
#             x=yearly_data['MONTH'],
#             y=yearly_data['INFLOW(MCM)'],
#             mode='lines+markers',
#             name=f'Inflow {year}'
#         ))
#         fig.add_trace(go.Scatter(
#             x=yearly_data['MONTH'],
#             y=yearly_data['VICTORIYA_SPILLWAY_RELEASE(MCM)'],
#             mode='lines+markers',
#             name=f'Victoria Release {year}',
#             line=dict(dash='dash')
#         ))
#     fig.update_layout(
#         title='Monthly Inflow vs Victoria Release (2000-2025)',
#         xaxis_title='Month',
#         yaxis_title='Volume (MCM)',
#         template='plotly_dark',
#         width=1000,
#         height=700
#     )
#     st.plotly_chart(fig)
    
def plot_monthly_avg_releases():
    monthly_avg = df.groupby('MONTH')[['RAJARATA_POWER_RELEASE(MCM)', 'VICTORIYA_SPILLWAY_RELEASE(MCM)']].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_avg.plot(kind='bar', ax=ax)
    ax.set_title('Monthly Average Rajarata vs Victoriya Release (MCM)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Release (MCM)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

def plot_yearly_comparison():
    df_yearly = df.groupby('YEAR')[['RAJARATA_POWER_RELEASE(MCM)', 'VICTORIYA_SPILLWAY_RELEASE(MCM)']].sum().reset_index()
    fig, ax = plt.subplots(figsize=(14, 7))
    x = df_yearly['YEAR']
    ax.bar(x - 0.2, df_yearly['RAJARATA_POWER_RELEASE(MCM)'], width=0.4, label='Rajarata Power Release', color='skyblue')
    ax.bar(x + 0.2, df_yearly['VICTORIYA_SPILLWAY_RELEASE(MCM)'], width=0.4, label='Victoriya Spillway Release', color='orange')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Release (MCM)')
    ax.set_title('Comparison of Rajarata Power Release vs Victoriya Spillway Release (2000-2025)')
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=45)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

def display_correlation_matrix():
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    st.pyplot(fig)
    
    
    
def plot_seasonal_releases():
    seasons = ['Maha', 'First Inter-Monsoon', 'Second Inter-Monsoon', 'Yala']
    seasonal_data = df.groupby(['YEAR', 'SEASON']).agg({
        'RAJARATA_POWER_RELEASE(MCM)': 'sum',
        'VICTORIYA_SPILLWAY_RELEASE(MCM)': 'sum'
    }).reset_index()
    
    # Create columns for layout
    cols = st.columns(2)
    
    for i, season in enumerate(seasons):
        season_data = seasonal_data[seasonal_data['SEASON'] == season]
        fig = go.Figure()
        
        # Rajarata releases
        fig.add_trace(go.Scatter(
            x=season_data['YEAR'],
            y=season_data['RAJARATA_POWER_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Rajarata - {season}'
        ))
        
        # Victoria releases (dashed line)
        fig.add_trace(go.Scatter(
            x=season_data['YEAR'],
            y=season_data['VICTORIYA_SPILLWAY_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Victoria - {season}',
            line=dict(dash='dash')
        ))
        
        fig.update_layout(
            title=f'Seasonal Water Releases - {season}',
            xaxis_title='Year',
            yaxis_title='Total Release (MCM)',
            template='plotly_dark',
            width=800,
            height=600
        )
        
        # Display each plot in a separate column
        with cols[i % 2]:
            st.plotly_chart(fig)

def plot_inflow_vs_release():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Inflow vs Rajarata Release
    sns.regplot(ax=axes[0], x='INFLOW(MCM)', y='RAJARATA_POWER_RELEASE(MCM)', data=df, scatter_kws={'alpha':0.6})
    axes[0].set_title('Inflow vs Rajarata Power Release')
    axes[0].set_xlabel('Inflow (MCM)')
    axes[0].set_ylabel('Rajarata Power Release (MCM)')

    # Inflow vs Victoria Release
    sns.regplot(ax=axes[1], x='INFLOW(MCM)', y='VICTORIYA_SPILLWAY_RELEASE(MCM)', data=df, scatter_kws={'alpha':0.6})
    axes[1].set_title('Inflow vs Victoria Spillway Release')
    axes[1].set_xlabel('Inflow (MCM)')
    axes[1].set_ylabel('Victoria Spillway Release (MCM)')

    plt.tight_layout()
    st.pyplot(fig)
