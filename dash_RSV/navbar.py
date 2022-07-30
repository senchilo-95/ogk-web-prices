import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
           children=[
                dbc.NavItem(dbc.NavLink("Цена продажи на РСВ", active=True, href="/app")),
		        dbc.NavItem(dbc.NavLink("Потребление по ОЭС", active=True, href="/app_consum")),
                    ],
        color="rgb(87, 134, 189)",
    dark=True)
    return navbar