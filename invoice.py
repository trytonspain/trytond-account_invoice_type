# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
# This module changes the critieria in which tryton choosed if
# an invoice is either out_credit_note or not
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Invoice']

_TYPE = [
    ('out_invoice', 'Invoice'),
    ('in_invoice', 'Supplier Invoice'),
    ('out_credit_note', 'Credit Note'),
    ('in_credit_note', 'Supplier Credit Note'),
]


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'
    invoice_type = fields.Function(fields.Selection(_TYPE, 'Invoice Type'),
        'on_change_with_invoice_type')

    @fields.depends('type')
    def on_change_with_invoice_type(self, name=None):
        if all(l.amount <= 0 for l in self.lines):
            return '%s_credit_note' % self.type
        else:
            return '%s_invoice' % self.type

    def invoice_type_criteria(self):
        super(Invoice, self).invoice_type_criteria()
        if self.total_amount <= 0:
            return '_credit_note'
        return '_invoice'
