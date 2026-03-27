# -*- coding: utf-8 -*-
{
    'name': 'CRM Partner Cliente Indiretto',
    'version': '17.0.1.0.0',
    'category': 'CRM',
    'summary': 'Estende il conteggio opportunità sul partner includendo il campo x_studio_cliente_indiretto',
    'description': """
        Questo modulo estende il modello res.partner per includere nel conteggio
        e nella visualizzazione delle opportunità anche quelle in cui il partner
        è impostato come cliente indiretto (campo x_studio_cliente_indiretto su crm.lead).
    """,
    'author': 'Custom',
    'depends': [
        'crm',
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
