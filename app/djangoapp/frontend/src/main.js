// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';


import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
Vue.use(ElementUI);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App
  },
  template: '<App/>'
});

Vue.prototype.message_list_flash = function message_list_flash() {
  axios.get("http://localhost:8000/apis/filter_messages/" + this.current_obj_id, {
    headers: {
      // "logining_userid":this.logining_userid
    }
  }).then((response) => {
    if (response.data["code"] === 1) {
      // console.log(response.data)
      this.message_list = response.data["data"]
    } else {
      this.$notify.error({
        title: '获取历史记录失败。',
        message: '刷新一下。',
        // type: 'success'
      });
    }
  })
}

Vue.prototype.friends_list_flash = function friends_list_flash() {
  axios.get("http://localhost:8000/apis/friends_list/", {
    headers: {
      // "logining_userid":this.logining_userid
    }
  }).then((response) => {
    if (response.data["code"] === 1) {
      // console.log(response.data)
      this.friends_list = response.data["data"]
    } else {
      this.$notify.error({
        title: '获取好友列表失败，或者好友列表为空。',
        message: '重启一下应用看看？',
        // type: 'success'
      });
    }
  })
}
