/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { rpc } from "@web/core/network/rpc";
import { onWillUnmount } from "@odoo/owl";

export class EidController extends ListController {

    setup() {
        super.setup();
        this.notification = useService("notification");
        this.company = useService("company");
        this.action = useService("action");
        this.busService = this.env.services.bus_service;
        this.collaborationChannelName = "user-channel";
        this.collaborationBusListener = this._onBusNotification.bind(this);

        // Subscribe to bus service and add channel
        this.busService.subscribe(this.collaborationChannelName, this.collaborationBusListener);
        this.busService.addChannel(this.collaborationChannelName);

        // Unsubscribe on component destruction
        onWillUnmount(() => this._cleanupBus());
    }

    _cleanupBus() {
        this.busService.unsubscribe(this.collaborationChannelName, this.collaborationBusListener);
        this.busService.deleteChannel(this.collaborationChannelName);
    }

    _onBusNotification(payload) {
        if (payload.uid === user.userId) {
            if (payload.type === 'success') {
                this.openPartnerFormView(payload.data.partner_id);
                this.notification.add(payload.data.message, { title: "Import Success", type: payload.type });
            } else {
                this.notification.add(`User not created. Details: ${payload.data.message}`, { title: "Creation Error", type: payload.type });
            }
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
        const platform = window.navigator.userAgent.toLowerCase();
        if (!platform.includes("windows")) {
            console.log("Platform not yet supported");
            this.notification.add("Only Windows is supported yet", { title: "OS Error", type: "danger" });
        } else {
            const url = new URL(window.location.href).origin;
            const cid = this.company.currentCompany.id;
            const uid = user.userId;
            const sid = await rpc("/sid");
            const endPoint = "/eid-user/create";
            const customScheme = `kinosteo://?uid=${uid}&cid=${cid}&key=${sid}&redirect_url=${url}${endPoint}`;

            window.open(customScheme, '_blank');
            this.notification.add("Request in progress", { title: "Processing", type: "warning" });
        }
    }
}

registry.category("views").add("eid_button_in_list", {
    ...listView,
    Controller: EidController,
    buttonTemplate: "button_eid.ListView.Buttons",
});

