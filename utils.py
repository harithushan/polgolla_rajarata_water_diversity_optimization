import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st

def plot_time_series(df):
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

def plot_rajarata_vs_victoriya(df):
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


def plot_inflow_vs_release_dam(df, year_range, release_col, title):
    
    
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    df['Year-Month'] = df['DATE'].dt.strftime('%Y-%m')

    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['Year-Month'],
        y=filtered_df['INFLOW(MCM)'],
        mode='lines+markers',
        name='Inflow'
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['Year-Month'],
        y=filtered_df[release_col],
        mode='lines+markers',
        name=title.split('vs ')[-1].strip(),
        line=dict(dash='dash')
    ))
    
    if release_col =="RAJARATA_POWER_RELEASE(MCM)":

        # max reference lines
        fig.add_shape(type="line",
                    x0=filtered_df['Year-Month'].min(), x1=filtered_df['Year-Month'].max(),
                    y0=145.152, y1=145.152,
                    line=dict(color="red", width=2, dash="dot"))
        
        fig.add_shape(type="line",
                    x0=filtered_df['Year-Month'].min(), x1=filtered_df['Year-Month'].max(),
                    y0=72.576, y1=72.576,
                    line=dict(color="blue", width=2, dash="dot"))

        #min reference lines
        fig.add_annotation(
            x=filtered_df['Year-Month'].max(), y=145.152,
            text="Normal Max Flow (145.152 MCM)",
            showarrow=False,
            font=dict(color="red", size=12),
            xanchor="left"
        )

        fig.add_annotation(
            x=filtered_df['Year-Month'].max(), y=72.576,
            text="Minimum Flow (72.576 MCM)",
            showarrow=False,
            font=dict(color="blue", size=12),
            xanchor="left"
        )

    fig.update_layout(
        title=f'{title} ({year_range[0]}-{year_range[1]})',
        xaxis_title='Year-Month',
        yaxis_title='Volume (MCM)',
        template='plotly_white',#'plotly_dark',
        width=1000,
        height=700,
        xaxis=dict(type='category', tickangle=45)
    )

    st.plotly_chart(fig)
def plot_filtered_inflow_vs_release(df, year_range, release_col, title):
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    df['Year-Month'] = df['DATE'].dt.strftime('%Y-%m')

    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    filtered_df = filtered_df[(filtered_df['INFLOW(MCM)'] > 72.576) & (filtered_df[release_col] < 72.576)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['Year-Month'],
        y=filtered_df['INFLOW(MCM)'],
        mode='lines+markers',
        name='Inflow (> 72.576 MCM)',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['Year-Month'],
        y=filtered_df[release_col],
        mode='lines+markers',
        name=f"{title.split('vs ')[-1].strip()} (< 72.576 MCM)",
        line=dict(dash='dash', color='green')
    ))

    fig.add_shape(type="line",
                  x0=filtered_df['Year-Month'].min(), x1=filtered_df['Year-Month'].max(),
                  y0=145.152, y1=145.152,
                  line=dict(color="red", width=2, dash="dot"))
    
    fig.add_shape(type="line",
                  x0=filtered_df['Year-Month'].min(), x1=filtered_df['Year-Month'].max(),
                  y0=72.576, y1=72.576,
                  line=dict(color="black", width=2, dash="dot"))

    fig.add_annotation(
        x=filtered_df['Year-Month'].max(), y=145.152,
        text="Normal Max Flow (145.152 MCM)",
        showarrow=False,
        font=dict(color="red", size=12),
        xanchor="left"
    )

    fig.add_annotation(
        x=filtered_df['Year-Month'].max(), y=72.576,
        text="Threshold Flow (72.576 MCM)",
        showarrow=False,
        font=dict(color="black", size=12),
        xanchor="left"
    )

    fig.update_layout(
        title=f'{title} ({year_range[0]}-{year_range[1]}) - Filtered',
        xaxis_title='Year-Month',
        yaxis_title='Volume (MCM)',
        template='plotly_white', 
        width=1000,
        height=700,
        xaxis=dict(type='category', tickangle=45)
    )

    st.plotly_chart(fig)

