from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    scrap_reason_type = fields.Selection([
        ('spoilage', 'تلف مواد / انتهت الصلاحية'),
        ('prep_loss', 'هالك تجهيز وتحضير'),
        ('kitchen_error', 'خطأ مطبخ / طلب ملغى'),
    ], string='سبب الهالك', default='spoilage')

    cost_amount = fields.Float(string='قيمة الهالك المالية', compute='_compute_cost_amount', store=True)

    @api.depends('product_id', 'scrap_qty')
    def _compute_cost_amount(self):
        for rec in self:
            rec.cost_amount = rec.product_id.standard_price * rec.scrap_qty
