# Copyright 2019 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(env):
    """Hook de inicialización para establecer la vista Gantt como acción por defecto al usuario demo."""
    user_demo = env.ref("base.user_demo", raise_if_not_found=False)
    if user_demo:
        action = env.ref("bryntum_gantt.open_gantt_pro", raise_if_not_found=False)
        if action:
            user_demo.sudo().write({"action_id": action.id})
