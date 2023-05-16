# from app import app, cli
from app import create_app
from app.models import (
    Agendamento,
    Cliente,
)


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'Agendamento': Agendamento,
        'Cliente': Cliente,

    }
