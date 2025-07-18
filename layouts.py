import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Generate dummy data
def generate_dummy_data():
    """Generate sample data for the dashboard"""
    # Sales data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    sales_data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.normal(1000, 200, len(dates)).cumsum(),
        'Revenue': np.random.normal(15000, 3000, len(dates)).cumsum(),
        'Orders': np.random.poisson(50, len(dates)).cumsum()
    })
    
    # Product performance table
    products_data = pd.DataFrame({
        'Product': ['iPhone 15', 'MacBook Pro', 'iPad Air', 'AirPods Pro', 'Apple Watch'],
        'Sales': [1250, 890, 567, 2100, 1450],
        'Revenue': [1249000, 1780000, 340000, 525000, 580000],
        'Growth': ['+12.5%', '+8.9%', '-2.1%', '+15.7%', '+6.3%']
    })
    
    # Regional data
    regions_data = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'],
        'Sales': [45000, 38000, 52000, 15000, 12000],
        'Market Share': [28, 23, 32, 9, 8]
    })
    
    return sales_data, products_data, regions_data

def create_glass_card(children, title=None, className=""):
    """Create a glass morphism card component"""
    card_content = []
    
    if title:
        card_content.append(
            html.H4(title, className="card-title mb-3")
        )
    
    if isinstance(children, list):
        card_content.extend(children)
    else:
        card_content.append(children)
    
    return html.Div(
        card_content,
        className=f"glass-card {className}"
    )

def create_metric_card(title, value, change, icon):
    """Create a metric card with glass effect"""
    return create_glass_card([
        html.Div([
            html.I(className=f"fas {icon} metric-icon"),
            html.Div([
                html.H3(value, className="metric-value"),
                html.P(title, className="metric-title"),
                html.Span(change, className="metric-change positive" if '+' in change else "metric-change negative")
            ])
        ], className="metric-content")
    ], className="metric-card")

def create_charts():
    """Create the charts for the dashboard"""
    sales_data, products_data, regions_data = generate_dummy_data()
    
    # Cumulative sales line chart
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
        showlegend=False
    )
    
    # Revenue area chart
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
        showlegend=False
    )
    
    # Regional pie chart
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
        title_font=dict(size=20, color='white')
    )
    
    return sales_fig, revenue_fig, pie_fig

def create_data_table():
    """Create a modern data table"""
    _, products_data, _ = generate_dummy_data()
    
    return dash_table.DataTable(
        data=products_data.to_dict('records'),
        columns=[
            {"name": "Product", "id": "Product"},
            {"name": "Sales", "id": "Sales", "type": "numeric", "format": {"specifier": ","}},
            {"name": "Revenue", "id": "Revenue", "type": "numeric", "format": {"specifier": "$,"}},
            {"name": "Growth", "id": "Growth"}
        ],
        style_cell={
            'backgroundColor': 'rgba(255, 255, 255, 0.1)',
            'color': 'white',
            'border': '1px solid rgba(255, 255, 255, 0.2)',
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Inter, sans-serif'
        },
        style_header={
            'backgroundColor': 'rgba(255, 255, 255, 0.2)',
            'fontWeight': 'bold',
            'border': '1px solid rgba(255, 255, 255, 0.3)'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(255, 255, 255, 0.05)'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': 'rgba(255, 255, 255, 0.9)',
                'color': 'black'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(255, 255, 255, 0.9)',
                'color': 'black'
            }
        ],
        id='products-table'
    )

def create_layout():
    """Create the main dashboard layout"""
    sales_fig, revenue_fig, pie_fig = create_charts()
    
    return html.Div([
        # Header
        html.Div([
            html.H1("Analytics Dashboard", className="dashboard-title"),
            html.P("Real-time insights and performance metrics", className="dashboard-subtitle")
        ], className="header"),
        
        # Metrics Row
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_metric_card("Total Sales", "156K", "+12.5%", "fa-chart-line")
                ], width=3),
                dbc.Col([
                    create_metric_card("Revenue", "$2.4M", "+8.9%", "fa-dollar-sign")
                ], width=3),
                dbc.Col([
                    create_metric_card("Orders", "3,247", "+15.7%", "fa-shopping-cart")
                ], width=3),
                dbc.Col([
                    create_metric_card("Conversion", "3.8%", "+2.1%", "fa-percentage")
                ], width=3)
            ], className="mb-4")
        ]),
        
        # Charts Row
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_glass_card([
                        dcc.Graph(figure=sales_fig, id='sales-chart')
                    ])
                ], width=8),
                dbc.Col([
                    create_glass_card([
                        dcc.Graph(figure=pie_fig, id='pie-chart')
                    ])
                ], width=4)
            ], className="mb-4")
        ]),
        
        # Second Charts Row
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_glass_card([
                        dcc.Graph(figure=revenue_fig, id='revenue-chart')
                    ])
                ], width=12)
            ], className="mb-4")
        ]),
        
        # Data Table Row
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_glass_card([
                        html.H4("Product Performance", className="mb-3"),
                        create_data_table()
                    ])
                ], width=12)
            ])
        ])
        
    ], className="dashboard-container")
