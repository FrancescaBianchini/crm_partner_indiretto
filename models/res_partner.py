# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    opportunity_count = fields.Integer(
        compute='_compute_opportunity_count',
        string='Opportunità',
    )

    def _compute_opportunity_count(self):
        """
        Override del metodo nativo di crm per includere nel conteggio
        anche le opportunità dove il partner è impostato come
        x_studio_cliente_indiretto, oltre al classico partner_id.
        """
        Lead = self.env['crm.lead']

        # Recuperiamo tutti i lead rilevanti in una singola query
        # raggruppando per evitare N+1 query
        leads_direct = Lead._read_group(
            domain=[('partner_id', 'in', self.ids)],
            groupby=['partner_id'],
            aggregates=['__count'],
        )
        leads_indirect = Lead._read_group(
            domain=[('x_studio_cliente_indiretto', 'in', self.ids)],
            groupby=['x_studio_cliente_indiretto'],
            aggregates=['__count'],
        )

        # Costruiamo dizionari {partner_id: count}
        direct_map = {partner.id: count for partner, count in leads_direct}
        indirect_map = {partner.id: count for partner, count in leads_indirect}

        for partner in self:
            direct = direct_map.get(partner.id, 0)
            indirect = indirect_map.get(partner.id, 0)

            # Recuperiamo gli id dei lead in comune per evitare
            # di contare due volte le opportunità dove il partner
            # compare sia come partner_id che come cliente indiretto
            overlap_count = Lead.search_count([
                ('partner_id', '=', partner.id),
                ('x_studio_cliente_indiretto', '=', partner.id),
            ])

            partner.opportunity_count = direct + indirect - overlap_count

    def action_view_opportunity(self):
        """
        Override dell'action che si apre cliccando lo smart button.
        Estende il domain per mostrare sia le opportunità con partner_id
        che quelle con x_studio_cliente_indiretto uguale al partner corrente.
        """
        action = super().action_view_opportunity()

        # Override del domain: OR tra partner diretto e cliente indiretto
        action['domain'] = [
            '|',
            ('partner_id', '=', self.id),
            ('x_studio_cliente_indiretto', '=', self.id),
        ]

        # Puliamo eventuale context che potrebbe forzare
        # un domain più restrittivo impostato dall'action originale
        ctx = action.get('context', {})
        if isinstance(ctx, dict):
            ctx.pop('default_partner_id', None)
            action['context'] = ctx

        return action
