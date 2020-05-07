odoo.define('owl_work.btn_component', function(require){
    "use strict";

    var session = require('web.session');
    var WebsiteLivechat = require('im_livechat.model.WebsiteLivechat');
    var WebsiteLivechatMessage = require('im_livechat.model.WebsiteLivechatMessage');
    var WebsiteLivechatWindow = require('im_livechat.WebsiteLivechatWindow');
         
    require('web.dom_ready');

    const { Component, useState, hooks } = owl;
    const { xml } = owl.tags;

    class OwlWork extends Component{
        static template = xml`
            <button t-on-click="_onClickButton">
                Click Me
            </button>`;
        state = useState({ value: "Helllooooo"})

        _livechat = null;

        _openChatWindow() {
            var self = this;
            var options = {
                displayStars: false,
                headerBackgroundColor: 'black',
                placeholder: 'please enter msg',
                titleColor: 'white',
            };
            this._chatWindow = new WebsiteLivechatWindow(this, this._livechat, options);
            return this._chatWindow.appendTo($('body')).then(function () {
                var cssProps = {bottom: 0};
                self._chatWindow.$el.css(cssProps);
                $(self.el).hide();
            });
        }
        _onClickButton() {
            // var button = new im_livechat.LivechatButton(rootWidget);
            // button._openChat();
            const self = this;
            let def;
            def = session.rpc('/im_livechat/get_session', {
                channel_id : 1,
                anonymous_name : 'Visitor',
                previous_operator_id: '3',
            }, {shadow: true});
            def.then(function (livechatData) {
                if (!livechatData || !livechatData.operator_pid) {
                    return;
                } else {
                    self._livechat = new WebsiteLivechat({
                        parent: self,
                        data: livechatData
                    });
                    return self._openChatWindow().then(function () {});
                }
            });
        }
    }

    const workInstance = new OwlWork();
    workInstance.mount(document.body);
});