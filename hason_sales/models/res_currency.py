from odoo import models, api

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def amount_to_text_indian(self, amount):
        def _num_to_words(n):
            from num2words import num2words
            return num2words(n, lang='en_IN').title()

        amount_int = int(amount)
        amount_dec = int(round((amount - amount_int) * 100))

        words = _num_to_words(amount_int)
        if amount_dec > 0:
            words += f" And {_num_to_words(amount_dec)} Paise"

        return words
