<template>
  <div class="login-container">
    <el-dialog title="没有私钥信息，请输入私钥信息！" :visible.sync="dialogFormVisible">
      <el-form :model="FormPrikey">
        <el-form-item label="IdentityPri">
          <el-input v-model="FormPrikey.IdentityPri" autocomplete="off" required="required"></el-input>
        </el-form-item>
        <el-form-item label="SignedPri">
          <el-input v-model="FormPrikey.SignedPri" autocomplete="off" required="required"></el-input>
        </el-form-item>
        <el-form-item label="OneTimePri">
          <el-input v-model="FormPrikey.OneTimePri" autocomplete="off" required="required"></el-input>
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
          required="required" />
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="FormLogin.password" auto-complete="off" placeholder="密码"
          required="required" />
      </el-form-item>
      <el-alert title="登录失败！" type="error" v-show="erroralert"></el-alert>
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
          required="required" />
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="FormReg.password" auto-complete="off" placeholder="密码"
          required="required" />
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
  export default {
    data() {
      return {
        dialogFormVisible:false,
        server_csrf:"",
        client_csrf:"",
        isreg: 0,
        erroralert: 0,
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
          Port: 8000,
          IdentityPri: "",
          SignedPri: "",
          OneTimePri: ""
        },
        FormPrikey:{
          IdentityPri:"",
          SignedPri:"",
          OneTimePri:"",
        },
        keys:{},
      }
    },
    // 查询是否有已登录的账号
    created: function () {
      // axios.get("http://127.0.0.1:8888/apis/gettoken/")
      // axios.get("http://127.0.0.1:8000/apis/gettoken/")
      // this.$cookies.set("logining_userid", "test")
      // var logging_cookie = this.$cookies.get("logining_userid");
      // if (logging_cookie) {
      //   this.$router.push("/index")
      // }
    },
    methods: {
      login() {
        this.isreg = 0;
        this.FormReg.username = ''
        this.FormReg.password = ''
        this.FormLogin.userid = ''
        this.FormLogin.password = ''
      },
      regis() {
        this.isreg = 1;
        this.FormLogin.userid = ''
        this.FormLogin.password = ''
        this.FormReg.username = ''
        this.FormReg.password = ''
      },
      Login() {
        axios.get("http://127.0.0.1:8000/apis/get_user/"+this.FormLogin.userid).then((response)=>{
          console.log(response.data["code"])
          if(response.data["code"]==1){
            if(response.data["data"]["IdentityPri"]!=""){
              axios.post("http://127.0.0.1:8888/apis/user/" + this.FormLogin.userid, {
                "password": sha256(this.FormLogin.password),
              }).then((response) => {
                if(response.data["code"]==1){
                  // 获取到用户登录的username
                  username_t=response.data["data"]["username"]
                  // 密码验证正确后将该私钥
                  axios.post("http://127.0.0.1:8000/apis/store_user",{
                  userid=this.FormLogin.userid, username=username_t,
                  IdentityPub=response_data["IdentityPub"], SignedPub=response_data["SignedPub"],
                  OneTimePub=response_data["OneTimePub"], ElephantPub="",
                  IdentityPri=response_data["IdentityPri"], SignedPri=response_data["SignedPri"],
                  OneTimePri=response_data["OneTimePri"], ElephantPri=""
                  }).then((response)=>{
                  
                  })
                }else{
                }
              })
            }else{
                  this.dialogFormVisible=true
            }
          }else{
                  this.dialogFormVisible=true
          }
        })
      },
      updated_pri() {
        this.dialogFormVisible = false
        // 先检查私钥的格式是否有误
        axios.post("http://127.0.0.1:8000/apis/check_pri/",{
          "IdentityPri":this.FormPrikey.IdentityPri,
          "SignedPri":this.FormPrikey.SignedPri,
          "OneTimePri":this.FormPrikey.OneTimePri
        }).then((response)=>{
          // console.log(response.data["data"])
          if(response.data["code"]==1){
            // 返回的数据包括私钥字符串和公钥字符串
            this.keys=response.data["data"]
          }else{
            this.$notify.error({
            title: '私钥格式有误！',
            message: '请重新登录',
            // type: 'success'
            });
          }
        })
      },
      Register() {
        axios.post("http://127.0.0.1:8000/apis/create_new_keyspair/", {
          headers: {
            "Content-Type": "application/json",
          }
        }).then((response) => {
          var pubs = response.data["data"]
          console.log(response.data["data"])
          this.FormReg.IdentityPub = pubs["IdentityPub"]
          this.FormReg.SignedPub = pubs["SignedPub"]
          this.FormReg.OneTimePub = pubs["OneTimePub"]
          this.FormReg.IdentityPri = pubs["IdentityPri"]
          this.FormReg.SignedPri = pubs["SignedPri"]
          this.FormReg.OneTimePri = pubs["OneTimePri"]
          axios.post("http://127.0.0.1:8888/apis/user/", {
            "username": this.FormReg.username,
            "password": sha256(this.FormReg.password),
            "IdentityPub": this.FormReg.IdentityPub,
            "SignedPub": this.FormReg.SignedPub,
            "OneTimePub": this.FormReg.OneTimePub,
          }).then((response) => {
            console.log(response.data)
            if (response.data["code"]) {
              this.$notify({
              title: '注册成功的ID:',
              message: h('i', {
                  style: 'color: teal'
                }, response.data["data"]),
              type: 'success',
              duration: 0
              });
              axios.post("http://127.0.0.1:8000/apis/store_user/", {
                "userid": response.data["data"],
                "username": this.FormReg.username,
                "IdentityPub": this.FormReg.IdentityPub,
                "SignedPub": this.FormReg.SignedPub,
                "OneTimePub": this.FormReg.OneTimePub,
                "ElephantPub": "",
                "IdentityPri": this.FormReg.IdentityPri,
                "SignedPri": this.FormReg.SignedPri,
                "OneTimePri": this.FormReg.OneTimePri,
                "ElephantPri": "",
              })
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
