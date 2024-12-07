from odoo import _, api, fields, models
import uuid

class resPartner(models.Model):
    _inherit = 'res.users'
    
    iot_access_key = fields.Char('Session Key')
    iot_access_key_timestamp = fields.Datetime('iot_access_key_timestamp')
    
    def get_access_key(self):
        self.iot_access_key = str(uuid.uuid4())
        self.iot_access_key_timestamp = fields.Datetime.now()
        return self.iot_access_key   
    
    def iot_access_key_valid(self, access_key):
        validity_time = 30
        if not self.iot_access_key or not self.iot_access_key_timestamp:
            return False
        current_time = fields.Datetime.now()
        
        if self.iot_access_key == access_key and (current_time - self.iot_access_key_timestamp).total_seconds() <= validity_time:
            
            return True
        return False