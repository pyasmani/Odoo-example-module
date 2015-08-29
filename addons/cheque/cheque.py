# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Cheque(models.Model):
    # _inherit = 'x_cheque'
    _name = "cheque"
    _description = "cheque"
    bank_account = fields.Many2one('res.partner.bank', 'حساب بانکی')
    cheque_detail = fields.One2many('cheque_detail', 'cheque_no', 'برگه ها')
    cheque_seri = fields.Integer(' سری دسته چک ')
    issue_date = fields.Date('تاریخ صدور')
    first_page_serial = fields.Integer(' شماره برگه اول ')
    pages = fields.Integer('تعدادبرگه')
    

    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        record=models.Model.create(self, vals)
        for vals['first_page_serial'] in xrange(vals['first_page_serial']+vals['pages']):
            self.env['cheque_detail'].create({
                'cheque_no': vals['first_page_serial'],
                'amount': 0,
                'cheque_date': fields.date.context_today(),
                'ref_no': 1,
                'status': 'وضعیت'})
        return record
    

class ChequeDetail(models.Model):
    _name = "cheque_detail"
    _description = "cheque detail"
    cheque_no = fields.Integer(' شماره برگه چک ')
    amount = fields.Float('مبلغ')
    cheque_date = fields.Date(' تاریخ چک ')
    ref_no = fields.Integer(' شماره ارجاع ')
    status = fields.Char('وضعیت')

