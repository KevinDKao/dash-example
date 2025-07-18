import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from layouts import create_layout
from callbacks import register_callbacks

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    title="Modern Analytics Dashboard"
)

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
