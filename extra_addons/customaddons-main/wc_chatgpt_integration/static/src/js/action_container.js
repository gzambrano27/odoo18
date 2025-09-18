import { ActionContainer } from '@web/webclient/actions/action_container';
import { Component, xml, onWillDestroy, useState, onWillRender} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useSequential } from "@mail/utils/common/hooks";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";


ActionContainer.template = xml`
        <t t-name="web.ActionContainer">
          <div class="o_action_manager">
            <t t-if="info.Component" t-component="info.Component" className="'o_action'" t-props="info.componentProps" t-key="info.id"/>
          </div>
          <style type="text/css">
                .glow-on-hover {
                    width: 220px;
                    height: 50px;
                    border: none;
                    outline: none;
                    color: #fff;
                    background: #111;
                    cursor: pointer;
                    position: relative;
                    z-index: 0;
                    border-radius: 10px;
                }

                .glow-on-hover:before {
                    content: '';
                    background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
                    position: absolute;
                    top: -2px;
                    left:-2px;
                    background-size: 400%;
                    z-index: -1;
                    filter: blur(5px);
                    width: calc(100% + 4px);
                    height: calc(100% + 4px);
                    animation: glowing 20s linear infinite;
                    opacity: 0;
                    transition: opacity .3s ease-in-out;
                    border-radius: 10px;
                }

                .glow-on-hover:active {
                    color: #000
                }

                .glow-on-hover:active:after {
                    background: transparent;
                }

                .glow-on-hover:hover:before {
                    opacity: 1;

                }

                .glow-on-hover:after {
                    z-index: -1;
                    content: '';
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    background: #111;
                    left: 0;
                    top: 0;
                    border-radius: 10px;
                }

                @keyframes glowing {
                    0% { background-position: 0 0; }
                    50% { background-position: 400% 0; }
                    100% { background-position: 0 0; }
                }
          </style>
          <t t-if="this.state.is_valid_api_key">
              <button type="button" class="o-mail-ChatHub-bubbleBtn btn o-mail-ChatHub-optionsBtn fa fa-ellipsis-h bg-100 mt-1 glow-on-hover" style="margin-left:95%;margin-bottom:10px; height:45px !important; width:40px !important" t-on-click="() => this.onChatGpt(ev)">
                <img src="/wc_chatgpt_integration/static/description/chatgpt.png" style="height: 38px;" class="illustration_border" />
              </button>
          </t>
        </t>`;


patch(ActionContainer.prototype, {
    setup() {
        super.setup();
        this.action = useService("action");
        this.store = useState(useService("mail.store"));
        this.sequential = useSequential();

        this.state = useState({
            is_valid_api_key: false,
        });

        onWillRender(async () => {
            const res = await this.env.services.orm.call("discuss.channel", "check_api_key_and_model", [[]]);
            if (res.is_enable && res.is_valid_api_key){
                this.state.is_valid_api_key = true
            }
        });


    },

    async onChatGpt(ev) {
        if (this.Valid_api_model == false){
            return alert('Please Enter Valid Api Key Or Model.')
        }
        const domain = [
            ["parent_channel_id", "=", false],
            ["channel_type", "=", "channel"],
            ["is_chatgpt", "=", true],
            ["name", "ilike", 'ChatGpt'],
            ["channel_member_ids.partner_id", "=", user.partnerId],
        ];
        const fields = ["name"];

        const results = await this.sequential(async () => {
            const res = await this.env.services.orm.searchRead("discuss.channel", domain, fields, {
                limit: 10,
            });
            return res;
        });
        if (results.length == 0) {
            this.env.services.orm.call("discuss.channel", "channel_create_chatgpt", [
                'ChatGpt',
                this.store.internalUserGroupId,
            ]).then((data) => {
                const { Thread } = this.store.insert(data);
                const [channel] = Thread;
                channel.open();
            });
       }
       else{
            const data = await this.env.services.orm.call("discuss.channel", "channel_get_chatgpt", [], {
            partners_to: [user.partnerId],
            force_open: false,
            channel: results,
            });
            const { Thread } = this.store.insert(data);
            const [channel] = Thread;
            channel.open();
       }
    }
});
