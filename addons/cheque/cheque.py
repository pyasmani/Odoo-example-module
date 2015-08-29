# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Cheque(models.Model):
    # _inherit = 'x_cheque'
    _name = "cheque"
    _description = "cheque"
    _order = 'date_issue,sequence'
    bank_account_id = fields.Many2one('res.partner.bank', 'حساب بانکی')
    cheque_detail_id = fields.One2many('cheque_detail', 'cheque_id', 'برگه ها')
    sequence = fields.Integer(' سری دسته چک ')
    date_issue = fields.Date('تاریخ صدور')
    first_page_serial = fields.Integer(' شماره برگه اول ')
    pages = fields.Integer('تعدادبرگه')
    

    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        record=models.Model.create(self, vals)
        for i in xrange(vals['first_page_serial'],vals['first_page_serial']+vals['pages']):
            self.env['cheque_detail'].create({
            'cheque_id': record['id'],'sequence': i,'state': 'draft'
            })
        return record
    

class ChequeDetail(models.Model):
    _name = "cheque_detail"
    _description = "cheque detail"
    _order = 'sequence'
    cheque_id = fields.Many2one('cheque','دسته چک')
    sequence = fields.Integer(' شماره برگه چک ')
    amount = fields.Float('مبلغ')
    date_cheque = fields.Date(' تاریخ چک ')
    ref_no = fields.Integer(' شماره ارجاع ')
    state = fields.Selection(
    [('draft','New'), ('open','Started'),('done','Closed')],
    'State')

