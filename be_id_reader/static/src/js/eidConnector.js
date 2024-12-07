/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useService, useBus } from "@web/core/utils/hooks";


import { user } from "@web/core/user";
import { rpc } from "@web/core/network/rpc";

export class EidController extends ListController {

   setup() {
      super.setup();
      this.notification = useService("notification");
      this.company = useService("company");
      this.action = useService("action");

      this.busService = this.env.services.bus_service;
      console.log(this.busService);
      this.busService.subscribe("user-channel", (params) => {
         if (params.uid == user.userId) {
            
             if(params.type == 'success') {
                 this.openPartnerFormView(params.data.partner_id);
                 this.notification.add(params.data.message,
                    {title: "Import Success", type: params.type});
             }
             else {
              this.notification.add(`User not created. Details: ${params.data.message}`,{title: "Creation Error", type: params.type});
             }
         } 
     });
     
      
   }
   onWillStart() {
      
   }

   
   async openPartnerFormView(partnerId) {
      await this.action.doAction({
          name: 'res.partner.form',
          type: 'ir.actions.act_window',
          res_model: 'res.partner',
          view_mode: 'form',
          views: [[false, 'form']],
          res_id: partnerId,
          target: 'current',
      });
   }
   async OnClick() {

      // Eid software avalable here : https://eid.belgium.be/
      var platform = window.navigator.userAgent.toLowerCase()
      if (platform.match("windows") == undefined) {
         console.log("Platform not yet supported");
         this.notification.add("Only Windows is supported yet", {title: "OS Error", type: "danger"});

      }
      else {
         var url = new URL(window.location.href).origin;
         var cid = this.company.currentCompany.id;

         var uid = user.userId;

         var sid = await rpc("/sid");

         var endPoint = "/eid-user/create";

         var custom_scheme = `kinosteo://?uid=${uid}&cid=${cid}&key=${sid}&redirect_url=${url}${endPoint}`;

         window.open(custom_scheme, '_blank');

         this.notification.add("Request in progress",{title: "Processing", type: "warning"});

      } 
   }

}

registry.category("views").add("eid_button_in_list", {
   ...listView,
   Controller: EidController,
   buttonTemplate: "button_eid.ListView.Buttons",
});
