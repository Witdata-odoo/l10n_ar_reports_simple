# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ARCAActivity(models.Model):
    _name = "l10n_ar.arca.activity"
    _description = "ARCA Activity"
    _order = "code"

    code = fields.Char(string="Código", required=True, help="Código de actividad")
    name = fields.Char(string="Nombre", required=True, help="Descripción de la actividad")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'El código de actividad debe ser único.'),
        ('code_length', 'CHECK(LENGTH(code) <= 6)', 'El código de actividad no puede tener más de 6 caracteres.'),
    ]

    @api.depends("code", "name")
    @api.depends_context("formatted_display_name")
    def _compute_display_name(self):
        for activity in self:
            if activity.env.context.get("formatted_display_name"):
                activity.display_name = f"--{activity.code}--\t{activity.name}"
            else:
                activity.display_name = "%s - %s" % (activity.code, activity.name)

    def name_get(self):
        result = []
        for activity in self:
            if self.env.context.get("formatted_display_name"):
                name = f"--{activity.code}--\t{activity.name}"
            else:
                name = "%s - %s" % (activity.code, activity.name)
            result.append((activity.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
