from odoo import fields, models, api

class ContactsTemplate(models.Model):
    _inherit = "res.partner"

    # Custom fields added to Contacts form view
   
    group_name_ids = fields.Many2one('group.name', string='Group Name')
   
class GroupName(models.Model):
    _name = 'group.name'
    _description = 'Create Group Names'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name")


    