webpackJsonp([1],{"09yM":function(e,t){},Fqkb:function(e,t){},NHnr:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=r("7+uW"),o={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},staticRenderFns:[]};var i=r("VU/8")({name:"App"},o,!1,function(e){r("gsu9")},null,null).exports,a=r("/ocq"),n={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[r("div",{staticClass:"left"},e._l(e.friend_list,function(t,s){return r("ul",{key:s},[r("a",{attrs:{href:"#"}},[e._v(e._s(t.id+t.name))])])}),0),e._v(" "),r("div",{staticClass:"r-up"},[r("h3",[e._v("聊天详情")]),e._v(" "),e._l(e.message_list,function(t,s){return r("ul",{key:s,attrs:{id:"content"}},[r("li",[e._v(e._s(t))])])})],2),e._v(" "),r("div",{staticClass:"r-dn"},[r("textarea",{directives:[{name:"model",rawName:"v-model",value:e.inputmsg,expression:"inputmsg"}],attrs:{name:"",id:"",cols:"66",rows:"20",placeholder:"在这里输入"},domProps:{value:e.inputmsg},on:{input:function(t){t.target.composing||(e.inputmsg=t.target.value)}}}),e._v(" "),r("div",{staticClass:"sub_button"},[r("button",{on:{click:e.submit}},[e._v("发送")])])])])},staticRenderFns:[]};var l=r("VU/8")({name:"friend",data:function(){return{message_list:[],inputmsg:"",friend_list:[{id:1,name:"张三"},{id:2,name:"李四"},{id:3,name:"王五"}]}},methods:{submit:function(){this.list.push(this.inputmsg),this.inputmsg=""}},watch:{}},n,!1,function(e){r("Fqkb")},"data-v-40cfd95e",null).exports,u=r("Muz9"),d=r.n(u),m=r("e9Q/"),p=r.n(m),c={data:function(){return{isreg:0,erroralert:0,ruleForm:{userid:"",password:""},ruleFromReg:{username:"",password:"",IdentityPub:"",SignedPub:"",OneTimePub:"",Port:8e3}}},created:function(){this.$cookies.get("logining_userid")&&this.$router.push("/index")},methods:{login:function(){this.isreg=0,this.ruleFromReg.username="",this.ruleFromReg.password="",this.ruleForm.userid="",this.ruleForm.password=""},regis:function(){this.isreg=1,this.ruleForm.userid="",this.ruleForm.password="",this.ruleFromReg.username="",this.ruleFromReg.password=""},Login:function(){var e=this;d.a.post("http://127.0.0.1:8888/apis/user/"+this.ruleForm.userid,{password:p()(this.ruleForm.password)}).then(function(t){console.log(t.data),t.data.code?(e.$cookies.set("logining_userid",e.ruleForm.userid),console.log(e.$cookies),e.erroralert=0,e.$router.push("/index")):e.erroralert=1})},Register:function(){var e=this;d.a.post("http://127.0.0.1:8000/apis/create_new_keyspair/",{headers:{"Content-Type":"application/json"}}).then(function(t){var r=t.data.data;console.log(t.data.data),e.ruleFromReg.IdentityPub=r.IdentityPub,e.ruleFromReg.SignedPub=r.SignedPub,e.ruleFromReg.OneTimePub=r.OneTimePub,d.a.post("http://127.0.0.1:8888/apis/user/",{username:e.ruleFromReg.username,password:p()(e.ruleFromReg.password),IdentityPub:e.ruleFromReg.IdentityPub,SignedPub:e.ruleFromReg.SignedPub,OneTimePub:e.ruleFromReg.OneTimePub,last_port:e.ruleFromReg.Port}).then(function(t){if(console.log(t.data),t.data.code){var r=e.$createElement;e.$notify({title:"注册成功的ID",message:r("i",{style:"color: teal"},t.data.data),duration:0}),e.isreg=0,e.ruleForm.userid="",e.ruleForm.password="",e.ruleFromReg.username="",e.ruleFromReg.password=""}else{var s=e.$createElement;e.$notify({title:"注册失败！",message:s("i",{style:"color: teal"},t.data["请重新注册"])})}})})}}},g={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"login-container"},[e.isreg?r("el-form",{ref:"ruleForm2",staticClass:"demo-ruleForm login-page",attrs:{model:e.ruleFromReg,"status-icon":"","label-position":"left","label-width":"0px"}},[r("el-button",{staticClass:"login-button-left",attrs:{type:"primary"},on:{click:e.login}},[e._v("登录")]),e._v(" "),r("el-button",{staticClass:"login-button-right",attrs:{type:"primary"},on:{click:e.regis}},[e._v("注册")]),e._v(" "),r("el-form-item",{attrs:{prop:"username"}},[r("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"用户名",required:"required"},model:{value:e.ruleFromReg.username,callback:function(t){e.$set(e.ruleFromReg,"username",t)},expression:"ruleFromReg.username"}})],1),e._v(" "),r("el-form-item",{attrs:{prop:"password"}},[r("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码",required:"required"},model:{value:e.ruleFromReg.password,callback:function(t){e.$set(e.ruleFromReg,"password",t)},expression:"ruleFromReg.password"}})],1),e._v(" "),r("el-form-item",{staticStyle:{width:"100%"}},[r("el-button",{staticStyle:{width:"100%"},attrs:{type:"primary"},on:{click:e.Register}},[e._v("注册")])],1)],1):r("el-form",{ref:"ruleForm2",staticClass:"demo-ruleForm login-page",attrs:{model:e.ruleForm,"status-icon":"","label-position":"left","label-width":"0px"}},[r("el-button",{staticClass:"login-button-left",attrs:{type:"primary"},nativeOn:{click:function(t){return e.login(t)}}},[e._v("登录")]),e._v(" "),r("el-button",{staticClass:"login-button-right",attrs:{type:"primary"},nativeOn:{click:function(t){return e.regis(t)}}},[e._v("注册")]),e._v(" "),r("el-form-item",{attrs:{prop:"userid"}},[r("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"请使用注册成功的ID登录",required:"required"},model:{value:e.ruleForm.userid,callback:function(t){e.$set(e.ruleForm,"userid",t)},expression:"ruleForm.userid"}})],1),e._v(" "),r("el-form-item",{attrs:{prop:"password"}},[r("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码",required:"required"},model:{value:e.ruleForm.password,callback:function(t){e.$set(e.ruleForm,"password",t)},expression:"ruleForm.password"}})],1),e._v(" "),r("el-alert",{directives:[{name:"show",rawName:"v-show",value:e.erroralert,expression:"erroralert"}],attrs:{title:"登录失败！",type:"error"}}),e._v(" "),r("el-form-item",{staticStyle:{width:"100%"}},[r("el-button",{staticStyle:{width:"100%"},attrs:{type:"primary"},on:{click:e.Login}},[e._v("登录")])],1)],1)],1)},staticRenderFns:[]};var f=r("VU/8")(c,g,!1,function(e){r("YR2n")},"data-v-72fe633f",null).exports;s.default.use(a.a);var v=new a.a({mode:"history",routes:[{path:"/",name:"Login",component:f},{path:"/index",name:"Index",component:l}]}),h=r("TcQY"),F=r.n(h),_=(r("09yM"),r("6Lj2")),b=r.n(_);s.default.use(b.a),s.default.use(F.a),new s.default({el:"#app",router:v,components:{App:i},template:"<App/>"})},YR2n:function(e,t){},gsu9:function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.72c81af1ab7ee6bb7185.js.map