# def plot_inflow_vs_release_dam(df, year_range, release_col, title):
#     df['DATE'] = pd.to_datetime(df['DATE'])
#     df['Year'] = df['DATE'].dt.year
#     df['Month'] = df['DATE'].dt.month
#     df['Year-Month'] = df['DATE'].dt.strftime('%Y-%m')

#     filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

#     fig = go.Figure()

#     # Plot inflow data
#     fig.add_trace(go.Scatter(
#         x=filtered_df['Year-Month'],
#         y=filtered_df['INFLOW(MCM)'],
#         mode='lines+markers',
#         name='Inflow'
#     ))

#     # Plot release data
#     fig.add_trace(go.Scatter(
#         x=filtered_df['Year-Month'],
#         y=filtered_df[release_col],
#         mode='lines+markers',
#         name=title.split('vs ')[-1].strip(),
#         line=dict(dash='dash')
#     ))

#     fig.update_layout(
#         title=f'{title} ({year_range[0]}-{year_range[1]})',
#         xaxis_title='Year-Month',
#         yaxis_title='Volume (MCM)',
#         template='plotly_dark',
#         width=1000,
#         height=700,
#         xaxis=dict(type='category', tickangle=45)
#     )

#     st.plotly_chart(fig)

def plot_monthly_inflow_vs_rajarata(df, year_range):
    """
    Plots monthly inflow versus Rajarata Power Release for a selected year range.
    """
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    fig = go.Figure()

    for year in filtered_df['Year'].unique():
        year_data = filtered_df[filtered_df['Year'] == year]
        fig.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['INFLOW(MCM)'],
            mode='lines+markers',
            name=f'Inflow {year}'
        ))
        fig.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['RAJARATA_POWER_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Rajarata Release {year}',
            line=dict(dash='dash')
        ))

    fig.update_layout(
        title=f'Monthly Inflow vs Rajarata Release ({year_range[0]}-{year_range[1]})',
        xaxis_title='Month',
        yaxis_title='Volume (MCM)',
        template='plotly_dark',
        width=1000,
        height=700,
        xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
    )

    st.plotly_chart(fig)

def plot_monthly_inflow_vs_victoriya(df, year_range):
    """
    Plots monthly inflow versus Victoria Spillway Release for a selected year range.
    """
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    fig = go.Figure()

    # Loop through selected years
    for year in filtered_df['Year'].unique():
        year_data = filtered_df[filtered_df['Year'] == year]
        fig.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['INFLOW(MCM)'],
            mode='lines+markers',
            name=f'Inflow {year}'
        ))
        fig.add_trace(go.Scatter(
            x=year_data['Month'],
            y=year_data['VICTORIYA_SPILLWAY_RELEASE(MCM)'],
            mode='lines+markers',
            name=f'Victoria Release {year}',
            line=dict(dash='dash')
        ))

    fig.update_layout(
        title=f'Monthly Inflow vs Victoria Release ({year_range[0]}-{year_range[1]})',
        xaxis_title='Month',
        yaxis_title='Volume (MCM)',
        template='plotly_dark',
        width=1000,
        height=700,
        xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
    )

    st.plotly_chart(fig)


    
def plot_monthly_avg_releases(df):
    monthly_avg = df.groupby('MONTH')[['RAJARATA_POWER_RELEASE(MCM)', 'VICTORIYA_SPILLWAY_RELEASE(MCM)']].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_avg.plot(kind='bar', ax=ax)
    ax.set_title('Monthly Average Rajarata vs Victoriya Release (MCM)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Release (MCM)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

def plot_yearly_comparison(df):
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

def display_correlation_matrix(df):
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    st.pyplot(fig)
    
    
    
def plot_seasonal_releases(df):
    seasons = ['Maha', 'First Inter-Monsoon', 'Second Inter-Monsoon', 'Yala']
    seasonal_data = df.groupby(['YEAR', 'SEASON']).agg({
        'RAJARATA_POWER_RELEASE(MCM)': 'sum',
        'VICTORIYA_SPILLWAY_RELEASE(MCM)': 'sum'
    }).reset_index()
    
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
        
        with cols[i % 2]:
            st.plotly_chart(fig)

def plot_inflow_vs_release(df):
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
