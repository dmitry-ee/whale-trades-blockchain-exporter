from . import (
    PrintCallback
)

class App():
    async def run(self):

        c = PrintCallback()
        c.processCallback("LOYCE")
