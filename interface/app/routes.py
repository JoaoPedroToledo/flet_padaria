from flet import *
from paes import App

from table import home
def navigation(page: Page):

    page.title="Controle café da manhã"

    app_paes = App()
    app_cafe = App()

    

    #home
    def route_changes(e):
        page.views.clear()
        page.scroll = "always"

        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title=Text('Home'), bgcolor='blue'),
                    Text(value='Controle café da manhã', size=30),
                    
                    ElevatedButton(text='Pedidos de pães', on_click=lambda _: page.go('/paes')),
                    ElevatedButton(text='Pedidos de cafés', on_click=lambda _: page.go('/cafe')), 
                    home,
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )


        #paes
        if page.route=='/paes':
            page.views.append(
                View(
                    route='/paes',
                    controls=[
                        AppBar(title=Text('Pães'), bgcolor='blue'), app_paes
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        #cafe
        if page.route=='/cafe':
            page.views.append(
                View(
                    route='/cafe',
                    controls=[
                        AppBar(title=Text('Café'), bgcolor='blue'), app_paes
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        page.update()


    def view_pop(e):
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_changes
    page.on_view_pop = view_pop
    page.go(page.route)


target = navigation