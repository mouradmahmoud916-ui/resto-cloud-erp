from odoo import models, fields, api

class RestaurantRecipe(models.Model):
    _name = 'restaurant.recipe'
    _description = 'بطاقة تكلفة الوجبة'

    name = fields.Char(string='اسم الوجبة', required=True)
    sale_price = fields.Float(string='سعر البيع', required=True)
    total_cost = fields.Float(string='التكلفة المباشرة', compute='_compute_total_cost', store=True)
    food_cost_percentage = fields.Float(string='نسبة Food Cost %', compute='_compute_food_cost_pct', store=True)
    line_ids = fields.One2many('restaurant.recipe.line', 'recipe_id', string='المكونات')

    @api.depends('line_ids.subtotal_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = sum(line.subtotal_cost for line in rec.line_ids)

    @api.depends('total_cost', 'sale_price')
    def _compute_food_cost_pct(self):
        for rec in self:
            rec.food_cost_percentage = (rec.total_cost / rec.sale_price * 100) if rec.sale_price > 0 else 0.0


class RestaurantRecipeLine(models.Model):
    _name = 'restaurant.recipe.line'
    _description = 'مكون الوجبة'

    recipe_id = fields.Many2one('restaurant.recipe', string='الوجبة')
    ingredient_id = fields.Many2one('product.product', string='المادة الخام', required=True)
    quantity = fields.Float(string='الكمية', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='وحدة القياس')
    unit_cost = fields.Float(string='تكلفة الوحدة', related='ingredient_id.standard_price')
    subtotal_cost = fields.Float(string='إجمالي التكلفة', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal_cost = line.quantity * line.unit_cost
