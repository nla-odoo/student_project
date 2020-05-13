odoo.define('owl_work.btn_component', function(require){
    "use strict";

    var session = require('web.session');
    var rpc = require('web.rpc');
         
    require('web.dom_ready');

    const { Component, useState, hooks } = owl;
    const { xml } = owl.tags;

    class OwlChat extends Component {

        static template = xml`
            <div class="chatbox">
                <div class="fa fa-close"></div>
                <div class="chatlogs">
                    <div class="chat">
                        <div id="chat_div" style="display: block;"></div>
                    </div>
                </div>
                <div class="chat-form">
                    <input id="txt_chat_input" class="chat_txt" type="text" t-on-keyup="addChat"/>
                    <input class="btn btn-secondary" type="submit" value="Send" t-on-click="_sendChat"/>
                </div>
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
            this._reciveChatToOther(tci.value);
        }

        _sendChatToOther(chat) {
            return session
            .rpc('/mail/send_message', {uuid: this.props.uuid, message_content: chat})
            .then(function (messageId) {
                debugger;
            });
        }

        _reciveChatToOther(chat) {
            return session
            .rpc('/mail/recive_message', {uuid: this.props.uuid, message_content: chat})
            .then(function (messageId) {
                debugger;
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
                if (response) {
                    const cc = document.querySelector("#chat_container");
                    if (!cc) {
                        const OwlChatInstance = new OwlChat(self, response);
                        OwlChatInstance.mount(document.body);
                    }
                } else {
                    alert('No operators are available, Please try to contact later')
                }
            });
        }
        static Components = {OwlChat};
    }

    const workInstance = new OwlWork();
    workInstance.mount(document.body);
});