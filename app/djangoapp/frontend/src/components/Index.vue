<template>
  <div id="app">
    <el-dialog
      title="搜索结果"
      :visible.sync="dialogFormVisible"
      :modal-append-to-body="false"
    >
      <el-row v-if="!searchResult.length">
        <el-col :span="24">
          <div class="search_table_title">没有该用户相关信息</div>
        </el-col>
      </el-row>
      <el-row v-else>
        <el-col :span="8">
          <div class="search_table_title">ID</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_title">Username</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_title"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-divider></el-divider>
        </el-col>
      </el-row>
      <el-row v-for="(item, index) in searchResult" :key="index">
        <el-col :span="8">
          <div class="search_table_itme">{{ item.userid }}</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_itme">{{ item.username }}</div>
        </el-col>
        <el-col :span="8" v-if="isFriend === 1">
          <div class="search_table_itme">
            <el-button type="primary" disabled>已经是好友了</el-button>
          </div>
        </el-col>
        <el-col :span="8" v-else-if="isFriend === 2">
          <div class="search_table_itme">
            <el-button type="primary" disabled>不能添加自己哦</el-button>
          </div>
        </el-col>
        <el-col :span="8" v-else>
          <div class="search_table_itme">
            <el-button type="primary" @click="addFriend(item)">添加</el-button>
          </div>
        </el-col>
        <el-col :span="24">
          <el-divider></el-divider>
        </el-col>
      </el-row>
    </el-dialog>
    <div id="left">
      <div id="search_line" class=".col-md-3">
        <el-input
          v-model="formSearch.searchInput"
          placeholder="请输入内容"
          @keyup.enter.native="searchFriend('formSearch')"
          required="required"
          clearable
        ></el-input>
      </div>
      <div id="friendsList">
        <el-row class="tac">
          <el-col :span="24">
            <el-menu
              default-active="1"
              default-open="1"
              class="el-menu"
              background-color="#545c64"
              text-color="#fff"
              active-text-color="#ffd04b"
            >
              <el-menu-item-group
                v-for="(item, index) in friendsList"
                :key="index"
              >
                <el-menu-item
                  v-if="item.status"
                  class="friend-item"
                  @click="exchengObj(item.userid)"
                  >{{ item.username }}
                </el-menu-item>
                <el-menu-item
                  v-else-if="
                    notFriendActive === item.userid && item.status === 0
                  "
                  class="friend-item"
                  @click="showFriendOption(item.userid)"
                >
                  <el-button
                    type="success"
                    icon="el-icon-check"
                    circle
                    @click="updateFriend(item.userid)"
                  ></el-button>
                  <el-button
                    type="danger"
                    icon="el-icon-delete"
                    circle
                    @click="deleteFriend(item.userid)"
                  ></el-button>
                </el-menu-item>
                <el-menu-item
                  v-else-if="notFriendActive !== item.userid"
                  class="friend-item"
                  @click="showFriendOption(item.userid)"
                  >{{ item.username }}
                </el-menu-item>
              </el-menu-item-group>
            </el-menu>
          </el-col>
        </el-row>
      </div>
    </div>
    <div id="right">
      <div id="show_window" v-if="currentObjID">
        <div id="show_message">
          <el-row>
            <el-col :span="24">
              <div>
                <el-button
                  icon="el-icon-refresh-left"
                  id="message_get_button"
                  v-if="!messageLoading"
                  @click="messageGet()"
                >
                </el-button>
                <el-button
                  v-else
                  icon="el-icon-loading"
                  id="message_get_button"
                >
                </el-button>
              </div>
            </el-col>
          </el-row>
          <el-row v-for="(item, index) in messageList" :key="index">
            <el-col :span="24" v-if="item.fromUserid === 1">
              <div class="show_message_date_self">{{ item.date }}</div>
            </el-col>
            <el-col :span="24" v-else>
              <div class="show_message_date">{{ item.date }}</div>
            </el-col>
            <el-col :span="24" v-if="item.fromUserid === 1">
              <div class="show_message_text_self">{{ item.plaintext }}</div>
            </el-col>
            <el-col :span="24" v-else>
              <div class="show_message_text">{{ item.plaintext }}</div>
            </el-col>
          </el-row>
        </div>
        <div id="input_box">
          <el-form
            :rules="formMsgRule"
            ref="formMsg"
            id="textarea_form"
            :model="formMsg"
          >
            <textarea
              id="textarea_box"
              placeholder="在这里输入"
              v-model="formMsg.msgInput"
            ></textarea>
            <div id="submit_button">
              <el-button
                type="primary"
                id="button"
                @click="sendMessage('formMsg')"
                >发送
              </el-button>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.withCredentials = true;
