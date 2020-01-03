<template>
  <div class="login-container">
    <el-dialog title="没有私钥信息，请输入私钥信息！" :visible.sync="dialogFormVisible">
      <el-form :model="FormPrikey">
        <el-form-item label="IdentityPri">
          <el-input v-model="FormPrikey.IdentityPri" autocomplete="off" required="required"/>
        </el-form-item>
        <el-form-item label="SignedPri">
          <el-input v-model="FormPrikey.SignedPri" autocomplete="off" required="required"/>
        </el-form-item>
        <el-form-item label="OneTimePri">
          <el-input v-model="FormPrikey.OneTimePri" autocomplete="off" required="required"/>
        </el-form-item>
        <el-form-item label="EphemeralPri">
          <el-input v-model="FormPrikey.EphemeralPri" autocomplete="off" required="required"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="updated_pri()">确 定</el-button>
      </div>
    </el-dialog>
    <el-form :model="FormLogin" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-if="!isreg">
      <el-button type="primary" class="login-button-left" @click.native="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click.native="regis">注册</el-button>
      <el-form-item prop="userid">
        <el-input type="text" v-model="FormLogin.userid" auto-complete="off" placeholder="请使用注册成功的ID登录"
                  required="required"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="FormLogin.password" auto-complete="off" placeholder="密码"
                  required="required"/>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click="Login">登录</el-button>
      </el-form-item>
    </el-form>
    <el-form :model="FormReg" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-else>
      <el-button type="primary" class="login-button-left" @click="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click="regis">注册</el-button>
      <el-form-item prop="username">
        <el-input type="text" v-model="FormReg.username" auto-complete="off" placeholder="用户名"
                  required="required"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="FormReg.password" auto-complete="off" placeholder="密码"
                  required="required"/>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click="Register">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import axios from "axios"
  import sha256 from "js-sha256"

  
  function getCookie(cookieName) {
    var strCookie = document.cookie;
    var arrCookie = strCookie.split("; ");
    for(var i = 0; i < arrCookie.length; i++){
      var arr = arrCookie[i].split("=");
      if(cookieName == arr[0]){
          return arr[1];
      }
    }
    return "";
  }
  export default {
    data() {
      return {
        dialogFormVisible: false,
        // server_csrf: "",
        // client_csrf: "",
        isreg: 0,
        FormLogin: {
          userid: '',
          password: '',
        },
        FormReg: {
          username: '',
          password: '',
          IdentityPub: '',
          SignedPub: '',
          OneTimePub: '',
          EphemeralPub:'',
          IdentityPri: "",
          SignedPri: "",
          OneTimePri: "",
          EphemeralPri:"",
        },
        FormPrikey: {
          IdentityPri: "",
          SignedPri: "",
          OneTimePri: "",
          EphemeralPri:""
        },
        keys: {},
        csrftoken:"",
      }
    },
    // 查询是否有已登录的账号
    created: function () {
      // this.$cookies.set("logining_userid", "82119217")
      var logging_cookie = this.$cookies.get("logining_userid");
      if (logging_cookie) {
        this.$router.push("/")
      }
      // axios.get("http://localhost:8000/apis/gettoken/")
      // this.csrftoken=getCookie("csrftoken")
      // console.log(this.csrftoken)
    },
    methods: {
      login() {
        this.isreg = 0;
        this.FormReg.username = '';
        this.FormReg.password = '';
        this.FormLogin.userid = '';
        this.FormLogin.password = ''
      },
      regis() {
        this.isreg = 1;
        this.FormLogin.userid = '';
        this.FormLogin.password = '';
        this.FormReg.username = '';
        this.FormReg.password = ''
      },
      Login() {
        axios.get("http://localhost:8000/apis/get_user/" + this.FormLogin.userid).then((response) => {
          // console.log(response.data["code"]);
          if (response.data["code"] === 1) {
            var temp_data=response.data["data"][0]
            if (typeof temp_data["IdentityPri"] !== "undefined") {
              axios.post("http://127.0.0.1:8888/apis/user/" + this.FormLogin.userid, {
                "password": sha256(this.FormLogin.password),
                headers:{
                  // "X-CSRFToken":this.csrftoken
                }
              }).then((response) => {
                // console.log(response.data)
                if (response.data["code"] === 1) {
                  this.$cookies.set("logining_userid",response.data["data"]["userid"]);
                  this.$router.push("/")
                } else {
                  this.$notify.error({
                    title: '登录失败！',
                    message: '请重新登录',
                    // type: 'success'
                  });
                }
              })
            } else {
              this.dialogFormVisible = true
            }
          } else {
            this.dialogFormVisible = true
          }
        })
      },
      updated_pri() {
        this.dialogFormVisible = false
        // 先检查私钥的格式是否有误
        axios.post("http://localhost:8000/apis/check_pri/", {
          "IdentityPri": this.FormPrikey.IdentityPri,
          "SignedPri": this.FormPrikey.SignedPri,
          "OneTimePri": this.FormPrikey.OneTimePri,
          "EphemeralPri":this.FormPrikey.EphemeralPri,
          headers:{
            // "X-CSRFToken":this.csrftoken
          }
        }).then((response) => {
          // console.log(response.data["data"])
          if (response.data["code"] === 1) {
            // 返回的数据包括私钥字符串和公钥字符串
            this.keys = response.data["data"];
            axios.get("http://127.0.0.1:8888/apis/user/" + this.FormLogin.userid).then((response) => {
              if (response.data["code"] === 1) {
                const username_t = response.data["data"]["username"];
                axios.post("http://localhost:8000/apis/store_user", {
                  userid: this.FormLogin.userid, username: username_t,
                  IdentityPub: this.keys["IdentityPub"], SignedPub: this.keys["SignedPub"],
                  OneTimePub: this.keys["OneTimePub"], EphemeralPub: this.keys["EphemeralPub"],
                  IdentityPri: this.keys["IdentityPri"], SignedPri: this.keys["SignedPri"],
                  OneTimePri: this.keys["OneTimePri"], EphemeralPri: this.keys["EphemeralPri"],
                  headers:{
                    // "X-CSRFToken":this.csrftoken
                  }
                }).then((response) => {
                  if (response.data["code"] === 1) {
                    this.$notify({
                      title: '已将当前用户添加到数据库',
                      message: '请重新登录',
                      type: 'success'
                    });
                  } else {
                    this.$notify.error({
                      title: '保存用户密钥出错！',
                      message: '请重新登录',
                      // type: 'success'
                    });
                  }
                })
              } else {
                this.$notify.error({
                  title: '服务器获取用户信息失败！',
                  message: '请重新登录',
                  // type: 'success'
                });
              }
            });
          } else {
            this.$notify.error({
              title: '私钥格式有误！',
              message: '请重新登录',
              // type: 'success'
            });
          }
        })
      },
      Register() {
        axios.post("http://localhost:8000/apis/create_new_keyspair/", {
          headers: {
            // "X-CSRFToken":this.csrftoken,
          }
        }).then((response) => {
          var pubs = response.data["data"];
          // console.log(response.data["data"]);
          this.FormReg.IdentityPub = pubs["IdentityPub"];
          this.FormReg.SignedPub = pubs["SignedPub"];
          this.FormReg.OneTimePub = pubs["OneTimePub"];
          this.FormReg.EphemeralPub=pubs["EphemeralPub"];
          this.FormReg.IdentityPri = pubs["IdentityPri"];
          this.FormReg.SignedPri = pubs["SignedPri"];
          this.FormReg.OneTimePri = pubs["OneTimePri"];
          this.FormReg.EphemeralPri = pubs["EphemeralPri"];
          axios.post("http://127.0.0.1:8888/apis/user/", {
            "username": this.FormReg.username,
            "password": sha256(this.FormReg.password),
            "IdentityPub": this.FormReg.IdentityPub,
            "SignedPub": this.FormReg.SignedPub,
            "OneTimePub": this.FormReg.OneTimePub,
            "EphemeralPub": this.FormReg.EphemeralPub,
            headers:{
              // "X-CSRFToken":this.csrftoken
            }
          }).then((response) => {
            // console.log(response.data);
            if (response.data["code"]) {
              const h = this.$createElement;
              this.$notify({
                title: '注册成功的ID:',
                message: h('i', {
                  style: 'color: teal'
                }, response.data["data"]),
                type: 'success',
                duration: 0
              });
              axios.post("http://localhost:8000/apis/store_user/", {
                "userid": response.data["data"],
                "username": this.FormReg.username,
                "IdentityPub": this.FormReg.IdentityPub,
                "SignedPub": this.FormReg.SignedPub,
                "OneTimePub": this.FormReg.OneTimePub,
                "EphemeralPub": this.FormReg.EphemeralPub,
                "IdentityPri": this.FormReg.IdentityPri,
                "SignedPri": this.FormReg.SignedPri,
                "OneTimePri": this.FormReg.OneTimePri,
                "EphemeralPri": this.FormReg.EphemeralPri,
                headers:{
                  // "X-CSRFToken":this.csrftoken
                }
              });
              this.isreg = 0;
              this.FormLogin.userid = ''
              this.FormLogin.password = ''
              this.FormReg.username = ''
              this.FormReg.password = ''
            } else {
              this.$notify.error({
                title: '注册失败！',
                message: '请重新注册',
                // type: 'success'
              });
            }
          })
        })
      }
    }
  };

</script>

<style scoped>
  .login-container {
    width: 100%;
    height: 100%;
  }

  .login-page {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    margin: 180px auto 0px auto;
    width: 350px;
    padding: 35px 35px 15px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }


  .login-button-left {
    width: 165px;
    margin: 0px 5px 10px 0px;
  }

  .login-button-right {
    width: 165px;
    margin: 0px 0px 10px 5px;
  }

</style>
