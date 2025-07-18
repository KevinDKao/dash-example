from dash import Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def register_callbacks(app):
    """Register all dashboard callbacks"""
    
    @app.callback(
        [Output('sales-chart', 'figure'),
         Output('revenue-chart', 'figure'),
         Output('pie-chart', 'figure')],
        [Input('sales-chart', 'id')]  # Dummy input to trigger initial load
    )
    def update_charts(_):
        """Update charts with fresh data"""
        # Generate new dummy data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        sales_data = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.normal(1000, 200, len(dates)).cumsum(),
            'Revenue': np.random.normal(15000, 3000, len(dates)).cumsum(),
            'Orders': np.random.poisson(50, len(dates)).cumsum()
        })
        
        regions_data = pd.DataFrame({
            'Region': ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'],
            'Sales': [45000, 38000, 52000, 15000, 12000],
            'Market Share': [28, 23, 32, 9, 8]
        })
        
        # Sales chart
        sales_fig = go.Figure()
        sales_fig.add_trace(go.Scatter(
            x=sales_data['Date'],
            y=sales_data['Sales'],
            mode='lines',
            name='Sales',
            line=dict(color='#00d4ff', width=3),
            fill='tonexty'
        ))
        
        sales_fig.update_layout(
            title="Cumulative Sales Over Time",
            xaxis_title="Date",
            yaxis_title="Sales",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='white'),
            title_font=dict(size=20, color='white'),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Revenue chart
        revenue_fig = go.Figure()
        revenue_fig.add_trace(go.Scatter(
            x=sales_data['Date'],
            y=sales_data['Revenue'],
            mode='lines',
            name='Revenue',
            line=dict(color='#ff6b6b', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.3)'
        ))
        
        revenue_fig.update_layout(
            title="Cumulative Revenue",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='white'),
            title_font=dict(size=20, color='white'),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Pie chart
        pie_fig = px.pie(
            regions_data, 
            values='Sales', 
            names='Region',
            title="Sales by Region"
        )
        pie_fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(colors=['#00d4ff', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
        )
        pie_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=20, color='white'),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return sales_fig, revenue_fig, pie_fig
