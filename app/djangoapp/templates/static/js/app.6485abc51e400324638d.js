webpackJsonp([1],{"09yM":function(e,t){},FVDA:function(e,t){},JLih:function(e,t){},"N/yo":function(e,t){},NHnr:function(e,t,i){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=i("7+uW"),s={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},staticRenderFns:[]};var a=i("VU/8")({name:"App"},s,!1,function(e){i("JLih")},null,null).exports,n=i("/ocq"),o=i("Muz9"),l=i.n(o);l.a.defaults.withCredentials=!0;var d={name:"friend",data:function(){return{count:20,loading:!1,logining_userid:0,message_num:10,message_list:[],search_input:"",msg_input:"",dialogFormVisible:!1,friends_list:[],search_result:[],current_obj_id:0,is_friend:0,csrftoken:""}},created:function(){var e=this;this.logining_userid=this.$cookies.get("logining_userid"),this.logining_userid?l.a.get("http://localhost:8000/apis/friends_list/",{headers:{logining_userid:this.logining_userid}}).then(function(t){1===t.data.code?e.friends_list=t.data.data:e.$notify.error({title:"获取好友列表失败，或者好友列表为空。",message:"重启一下应用看看？"})}):this.$router.push("/login")},computed:{},methods:{send_message:function(e){function t(){return e.apply(this,arguments)}return t.toString=function(){return e.toString()},t}(function(){var e=this;l.a.get("http://localhost:8000/apis/friends_list/"+this.current_obj_id).then(function(t){1===t.data.code?l.a.post("http://localhost:8000/apis/encrypt_message/",{text:e.inputmsg,toUserid:e.current_obj_id}).then(function(e){console.log(e.data.data)}):l.a.get("http://127.0.0.1:8888/apis/user/"+e.current_obj_id).then(function(e){if(1===e.data.code){var t=e.data.data;l.a.post("http://localhost:8000/apis/store_friend/",{userid:t.userid,username:t.username,remark:"",status:1,IdentityPub:t.IdentityPub,SignedPub:t.SignedPub,OneTimePub:t.OneTimePub,ElephantPub:t.ElephantPub}),send_message()}})}),this.inputmsg=""}),excheng_obj:function(e){l.a.get("http://localhost:8000/apis/filter_messages/"+e).then(function(e){}),this.current_obj_id=e},search_friend:function(){var e=this;this.search_result=[],l.a.get("http://127.0.0.1:8888/apis/user/"+this.search_input).then(function(t){if(1===t.data.code){e.search_result.push(t.data.data),e.search_result[0].userid===parseInt(e.logining_userid)?e.is_friend=2:e.is_friend=0;for(var i=0;i<e.friends_list.length;i++)e.friends_list[i].userid===e.search_result[0].userid?e.is_friend=1:e.is_friend=0}else e.$notify.error({title:"搜索失败！",message:"请稍后重试。"})}),this.dialogFormVisible=!0},friends_list_flash:function(){var e=this;l.a.get("http://localhost:8000/apis/friends_list/",{headers:{logining_userid:this.logining_userid}}).then(function(t){1===t.data.code?e.friends_list=t.data.data:e.$notify.error({title:"获取好友列表失败，或者好友列表为空。",message:"重启一下应用看看？"})})},add_friend:function(e){var t=this;l.a.post("http://localhost:8000/apis/store_friend/",{userid:e.userid,username:e.username,remark:"",status:1,IdentityPub:e.IdentityPub,SignedPub:e.SignedPub,OneTimePub:e.OneTimePub,ElephantPub:e.ElephantPub,headers:{}}).then(function(e){1===e.data.code?(t.dialogFormVisible=!1,t.$notify({title:"添加成功！",message:"已将好友添加到列表。",type:"success"}),friends_list_flash()):(t.dialogFormVisible=!1,t.$notify.error({title:"添加失败！",message:"请稍后重试。"}))})}},watch:{current_obj_id:function(e,t){}}},u={render:function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{attrs:{id:"app"}},[i("el-dialog",{attrs:{title:"搜索结果",visible:e.dialogFormVisible,"modal-append-to-body":!1},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[e.search_result.length?i("el-row",[i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_title"},[e._v("ID")])]),e._v(" "),i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_title"},[e._v("Username")])]),e._v(" "),i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_title"})])],1):i("el-row",[i("el-col",{attrs:{span:24}},[i("div",{staticClass:"search_table_title"},[e._v("没有该用户相关信息")])])],1),e._v(" "),i("el-row",[i("el-col",{attrs:{span:24}},[i("el-divider")],1)],1),e._v(" "),e._l(e.search_result,function(t,r){return i("el-row",{key:r},[i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_itme"},[e._v(e._s(t.userid))])]),e._v(" "),i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_itme"},[e._v(e._s(t.username))])]),e._v(" "),1===e.is_friend?i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_itme"},[i("el-button",{attrs:{type:"primary",disabled:""}},[e._v("已经是好友了")])],1)]):2===e.is_friend?i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_itme"},[i("el-button",{attrs:{type:"primary",disabled:""}},[e._v("不能添加自己哦")])],1)]):i("el-col",{attrs:{span:8}},[i("div",{staticClass:"search_table_itme"},[i("el-button",{attrs:{type:"primary"},on:{click:function(i){return e.add_friend(t)}}},[e._v("添加")])],1)]),e._v(" "),i("el-col",{attrs:{span:24}},[i("el-divider")],1)],1)})],2),e._v(" "),i("div",{attrs:{id:"left"}},[i("div",{staticClass:".col-md-3",attrs:{id:"search_line"}},[i("el-input",{attrs:{placeholder:"请输入内容",required:"required",clearable:""},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.search_friend(t)}},model:{value:e.search_input,callback:function(t){e.search_input=t},expression:"search_input"}})],1),e._v(" "),i("div",{attrs:{id:"friends_list"}},[i("el-row",{staticClass:"tac"},[i("el-col",{attrs:{span:24}},[i("el-menu",{staticClass:"el-menu",attrs:{"default-active":"1","default-open":"1","background-color":"#545c64","text-color":"#fff","active-text-color":"#ffd04b"}},e._l(e.friends_list,function(t,r){return i("el-menu-item-group",{key:r},[i("el-menu-item",{staticClass:"friend-item",on:{click:function(i){return e.excheng_obj(t.userid)}}},[e._v(e._s(t.username))])],1)}),1)],1)],1)],1)]),e._v(" "),i("div",{attrs:{id:"right"}},[e.current_obj_id?i("div",{attrs:{id:"show_window"}},[i("div",{attrs:{id:"show_message"}},e._l(e.message_list,function(t,r){return i("el-row",{key:r},[t.toUserid==e.logging_in?i("el-col",{attrs:{span:24}},[i("div",{staticClass:"show_message_date"},[e._v(e._s(t.date))])]):e._e(),e._v(" "),t.fromUserid==e.logging_in?i("el-col",{attrs:{span:24}},[i("div",{staticClass:"show_message_date_self"},[e._v(e._s(t.date))])]):e._e(),e._v(" "),t.toUserid==e.logging_in?i("el-col",{attrs:{span:24}},[i("div",{staticClass:"show_message_text"},[e._v(e._s(t.plaintext))])]):e._e(),e._v(" "),t.fromUserid==e.logging_in?i("el-col",{attrs:{span:24}},[i("div",{staticClass:"show_message_text_self"},[e._v(e._s(t.plaintext))])]):e._e()],1)}),1),e._v(" "),i("div",{attrs:{id:"input_box"}},[i("textarea",{directives:[{name:"model",rawName:"v-model",value:e.msg_input,expression:"msg_input"}],attrs:{type:"textarea",id:"textarea_box",name:"",cols:"50",placeholder:"在这里输入",autofocus:""},domProps:{value:e.msg_input},on:{input:function(t){t.target.composing||(e.msg_input=t.target.value)}}}),e._v(" "),i("div",{attrs:{id:"submit_button"}},[i("el-button",{attrs:{type:"primary",id:"button"},on:{click:function(t){return e.send_message()}}},[e._v("发送")])],1)])]):e._e()])],1)},staticRenderFns:[]};var c=i("VU/8")(d,u,!1,function(e){i("FVDA")},"data-v-34b04877",null).exports,m=i("e9Q/"),p=i.n(m);var g={data:function(){return{dialogFormVisible:!1,isreg:0,FormLogin:{userid:"",password:""},FormReg:{username:"",password:"",IdentityPub:"",SignedPub:"",OneTimePub:"",ElephantPub:"",IdentityPri:"",SignedPri:"",OneTimePri:"",ElephantPri:""},FormPrikey:{IdentityPri:"",SignedPri:"",OneTimePri:"",ElephantPri:""},keys:{},csrftoken:""}},created:function(){this.$cookies.get("logining_userid")&&this.$router.push("/")},methods:{login:function(){this.isreg=0,this.FormReg.username="",this.FormReg.password="",this.FormLogin.userid="",this.FormLogin.password=""},regis:function(){this.isreg=1,this.FormLogin.userid="",this.FormLogin.password="",this.FormReg.username="",this.FormReg.password=""},Login:function(){var e=this;l.a.get("http://localhost:8000/apis/get_user/"+this.FormLogin.userid).then(function(t){if(1===t.data.code){var i=t.data.data[0];void 0!==i.IdentityPri?l.a.post("http://127.0.0.1:8888/apis/user/"+e.FormLogin.userid,{password:p()(e.FormLogin.password),headers:{}}).then(function(t){1===t.data.code?(e.$cookies.set("logining_userid",i.userid),e.$router.push("/")):e.$notify.error({title:"登录失败！",message:"请重新登录"})}):e.dialogFormVisible=!0}else e.dialogFormVisible=!0})},updated_pri:function(){var e=this;this.dialogFormVisible=!1,l.a.post("http://localhost:8000/apis/check_pri/",{IdentityPri:this.FormPrikey.IdentityPri,SignedPri:this.FormPrikey.SignedPri,OneTimePri:this.FormPrikey.OneTimePri,ElephantPri:this.FormPrikey.ElephantPri,headers:{}}).then(function(t){1===t.data.code?(e.keys=t.data.data,l.a.get("http://127.0.0.1:8888/apis/user/"+e.FormLogin.userid).then(function(t){if(1===t.data.code){var i=t.data.data.username;l.a.post("http://localhost:8000/apis/store_user",{userid:e.FormLogin.userid,username:i,IdentityPub:e.keys.IdentityPub,SignedPub:e.keys.SignedPub,OneTimePub:e.keys.OneTimePub,ElephantPub:e.keys.ElephantPub,IdentityPri:e.keys.IdentityPri,SignedPri:e.keys.SignedPri,OneTimePri:e.keys.OneTimePri,ElephantPri:e.keys.ElephantPri,headers:{}}).then(function(t){1===t.data.code?e.$notify({title:"已将当前用户添加到数据库",message:"请重新登录",type:"success"}):e.$notify.error({title:"保存用户密钥出错！",message:"请重新登录"})})}else e.$notify.error({title:"服务器获取用户信息失败！",message:"请重新登录"})})):e.$notify.error({title:"私钥格式有误！",message:"请重新登录"})})},Register:function(){var e=this;l.a.post("http://localhost:8000/apis/create_new_keyspair/",{headers:{}}).then(function(t){var i=t.data.data;e.FormReg.IdentityPub=i.IdentityPub,e.FormReg.SignedPub=i.SignedPub,e.FormReg.OneTimePub=i.OneTimePub,e.FormReg.ElephantPub=i.ElephantPub,e.FormReg.IdentityPri=i.IdentityPri,e.FormReg.SignedPri=i.SignedPri,e.FormReg.OneTimePri=i.OneTimePri,e.FormReg.ElephantPri=i.ElephantPri,l.a.post("http://127.0.0.1:8888/apis/user/",{username:e.FormReg.username,password:p()(e.FormReg.password),IdentityPub:e.FormReg.IdentityPub,SignedPub:e.FormReg.SignedPub,OneTimePub:e.FormReg.OneTimePub,ElephantPub:e.FormReg.ElephantPub,headers:{}}).then(function(t){if(t.data.code){var i=e.$createElement;e.$notify({title:"注册成功的ID:",message:i("i",{style:"color: teal"},t.data.data),type:"success",duration:0}),l.a.post("http://localhost:8000/apis/store_user/",{userid:t.data.data,username:e.FormReg.username,IdentityPub:e.FormReg.IdentityPub,SignedPub:e.FormReg.SignedPub,OneTimePub:e.FormReg.OneTimePub,ElephantPub:e.FormReg.ElephantPub,IdentityPri:e.FormReg.IdentityPri,SignedPri:e.FormReg.SignedPri,OneTimePri:e.FormReg.OneTimePri,ElephantPri:e.FormReg.ElephantPri,headers:{}}),e.isreg=0,e.FormLogin.userid="",e.FormLogin.password="",e.FormReg.username="",e.FormReg.password=""}else e.$notify.error({title:"注册失败！",message:"请重新注册"})})})}}},_={render:function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"login-container"},[i("el-dialog",{attrs:{title:"没有私钥信息，请输入私钥信息！",visible:e.dialogFormVisible},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[i("el-form",{attrs:{model:e.FormPrikey}},[i("el-form-item",{attrs:{label:"IdentityPri"}},[i("el-input",{attrs:{autocomplete:"off",required:"required"},model:{value:e.FormPrikey.IdentityPri,callback:function(t){e.$set(e.FormPrikey,"IdentityPri",t)},expression:"FormPrikey.IdentityPri"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"SignedPri"}},[i("el-input",{attrs:{autocomplete:"off",required:"required"},model:{value:e.FormPrikey.SignedPri,callback:function(t){e.$set(e.FormPrikey,"SignedPri",t)},expression:"FormPrikey.SignedPri"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"OneTimePri"}},[i("el-input",{attrs:{autocomplete:"off",required:"required"},model:{value:e.FormPrikey.OneTimePri,callback:function(t){e.$set(e.FormPrikey,"OneTimePri",t)},expression:"FormPrikey.OneTimePri"}})],1),e._v(" "),i("el-form-item",{attrs:{label:"ElephantPri"}},[i("el-input",{attrs:{autocomplete:"off",required:"required"},model:{value:e.FormPrikey.ElephantPri,callback:function(t){e.$set(e.FormPrikey,"ElephantPri",t)},expression:"FormPrikey.ElephantPri"}})],1)],1),e._v(" "),i("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("取 消")]),e._v(" "),i("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.updated_pri()}}},[e._v("确 定")])],1)],1),e._v(" "),e.isreg?i("el-form",{ref:"ruleForm2",staticClass:"demo-ruleForm login-page",attrs:{model:e.FormReg,"status-icon":"","label-position":"left","label-width":"0px"}},[i("el-button",{staticClass:"login-button-left",attrs:{type:"primary"},on:{click:e.login}},[e._v("登录")]),e._v(" "),i("el-button",{staticClass:"login-button-right",attrs:{type:"primary"},on:{click:e.regis}},[e._v("注册")]),e._v(" "),i("el-form-item",{attrs:{prop:"username"}},[i("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"用户名",required:"required"},model:{value:e.FormReg.username,callback:function(t){e.$set(e.FormReg,"username",t)},expression:"FormReg.username"}})],1),e._v(" "),i("el-form-item",{attrs:{prop:"password"}},[i("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码",required:"required"},model:{value:e.FormReg.password,callback:function(t){e.$set(e.FormReg,"password",t)},expression:"FormReg.password"}})],1),e._v(" "),i("el-form-item",{staticStyle:{width:"100%"}},[i("el-button",{staticStyle:{width:"100%"},attrs:{type:"primary"},on:{click:e.Register}},[e._v("注册")])],1)],1):i("el-form",{ref:"ruleForm2",staticClass:"demo-ruleForm login-page",attrs:{model:e.FormLogin,"status-icon":"","label-position":"left","label-width":"0px"}},[i("el-button",{staticClass:"login-button-left",attrs:{type:"primary"},nativeOn:{click:function(t){return e.login(t)}}},[e._v("登录")]),e._v(" "),i("el-button",{staticClass:"login-button-right",attrs:{type:"primary"},nativeOn:{click:function(t){return e.regis(t)}}},[e._v("注册")]),e._v(" "),i("el-form-item",{attrs:{prop:"userid"}},[i("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"请使用注册成功的ID登录",required:"required"},model:{value:e.FormLogin.userid,callback:function(t){e.$set(e.FormLogin,"userid",t)},expression:"FormLogin.userid"}})],1),e._v(" "),i("el-form-item",{attrs:{prop:"password"}},[i("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码",required:"required"},model:{value:e.FormLogin.password,callback:function(t){e.$set(e.FormLogin,"password",t)},expression:"FormLogin.password"}})],1),e._v(" "),i("el-form-item",{staticStyle:{width:"100%"}},[i("el-button",{staticStyle:{width:"100%"},attrs:{type:"primary"},on:{click:e.Login}},[e._v("登录")])],1)],1)],1)},staticRenderFns:[]};var h=i("VU/8")(g,_,!1,function(e){i("N/yo")},"data-v-6a54947a",null).exports;r.default.use(n.a);var f=new n.a({mode:"history",routes:[{path:"/",name:"Index",component:c},{path:"/login",name:"Login",component:h}]}),b=i("TcQY"),v=i.n(b),P=(i("09yM"),i("6Lj2")),y=i.n(P);r.default.use(y.a),r.default.use(v.a),new r.default({el:"#app",router:f,components:{App:a},template:"<App/>"})}},["NHnr"]);
//# sourceMappingURL=app.6485abc51e400324638d.js.map