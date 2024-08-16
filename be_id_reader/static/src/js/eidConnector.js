/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useService, useBus } from "@web/core/utils/hooks";
import { session } from "@web/session";

export class EidController extends ListController {
   setup() {
      super.setup();

      this.rpc = useService("rpc");
      this.notification = useService("notification");
      this.company = useService("company");
      this.action = useService("action");
      
      this.busService = this.env.services.bus_service
      this.channel = "user-channel"
      this.notifiedSessions = new Set();
      
   }

   

   onMessage({ detail: notifications }) {
      console.log({ notifications });
      const payload = notifications
          .filter(notification => notification.type === 'notification');
          
      const userPaload = payload.map(notification => notification.payload.uid);

      if(userPaload == session.uid && !this.notifiedSessions.has(session.uid)) {
         this.notifiedSessions.add(session.uid);
         const successPayloads = payload.map(notification => notification.payload.success);    
         successPayloads.forEach(success => {
            if (success) {

               const partnerPayload = payload.map(notification => notification.payload.partner_id);                
               this.openPartnerFormView(partnerPayload[0]);
               
               this.notification.add("User created",
               {title: "Creation Success", type: "success"});
            
               
            } else {
               const message = payload.map(notification => notification.payload.message).join(', '); 
               this.notification.add(`User not created. Details: ${message}`,{title: "Creation Error", type: "danger"});
            }
            
         });
      }
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

         var uid = session.uid;
         
         var sid = await this.rpc("/sid");

         var endPoint = "/eid-user/create";
         var custom_scheme = `kinosteo://?uid=${uid}&cid=${cid}&key=${sid}&redirect_url=${url}${endPoint}`;

         this.busService.addChannel(this.channel);

         //without this the events are not detected
         this.busService.addEventListener("notification", this.onMessage.bind(this),{ passive: true });
         window.open(custom_scheme, '_blank');

         this.notification.add("Request in progress",{title: "Processing", type: "warning"});

      } 
   }

}

registry.category("views").add("eid_button_in_tree", {
   ...listView,
   Controller: EidController,
   buttonTemplate: "button_eid.ListView.Buttons",
});
