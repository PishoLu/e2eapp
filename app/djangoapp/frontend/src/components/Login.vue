<template>
  <div class="login-container">
    <el-form :model="ruleForm" :rules="rules" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-if="!isreg">
      <el-button type="primary" class="login-button-left" @click.native="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click.native="regis">注册</el-button>
      <el-form-item prop="userid">
        <el-input type="text" v-model="ruleForm.userid" auto-complete="off" placeholder="用户ID"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleForm.password" auto-complete="off" placeholder="密码"/>
      </el-form-item>
      
      <el-alert title="登录失败！" type="error" v-show="erroralert"></el-alert>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click="Login">登录</el-button>
      </el-form-item>
    </el-form>
    <el-form :model="ruleFromReg" :rules="rulesReg" status-icon ref="ruleForm2" label-position="left" label-width="0px"
             class="demo-ruleForm login-page" v-else>
      <el-button type="primary" class="login-button-left" @click="login">登录</el-button>
      <el-button type="primary" class="login-button-right" @click="regis">注册</el-button>
      <el-form-item prop="username">
        <el-input type="text" v-model="ruleForm.userid" auto-complete="off" placeholder="用户名"/>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleForm.password" auto-complete="off" placeholder="密码"/>
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
          Port: 0
        },

        rules: {
          userid: [{required: true, message: 'please enter your account', trigger: 'blur'}],
          password: [{required: true, message: 'enter your password', trigger: 'blur'}]
        },
        rulesReg: {
          username: [{required: true, message: 'please enter your username', trigger: 'blur'}],
          password: [{required: true, message: 'enter your password', trigger: 'blur'}]
        },
      }
    },
    methods: {
      login() {
        this.isreg = 0;
      },
      regis() {
        this.isreg = 1;
      },
      Login(){
        axios.get("http://127.0.0.1:8888/apis/user/"+this.ruleForm.userid,{
          password:sha256(this.ruleForm.password)
        }).then((response)=>{
          if(reponse.data["code"]){
            Vue.$cookies.set('logining_userid',this.ruleForm.userid)
            console.log(response.data["code"])
            this.erroralert=0
          }else{
            this.erroralert=1
          }
        })
      },
      Register(){
        axios.get("http://127.0.0.1:8000/apis/gettoken/").then((reponse)=>{
          axios.post("http://127.0.0.1:8000/apis/create_new_keyspair/").then((reponse)=>{
            data=reponse.data["data"]
            console.log(data)
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
    margin: 180px auto;
    width: 350px;
    padding: 35px 35px 15px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }


  .login-button-left {
    width: 165px;
    margin: 0px 0px 10px 5px;
  }

  .login-button-right {
    width: 165px;
    margin: 0px 5px 10px 0px;
  }
</style>
