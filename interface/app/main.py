
from flet import *
import flet
from routes import navigation
from paes import App



def main(page: Page):
    page.update()
    page.scroll = flet.ScrollMode.ALWAYS

    navigation(page)


app(target=main)





