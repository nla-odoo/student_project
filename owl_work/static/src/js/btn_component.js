odoo.define('owl_work.btn_component', function(require){
    "use strict";

    var session = require('web.session');
    var WebsiteLivechat = require('im_livechat.model.WebsiteLivechat');
    var WebsiteLivechatMessage = require('im_livechat.model.WebsiteLivechatMessage');
    var WebsiteLivechatWindow = require('im_livechat.WebsiteLivechatWindow');
    var rpc = require('web.rpc');
         
    require('web.dom_ready');

    const { Component, useState, hooks } = owl;
    const { xml } = owl.tags;

    class OwlChat extends Component {

        static template = xml`
            <div>
                <div class="d-flex p-2 justify-content-center">
                    <input id="txt_chat_input" type="text" t-on-keyup="addChat"/>
                    <input type="submit" t-on-click="_sendChat"/>
                </div>
                <center><div id="chat_div" style="display: block;"></div></center>
            </div>
        `;

        addChat(ev) {
            if (ev.keyCode === 13) {
                this._sendChat();
            }
        }

        _sendChat() {
            const tci = document.querySelector('#txt_chat_input');
            const chat_div = document.querySelector('#chat_div');
            const chat_lbl = document.createElement('label');
            chat_lbl.setAttribute('style', 'display: block');
            chat_lbl.textContent = tci.value;
            this._sendChatToOther(tci.value);
            chat_div.appendChild(chat_lbl);
            tci.value = "";
        }

        _sendChatToOther(chat) {
            return session
            .rpc('/mail/chat_post', {uuid: 1, message_content: chat})
            .then(function (messageId) {
                if (!messageId) {
                    debugger;
                }
            });
        }
    }

    class OwlWork extends Component{
        static template = xml`
            <div id="chat_btn" class="d-flex p-2 justify-content-center">
                <button id="btnstyle" t-on-click="_onClickButton">
                    Have a Question? Chat with us...
                 </button>
            </div>
        `;
        state = useState({ value: "Helllooooo"})

        _onClickButton() {
            const self = this;
            rpc.query({route: 'get_livechat_mail_channel_vals'})
            .then(function (response) {
                let def = session.rpc('/open_channel', {
                    channel_id : response.livechat_channel_id,
                });

                def.then(function (livechatData) {
                    debugger;
                });
            });
        }
    }

    const workInstance = new OwlWork();
    const div = document.querySelector('.oe_empty');
    workInstance.mount(document.body);
});