export default {
  name: "friend",
  data() {
    return {
      count: 20,
      messageLoading: false,
      loginingUserid: 0,
      // 该list只是对应目标的消息记录。通过侧边栏更新
      messageList: [],
      formSearch: {
        searchInput: ""
      },
      formMsg: {
        msgInput: ""
      },
      dialogFormVisible: false,
      // 好友列表
      friendsList: [],
      // 搜索结果
      searchResult: [],
      currentObjID: 0,
      isFriend: 0,
      csrftoken: "",
      resData: {},
      notFriendActive: 0,
      tempFromUserid: 0,
      formMsgRule: {
        msgInput: [
          { required: true, message: "发送内容不能为空", trigger: "blur" }
        ]
      },
      textareaLines: 20
    };
  },
  created: function() {
    // this.csrftoken=getCookie("csrftoken")
    // this.$cookies.set("loginingUserid", "82119217");

    this.loginingUserid = this.$cookies.get("loginingUserid");
    // console.log(this.loginingUserid)
    if (this.loginingUserid) {
      // 获取好友列表
      // 根据好友列表探查好友的存活
      // 或许可以获取所有的消息记录
      this.friendsListFlash();
    } else {
      this.$router.push("/login");
    }
  },
  computed: {},
  methods: {
    // 发送明文给后端加密再发送到服务器
    // 发送消息之前需要先获取一次。防止加密顺序错乱。
    // 异步函数需要添加 async 来使用 await
    async sendMessage(formMsg) {
      // await this.messageGet();
      this.$refs["formMsg"].validate(valid => {
        if (valid) {
          axios
            .get("http://localhost:8000/apis/friendsList/" + this.currentObjID)
            .then(response => {
              if (response.data["code"] === 1) {
                // console.log(this.formMsg.msgInput);
                axios
                  .post("http://localhost:8000/apis/encryptMessage/", {
                    plaintext: this.formMsg.msgInput,
                    toUserid: this.currentObjID
                  })
                  .then(response => {
                    // console.log(response);
                    if (response.data["code"] === 1) {
                      this.resData = response.data["data"];
                      axios
                        .post("http://127.0.0.1:8888/apis/message/", {
                          fromUserid: this.resData["fromUserid"],
                          toUserid: this.resData["toUserid"],
                          message: this.resData["message"]
                        })
                        .then(response => {
                          // console.log(response);
                          if (response.data["code"] === 1) {
                            axios
                              .post(
                                "http://localhost:8000/apis/storeMessage/",
                                {
                                  fromUserid: this.resData["fromUserid"],
                                  toUserid: this.resData["toUserid"],
                                  kdf_next: this.resData["kdf_next"],
                                  EphemeralPub: this.resData["message"][
                                    "EphemeralPub"
                                  ],
                                  EphemeralPri: this.resData["EphemeralPri"],
                                  plaintext: this.resData["plaintext"]
                                }
                              )
                              .then(response => {
                                if (response.data["code"] === 1) {
                                  this.messageListFlash();
                                } else {
                                  this.$notify.error({
                                    title: "储存消息到本地失败。",
                                    message: "请重新发送消息。"
                                    // type: 'success'
                                  });
                                }
                              });
                          } else {
                            this.$notify.error({
                              title: "上传消息到服务器失败。",
                              message: "请重新发送消息。"
                              // type: 'success'
                            });
                          }
                        });
                    } else {
                      this.$notify.error({
                        title: "本地加密失败。",
                        message: "请重新发送消息。"
                        // type: 'success'
                      });
                    }
                    this.formMsg.msgInput = "";
                  });
              } else {
                axios
                  .get("http://127.0.0.1:8888/apis/user/" + id)
                  .then(response => {
                    if (response.data["code"] === 1) {
                      var getData = response.data["data"];
                      axios.post("http://localhost:8000/apis/storeFriend/", {
                        userid: getData["userid"],
                        username: getData["username"],
                        remark: "",
                        status: 1,
                        IdentityPub: getData["IdentityPub"],
                        SignedPub: getData["SignedPub"],
                        OneTimePub: getData["OneTimePub"],
                        EphemeralPub: getData["EphemeralPub"]
                      });
                    }
                  })
                  .then(response => {
                    this.$notify.error({
                      title: "已添加好友信息到数据库",
                      message: "请重新输入。"
                      // type: 'success'
                    });
                  });
              }
            });
        } else {
          return false;
        }
      });
    },
    // 只能通过刷新消息列表来完成接收消息了
    messageGet() {
      this.messageLoading = true;
      axios.get("http://127.0.0.1:8888/apis/message/").then(response => {
        if (response.data["code"] === 1) {
          var getData = response.data["data"];
          // 循环解析数据包，判断消息源是否为好友并处理
          console.log(getData);
          for (var i = 0; i < getData.length; i++) {
            // 返回的列表中的数据的某一个数据包的来源
            this.tempFromUserid = getData[i][fromUserid];
            axios
              .get(
                "http://localhost:8000/apis/friendsList" + int(tempFromUserid)
              )
              .then(response => {
                if (response.data["code"] === 1) {
                  // 说明消息来源是好友
                  // 是好友的话就可以直接解密了
                } else {
                  // 消息来源不是好友
                  // 添加到数据库，但是status为0
                  axios
                    .get("http://127.0.0.1:8888/user/" + int(tempFromUserid))
                    .then(response => {
                      if (response.data["code"] === 1) {
                        // 获取目标服务器信息9-***
                        var postData = response.data["data"];
                        // 保存到好友数据库并设置status为0
                        axios
                          .post("http://localhost:8000/apis/sotre_friend/", {
                            userid: postData["userid"],
                            username: postData["username"],
                            remark: "",
                            status: 0,
                            IdentityPub: postData["IdentityPub"],
                            SignedPub: postData["SignedPub"],
                            OneTimePub: postData["OneTimePub"],
                            EphemeralPub: postData["EphemeralPub"]
                          })
                          .then(response => {
                            if (response.data["code"] === 1) {
                              this.$notify({
                                title: "待定好友添加成功",
                                // message: "请重新获取。",
                                type: "success"
                              });
                            } else {
                              this.$notify.error({
                                title: "待定好友添加失败。",
                                message: "请重新获取。"
                                // type: 'success'
                              });
                            }
                          });
                      } else {
                        this.$notify.error({
                          title: "获取服务器记录失败。",
                          message: "请重新获取。"
                          // type: 'success'
                        });
                      }
                    });
                }
              });
          }
          // 好友已经都添加了
          // 这里两个for循环应该是可以错开的。
          for (var i = 0; i < getData.length; i++) {
            // 开始解密，单个数据包传给 decryptMessage
            axios
              .post("http://localhost:8000/apis/decryptMessage/", {
                fromUserid: getData["fromUserid"],
                toUserid: getData["toUserid"],
                date: getData["date"],
                message: getData["message"]
              })
              .then(response => {});
          }
          this.messageLoading = false;
          // axios
          //   .post("http://127.0.0.1:8000/apis/decryptMessage/", {
          //     server_data: getData
          //   })
          //   .then(response => {

          //   });
        } else {
          this.$notify.error({
            title: "获取服务器记录失败。",
            message: "请重新获取。"
            // type: 'success'
          });
          this.messageLoading = false;
        }
      });
    },
    // 切换当前对话目标，获取该目标的消息
    exchengObj(id) {
      // console.log(id)
      this.currentObjID = id;
      this.notFriendActive = 0;
      this.messageListFlash();
    },
    messageListFlash() {
      axios
        .get("http://localhost:8000/apis/filterMessages/" + this.currentObjID, {
          headers: {
            // "loginingUserid":this.loginingUserid
          }
        })
        .then(response => {
          if (response.data["code"] === 1) {
            console.log(response.data);
            this.messageList = response.data["data"];
            // console.log(this.messageList);
          } else {
            this.$notify.error({
              title: "获取历史记录失败，或者记录为空。",
              message: "刷新一下。"
              // type: 'success'
            });
          }
        });
    },
    // 对应搜索栏，启动搜索
    searchFriend(formSearch) {
      // console.log(this.searchResult)

      this.searchResult = [];
      axios
        .get("http://127.0.0.1:8888/apis/user/" + this.formSearch.searchInput)
        .then(response => {
          if (response.data["code"] === 1) {
            // console.log(response.data["data"]);
            // 返回结果应该是只有一个
            this.searchResult.push(response.data["data"]);
            // console.log(
            // this.searchResult[0]["userid"] === parseInt(this.loginingUserid)
            // );
            for (var i = 0; i < this.friendsList.length; i++) {
              // console.log(this.searchResult)
              if (
                this.friendsList[i]["userid"] === this.searchResult[0]["userid"]
              ) {
                this.isFriend = 1;
              } else if (
                this.searchResult[0]["userid"] === parseInt(this.loginingUserid)
              ) {
                this.isFriend = 2;
              } else {
                this.isFriend = 0;
              }
            }
          } else {
            this.$notify.error({
              title: "搜索失败！",
              message: "请稍后重试。"
              // type: 'success'
            });
          }
        });
      this.dialogFormVisible = true;
    },
    friendsListFlash() {
      axios
        .get("http://localhost:8000/apis/friendsList/", {
          headers: {
            // "loginingUserid":this.loginingUserid
          }
        })
        .then(response => {
          if (response.data["code"] === 1) {
            // console.log(response.data)
            this.friendsList = response.data["data"];
          } else {
            this.$notify.error({
              title: "获取好友列表失败，或者好友列表为空。",
              message: "重启一下应用看看？"
              // type: 'success'
            });
          }
        });
    },
    showFriendOption(index) {
      this.notFriendActive = index;
      this.currentObjID = 0;
      // console.log(index);
      // document.getElementById("not_friend");
    },
    // 对应搜索栏的结果添加好友操作
    addFriend(fri_item) {
      // console.log(fri_item)
      axios
        .post("http://localhost:8000/apis/storeFriend/", {
          userid: fri_item.userid,
          username: fri_item.username,
          remark: "",
          status: 1,
          IdentityPub: fri_item.IdentityPub,
          SignedPub: fri_item.SignedPub,
          OneTimePub: fri_item.OneTimePub,
          EphemeralPub: fri_item.EphemeralPub,
          headers: {
            // "X-CSRFToken":this.csrftoken
          }
        })
        .then(response => {
          if (response.data["code"] === 1) {
            this.dialogFormVisible = false;
            this.$notify({
              title: "添加成功！",
              message: "已将好友添加到列表。",
              type: "success"
            });
            this.friendsListFlash();
          } else {
            this.dialogFormVisible = false;
            this.$notify.error({
              title: "添加失败！",
              message: "请稍后重试。"
              // type: 'success'
            });
          }
        });
    }
  },
  updateFriend(userid) {
    axios
      .put("http://localhost:8000/apis/storeFriend/", {
        userid: userid
      })
      .then(response => {
        if (response.data["code"] === 1) {
          this.$notify({
            title: "添加成功！",
            // message: "请稍后重试"
            type: "success"
          });
        } else {
          this.$notify.error({
            title: "添加失败！",
            message: "请稍后重试。"
            // type: 'success'
          });
        }
      });
  },
  deleteFriend(userid) {
    axios
      .delete("http://localhost:8000/apis/storeFriend/", {
        userid: userid
      })
      .then(response => {
        if (response.data["code"] === 1) {
          this.$notify({
            title: "删除成功！",
            // message: "请稍后重试"
            type: "success"
          });
        } else {
          this.$notify.error({
            title: "删除失败！",
            message: "请稍后重试。"
            // type: 'success'
          });
        }
      });
  },
  watch: {
    currentObjID: function(val, newval) {
      // console.log("watch me")
    }
  }
};
</script>
<style scoped src="../assets/index.css"></style>
