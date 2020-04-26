<template>
  <div class="login-container">
    <el-dialog
      title="没有私钥信息，请输入私钥信息！"
      :visible.sync="dialogFormVisible"
    >
      <el-form :model="formPrikey">
        <el-form-item label="IdentityPri">
          <el-input
            v-model="formPrikey.IdentityPri"
            autocomplete="off"
            required="required"
          />
        </el-form-item>
        <el-form-item label="SignedPri">
          <el-input
            v-model="formPrikey.SignedPri"
            autocomplete="off"
            required="required"
          />
        </el-form-item>
        <el-form-item label="OneTimePri">
          <el-input
            v-model="formPrikey.OneTimePri"
            autocomplete="off"
            required="required"
          />
        </el-form-item>
        <el-form-item label="EphemeralPri">
          <el-input
            v-model="formPrikey.EphemeralPri"
            autocomplete="off"
            required="required"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="updatedPri()">确 定</el-button>
      </div>
    </el-dialog>
    <el-form
      :model="formLogin"
      :rules="formLoginRule"
      ref="formLogin"
      status-icon
      label-position="left"
      label-width="0px"
      class="demo-ruleForm login-page"
      v-if="!isreg"
    >
      <el-button
        type="primary"
        class="login-button-left"
        @click.native="changeLogin()"
        >登录</el-button
      >
      <el-button
        type="primary"
        class="login-button-right"
        @click.native="changeRegis()"
        >注册</el-button
      >
      <el-form-item prop="userid">
        <el-input
          type="text"
          v-model="formLogin.userid"
          auto-complete="off"
          placeholder="请使用注册成功的ID登录"
          required="required"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="formLogin.password"
          auto-complete="off"
          placeholder="密码"
          required="required"
        />
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          type="primary"
          style="width:100%;"
          @click="Login('formLogin')"
          >登录</el-button
        >
      </el-form-item>
    </el-form>
    <el-form
      :model="formReg"
      :rules="formRegRule"
      ref="formReg"
      status-icon
      label-position="left"
      label-width="0px"
      class="demo-ruleForm login-page"
      v-else
    >
      <el-button type="primary" class="login-button-left" @click="changeLogin()"
        >登录</el-button
      >
      <el-button
        type="primary"
        class="login-button-right"
        @click="changRregis()"
        >注册</el-button
      >
      <el-form-item prop="username">
        <el-input
          type="text"
          v-model="formReg.username"
          auto-complete="off"
          placeholder="用户名"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="formReg.password"
          auto-complete="off"
          placeholder="密码"
        />
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          type="primary"
          style="width:100%;"
          @click="Register('formReg')"
          >注册</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
import sha256 from "js-sha256";

