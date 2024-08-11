from odoo import _, api, fields, models

class CardWizard(models.TransientModel):
    _name = 'card.reader.wizard'
    
    def get_eid_installer(self):

        return {
                'label': _('Import Eid Reader Installer'),
                'type': 'ir.actions.act_url', 
                'url': '/be_id_reader/static/files/eid_reader_installer.exe'
                }