<template>
  <div class="login-container">
    <el-form :model="ruleForm" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-if="!isreg">
      <el-button type="primary" class="login-button-left" @click.native="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click.native="regis">注册</el-button>
      <el-form-item prop="userid">
        <el-input type="text" v-model="ruleForm.userid" auto-complete="off" placeholder="请使用注册成功的ID登录" required="required"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleForm.password" auto-complete="off" placeholder="密码" required="required"/>
      </el-form-item>
      
      <el-alert title="登录失败！" type="error" v-show="erroralert"></el-alert>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click="Login">登录</el-button>
      </el-form-item>
    </el-form>
    <el-form :model="ruleFromReg" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-else>
      <el-button type="primary" class="login-button-left" @click="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click="regis">注册</el-button>
      <el-form-item prop="username">
        <el-input type="text" v-model="ruleFromReg.username" auto-complete="off" placeholder="用户名" required="required"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleFromReg.password" auto-complete="off" placeholder="密码" required="required"/>
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
        isreg: 0,
        erroralert:0,
        ruleForm: {
          userid: '',
          password: '',
        },
        ruleFromReg: {
          username: '',
          password: '',
          IdentityPub: '',
          SignedPub: '',
          OneTimePub: '',
          Port: 8000
        },
      }
    },  
    // 查询是否有已登录的账号
    created: function () {
      this.$cookies.set("logining_userid","test")
      var logging_cookie=this.$cookies.get("logining_userid");
      if(logging_cookie){
        this.$router.push("/index")
      }
    },
    methods: {
      login() {
        this.isreg = 0;
        this.ruleFromReg.username=''
        this.ruleFromReg.password=''
        this.ruleForm.userid=''
        this.ruleForm.password=''
      },
      regis() {
        this.isreg = 1;
        this.ruleForm.userid=''
        this.ruleForm.password=''
        this.ruleFromReg.username=''
        this.ruleFromReg.password=''
      },
      Login(){
        axios.post("http://127.0.0.1:8888/apis/user/"+this.ruleForm.userid,{
          "password":sha256(this.ruleForm.password)
        }).then((response)=>{
          console.log(response.data)
          if(response.data["code"]){
            this.$cookies.set('logining_userid',this.ruleForm.userid)
            console.log(this.$cookies)
            this.erroralert=0
            this.$router.push("/index")
          }else{
            this.erroralert=1
          }
        })
      },
      Register(){
          axios.post("http://127.0.0.1:8000/apis/create_new_keyspair/",{
            headers:{
              "Content-Type":"application/json",
            }
          }).then((response)=>{
            var pubs=response.data["data"]
            console.log(response.data["data"])
            this.ruleFromReg.IdentityPub=pubs["IdentityPub"]
            this.ruleFromReg.SignedPub=pubs["SignedPub"]
            this.ruleFromReg.OneTimePub=pubs["OneTimePub"]
            axios.post("http://127.0.0.1:8888/apis/user/",{
              "username": this.ruleFromReg.username,
              "password": sha256(this.ruleFromReg.password),
              "IdentityPub": this.ruleFromReg.IdentityPub,
              "SignedPub": this.ruleFromReg.SignedPub,
              "OneTimePub": this.ruleFromReg.OneTimePub,
              "last_port": this.ruleFromReg.Port
            }).then((response)=>{
              console.log(response.data)
              if(response.data["code"]){
                const h = this.$createElement;
                this.$notify({
                  title: '注册成功的ID',
                  message: h('i', { style: 'color: teal'}, response.data["data"]),
                  duration: 0
                });
                this.isreg = 0;
                this.ruleForm.userid=''
                this.ruleForm.password=''
                this.ruleFromReg.username=''
                this.ruleFromReg.password=''
              }else{
                const h = this.$createElement;
                this.$notify({
                  title: '注册失败！',
                  message: h('i', { style: 'color: teal'}, response.data["请重新注册"]),
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
