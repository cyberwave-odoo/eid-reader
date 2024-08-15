from odoo import _, api, fields, models
from odoo.http import request
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    _sql_constraints = [
        (
            'unique_national_identification_number',
            'UNIQUE(national_identification_number,company_id)',
            'National identification number must be unique, check your users and archived users',
        ),
        (
            'unique_name_and_birthdate',
            'UNIQUE(name,date_of_birth,company_id)',
            'User with name and ad birthdate already exist, check your users and archived users',
        ),
    ]
    
    date_of_birth = fields.Date(string='Date of birth')
    national_identification_number = fields.Char(string='National identification number')
    nationality = fields.Char('Nationality')
    gender = fields.Selection([('M', 'Male'), ('F', 'Female'), ('other', 'Other')], string='Gender')
    location_of_birth = fields.Char('Location of birth')
    


    
    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Partners'),
            'template': '/be_id_reader/static/files/res_partner.xlsx'
        }]
        
        
    



    
        
    
    
    