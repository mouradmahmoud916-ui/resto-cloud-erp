from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_food_cost = fields.Float(string='إجمالي تكلفة المبيعات COGS', compute='_compute_order_food_cost', store=True)

    @api.depends('lines.product_id', 'lines.qty')
    def _compute_order_food_cost(self):
        for order in self:
            cost = 0.0
            for line in order.lines:
                recipe = self.env['restaurant.recipe'].search([('name', '=', line.product_id.name)], limit=1)
                if recipe:
                    cost += recipe.total_cost * line.qty
                else:
                    cost += line.product_id.standard_price * line.qty
            order.total_food_cost = cost


class AccountMove(models.Model):
    _inherit = 'account.move'

    restaurant_cost_center = fields.Selection([
        ('kitchen', 'المطبخ الرئيسي'),
        ('bar', 'المشروبات / البار'),
        ('hall', 'الصالات والخدمة'),
    ], string='مركز التكلفة للمطعم')
