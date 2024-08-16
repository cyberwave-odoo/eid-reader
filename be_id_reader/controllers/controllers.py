# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from datetime import datetime
import logging
from .month import fix_date
import base64

_logger = logging.getLogger(__name__)


class Users(http.Controller):
    
    
    @http.route('/sid', methods=['POST'], auth='user', type="json", csrf=True)
    def get_session(self, **kw):
        uid = request.uid
        user = request.env['res.users'].browse(uid)
        session = user.sudo().get_access_key()
        return session

    def trigger_bus(self, user, data):
        data['uid'] = user.id
        request.env['bus.bus'].with_env(request.env(user=user))._sendone(channel='user-channel',notification_type="notification", message=data 
                    ) 
    # TODO manage exeptions : no card, already niss for this user, ...
    @http.route('/eid-user/create', auth='public', methods=['POST'], type="json", csrf=False)
    def eid_user_create(self, **kw):
        
        _logger.info(f"Request Params: {request.params}")
        card_data = json.loads(request.params['card_data'])
        iot_access_key = request.params['key']
        
        user = request.env['res.users'].sudo().browse(int(request.params['uid']))
        
        if not user.iot_access_key_valid(iot_access_key):
            _logger.info(f"Access key not valid: {iot_access_key}")
            data = {'success': False, 'message': "Error creating user, iot acces key not valid."}
            self.trigger_bus(user, data)
            return data
        
        if not card_data["message"] == "OK" :
            _logger.error(f"Error: in message data")
            data = {'success': False, 'message': card_data["message"]}
            self.trigger_bus(user, data)
            return data
        else :
            company_id = request.params['cid']
            photo_file = card_data["PHOTO_FILE"]
            
            if card_data["gender"] not in ["M", "F"] :
                gender = "other"
            else :
                gender = card_data["gender"]
            
            fixed_date = "1990-01-01"
            try :
                fixed_date = fix_date(card_data["date_of_birth"])
   
                vals = {
                    "national_identification_number" : card_data["national_number"],
                    "name" : card_data["firstnames"] + " " + card_data["surname"],
                    "gender" : gender,
                    "nationality" : card_data["nationality"],
                    "location_of_birth" : card_data["location_of_birth"],
                    "date_of_birth" : fixed_date,
                    "street" : card_data["address_street_and_number"],
                    "zip" : card_data["address_zip"],
                    "city" : card_data["address_municipality"],
                    "image_1920" : photo_file,
                    "company_id": company_id,
                }
                
                # Check if a partner with the same company_id and national_identification_number already exists
                existing_partner = user.env['res.partner'].search([
                    ('company_id', '=', int(company_id)),
                    ('national_identification_number', '=', str(card_data["national_number"]))
                ], limit=1)
                
                if existing_partner:
                    del vals['company_id']
                    existing_partner.with_env(request.env(user=user)).write(vals)
                    data = {'success': True, 'message': 'User updated', 'partner_id': existing_partner.id}
                    self.trigger_bus(user, data)
                else:
                    new_partner = user.env['res.partner'].with_env(request.env(user=user)).create(vals)
                    data = {'success': True, 'message': "User Created.", 'partner_id': new_partner.id}
                    self.trigger_bus(user, data)
            except Exception as ex:
                _logger.exception("Exception while creating user: %s", ex)
                data = {'success': False, 'message': "Error creating user."}
                self.trigger_bus(user, data)
            return data
            
        
        return request.params