function getCookie(cookieName) {
  var strCookie = document.cookie;
  var arrCookie = strCookie.split("; ");
  for (var i = 0; i < arrCookie.length; i++) {
    var arr = arrCookie[i].split("=");
    if (cookieName == arr[0]) {
      return arr[1];
    }
  }
  return "";
}
function isengnum(rule, value, callback) {
  const reg = /^[_a-zA-Z0-9]+$/;
  if (value == "" || value == undefined || value == null) {
    callback();
  } else {
    if (!reg.test(value)) {
      callback(new Error("仅由英文字母，数字以及下划线组成"));
    } else {
      callback();
    }
  }
}
export default {
  data() {
    return {
      dialogFormVisible: false,
      // server_csrf: "",
      // client_csrf: "",
      isreg: 0,
      formLogin: {
        userid: "",
        password: ""
      },
      formLoginRule: {
        userid: [{ required: true, message: "请输入用户id", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      formRegRule: {
        username: [
          {
            required: true,
            message: "请输入不包含空格符的英文字符串",
            trigger: "blur"
          },
          { validator: isengnum, trigger: "blur" }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      formReg: {
        username: "",
        password: "",
        IdentityPub: "",
        SignedPub: "",
        OneTimePub: "",
        EphemeralPub: "",
        IdentityPri: "",
        SignedPri: "",
        OneTimePri: "",
        EphemeralPri: ""
      },
      formPrikey: {
        IdentityPri: "",
        SignedPri: "",
        OneTimePri: "",
        EphemeralPri: ""
      },
      keys: {},
      csrftoken: ""
    };
  },
  // 查询是否有已登录的账号
  created: function() {
    // this.$cookies.set("loginingUserid", "82119217")
    var logging_cookie = this.$cookies.get("loginingUserid");
    if (logging_cookie) {
      this.$router.push("/");
    }
    // axios.get("http://localhost:8000/apis/gettoken/")
    // this.csrftoken=getCookie("csrftoken")
    // console.log(this.csrftoken)
  },
  methods: {
    changeLogin() {
      this.isreg = 0;
      this.formReg.username = "";
      this.formReg.password = "";
      this.formLogin.userid = "";
      this.formLogin.password = "";
    },
    changeRegis() {
      this.isreg = 1;
      this.formLogin.userid = "";
      this.formLogin.password = "";
      this.formReg.username = "";
      this.formReg.password = "";
    },
    Login(formLogin) {
      this.$refs["formLogin"].validate(valid => {
        if (valid) {
          axios
            .get("http://localhost:8000/apis/getUser/" + this.formLogin.userid)
            .then(response => {
              console.log(response);
              // console.log(response.data["code"]);
              if (response.data["code"] === 1) {
                var temp_data = response.data["data"][0];
                if (typeof temp_data["IdentityPri"] !== "undefined") {
                  axios
                    .post(
                      "http://127.0.0.1:8888/apis/user/" +
                        this.formLogin.userid,
                      {
                        password: sha256(this.formLogin.password)
                      }
                    )
                    .then(response => {
                      console.log(response);
                      // console.log(response.data)
                      if (response.data["code"] === 1) {
                        this.$cookies.set(
                          "loginingUserid",
                          response.data["data"]["userid"]
                        );
                        this.$router.push("/");
                      } else {
                        this.$notify.error({
                          title: "登录失败！",
                          message: "请重新登录"
                        });
                      }
                    });
                } else {
                  this.dialogFormVisible = true;
                }
              } else {
                this.dialogFormVisible = true;
              }
            })
            .catch(() => {
              this.$notify.error({
                title: "与服务器或本地后端连接出错！"
              });
            });
        } else {
          return false;
        }
      });
    },
    updatedPri() {
      this.dialogFormVisible = false;
      // 先检查私钥的格式是否有误
      axios
        .post("http://localhost:8000/apis/checkPri/", {
          IdentityPri: this.formPrikey.IdentityPri,
          SignedPri: this.formPrikey.SignedPri,
          OneTimePri: this.formPrikey.OneTimePri,
          EphemeralPri: this.formPrikey.EphemeralPri
        })
        .then(response => {
          console.log(response);
          // console.log(response.data["data"])
          if (response.data["code"] === 1) {
            // 返回的数据包括私钥字符串和公钥字符串
            this.keys = response.data["data"];
            axios
              .get("http://127.0.0.1:8888/apis/user/" + this.formLogin.userid)
              .then(response => {
                console.log(response);
                if (response.data["code"] === 1) {
                  const username_t = response.data["data"]["username"];
                  axios
                    .post("http://localhost:8000/apis/storeUser", {
                      userid: this.formLogin.userid,
                      username: username_t,
                      IdentityPub: this.keys["IdentityPub"],
                      SignedPub: this.keys["SignedPub"],
                      OneTimePub: this.keys["OneTimePub"],
                      EphemeralPub: this.keys["EphemeralPub"],
                      IdentityPri: this.keys["IdentityPri"],
                      SignedPri: this.keys["SignedPri"],
                      OneTimePri: this.keys["OneTimePri"],
                      EphemeralPri: this.keys["EphemeralPri"]
                    })
                    .then(response => {
                      console.log(response);
                      if (response.data["code"] === 1) {
                        this.$notify({
                          title: "已将当前用户添加到数据库",
                          message: "请重新登录",
                          type: "success"
                        });
                      } else {
                        this.$notify.error({
                          title: "保存用户密钥出错！",
                          message: "请重新登录"
                        });
                      }
                    });
                } else {
                  this.$notify.error({
                    title: "服务器获取用户信息失败！",
                    message: "请重新登录"
                  });
                }
              });
          } else {
            this.$notify.error({
              title: "私钥格式有误！",
              message: "请重新登录"
            });
          }
        })
        .catch(() => {
          this.$notify.error({
            title: "与服务器或本地后端连接出错！"
          });
        });
    },
    Register(formReg) {
      this.$refs["formReg"].validate(valid => {
        if (valid) {
          axios
            .post("http://localhost:8000/apis/createNewKeyspair/")
            .then(response => {
              console.log(response);
              var pubs = response.data["data"];
              // console.log(response.data["data"]);
              this.formReg.IdentityPub = pubs["IdentityPub"];
              this.formReg.SignedPub = pubs["SignedPub"];
              this.formReg.OneTimePub = pubs["OneTimePub"];
              this.formReg.EphemeralPub = pubs["EphemeralPub"];
              this.formReg.IdentityPri = pubs["IdentityPri"];
              this.formReg.SignedPri = pubs["SignedPri"];
              this.formReg.OneTimePri = pubs["OneTimePri"];
              this.formReg.EphemeralPri = pubs["EphemeralPri"];
              axios
                .post("http://127.0.0.1:8888/apis/user/", {
                  username: this.formReg.username,
                  password: sha256(this.formReg.password),
                  IdentityPub: this.formReg.IdentityPub,
                  SignedPub: this.formReg.SignedPub,
                  OneTimePub: this.formReg.OneTimePub,
                  EphemeralPub: this.formReg.EphemeralPub
                })
                .then(response => {
                  console.log(response);
                  // console.log(response.data);
                  if (response.data["code"]) {
                    const h = this.$createElement;
                    this.$notify({
                      title: "注册成功的ID:",
                      message: h(
                        "i",
                        {
                          style: "color: teal"
                        },
                        response.data["data"]
                      ),
                      type: "success",
                      duration: 0
                    });
                    axios
                      .post("http://localhost:8000/apis/storeUser/", {
                        userid: response.data["data"],
                        username: this.formReg.username,
                        IdentityPub: this.formReg.IdentityPub,
                        SignedPub: this.formReg.SignedPub,
                        OneTimePub: this.formReg.OneTimePub,
                        EphemeralPub: this.formReg.EphemeralPub,
                        IdentityPri: this.formReg.IdentityPri,
                        SignedPri: this.formReg.SignedPri,
                        OneTimePri: this.formReg.OneTimePri,
                        EphemeralPri: this.formReg.EphemeralPri
                      })
                      .then(response => {
                        console.log(response);
                      });
                    this.isreg = 0;
                    this.formLogin.userid = "";
                    this.formLogin.password = "";
                    this.formReg.username = "";
                    this.formReg.password = "";
                  } else {
                    this.$notify.error({
                      title: "注册失败！",
                      message: "请重新注册"
                    });
                  }
                });
            })
            .catch(() => {
              this.$notify.error({
                title: "与服务器或本地后端连接出错！"
              });
            });
        } else {
          return false;
        }
      });
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
