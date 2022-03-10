from numpy.core.numeric import NaN
import dash
from dash import html,dcc
from dash.html import Label
from pandas.io.formats import style
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
)

df = pd.read_csv("SalesPrediction.csv")
df["Outlet_Size"].fillna(NaN)
df=df[1:500]
colors = {"background": "#011833", "text": "#7FDBFF"}



app.layout = html.Div(
    [
        html.H1(
            "My Dazzling Dashboard",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Outlet Type"),
                        dcc.Dropdown(
                            id="outlet-dropdown",
                            options=[
                                {"label": s, "value": s} for s in df.Outlet_Type.unique()
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Outlet Size"),
                        dcc.Dropdown(
                            id="size-dropdown",
                            options=[
                                {"label": y, "value": y} for y in df["Outlet_Size"].dropna().unique()
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="column",
        ),
        html.Div(dcc.Graph(id="Item Type vs Sales"), className="chart")
    ],
    className="container"        
)


@app.callback(
    Output("Item Type vs Sales", "figure"),
    Input("size-dropdown", "value"),
    Input("outlet-dropdown", "value"),
)
def update_figure(size, outlet_type):
    filtered_dataset = df[(df.Outlet_Type == outlet_type)]


    if outlet_type:
        filtered_dataset = filtered_dataset[filtered_dataset.Outlet_Size == size]

    fig=px.bar(
    filtered_dataset,
    x="Item_Identifier",
    y="Item_Outlet_Sales",
    color="Item_Type"
    )

    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)