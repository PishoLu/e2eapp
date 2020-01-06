<template>
  <div id="app">
    <el-dialog
      title="搜索结果"
      :visible.sync="dialogFormVisible"
      :modal-append-to-body="false"
    >
      <el-row v-if="!search_result.length">
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
      <el-row v-for="(item, index) in search_result" :key="index">
        <el-col :span="8">
          <div class="search_table_itme">{{ item.userid }}</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_itme">{{ item.username }}</div>
        </el-col>
        <el-col :span="8" v-if="is_friend === 1">
          <div class="search_table_itme">
            <el-button type="primary" disabled>已经是好友了</el-button>
          </div>
        </el-col>
        <el-col :span="8" v-else-if="is_friend === 2">
          <div class="search_table_itme">
            <el-button type="primary" disabled>不能添加自己哦</el-button>
          </div>
        </el-col>
        <el-col :span="8" v-else>
          <div class="search_table_itme">
            <el-button type="primary" @click="add_friend(item)">添加</el-button>
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
          v-model="search_input"
          placeholder="请输入内容"
          @keyup.enter.native="search_friend"
          required="required"
          clearable
        ></el-input>
      </div>
      <div id="friends_list">
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
                v-for="(item, index) in friends_list"
                :key="index"
              >
                <el-menu-item
                  class="friend-item"
                  @click="excheng_obj(item.userid)"
                  >{{ item.username }}
                </el-menu-item>
              </el-menu-item-group>
            </el-menu>
          </el-col>
        </el-row>
      </div>
    </div>
    <div id="right">
      <div id="show_window" v-if="current_obj_id">
        <div id="show_message">
          <el-row>
            <el-col :span="24">
              <div>
                <el-button
                  icon="el-icon-refresh-left"
                  id="message_get_button"
                  v-if="!message_loading"
                  @click="message_get()"
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
          <el-row v-for="(item, index) in message_list" :key="index">
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
          <textarea
            id="textarea_box"
            name=""
            cols="50"
            placeholder="在这里输入"
            v-model="msg_input"
            autofocus
            required="required"
          ></textarea>
          <div id="submit_button">
            <el-button type="primary" id="button" @click="send_message()"
              >发送</el-button
            >
          </div>
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
      message_loading: false,
      loading: false,
      logining_userid: 0,
      // 该list只是对应目标的消息记录。通过侧边栏更新
      message_list: [],
      search_input: "",
      msg_input: "",
      dialogFormVisible: false,
      // 好友列表
      friends_list: [],
      // 搜索结果
      search_result: [],
      current_obj_id: 0,
      is_friend: 0,
      csrftoken: "",
      res_data: {}
    };
  },
  created: function() {
    // this.csrftoken=getCookie("csrftoken")
    this.logining_userid = this.$cookies.get("logining_userid");
    // console.log(this.logining_userid)
    if (this.logining_userid) {
      // 获取好友列表
      // 根据好友列表探查好友的存活
      // 或许可以获取所有的消息记录
      this.friends_list_flash();
    } else {
      this.$router.push("/login");
    }
  },
  computed: {},
  methods: {
    // 发送明文给后端加密再发送到服务器
    // 发送消息之前需要先获取一次。防止加密顺序错乱。
    send_message() {
      this.message_get().then(
        axios
          .get("http://localhost:8000/apis/friends_list/" + this.current_obj_id)
          .then(response => {
            if (response.data["code"] === 1) {
              // console.log(this.msg_input),
              axios
                .post("http://localhost:8000/apis/encrypt_message/", {
                  plaintext: this.msg_input,
                  toUserid: this.current_obj_id
                })
                .then(response => {
                  if (response.data["code"] === 1) {
                    this.res_data = response.data["data"];
                    axios
                      .post("http://127.0.0.1:8888/apis/message/", {
                        fromUserid: this.res_data["fromUserid"],
                        toUserid: this.res_data["toUserid"],
                        ciphertext: this.res_data["message"]
                      })
                      .then(response => {
                        if (response.data["code"] === 1) {
                          axios
                            .post("http://localhost:8000/apis/store_message/", {
                              fromUserid: this.res_data["fromUserid"],
                              toUserid: this.res_data["toUserid"],
                              kdf_next: this.res_data["kdf_next"],
                              EphemeralPub: this.res_data["message"][
                                "EphemeralPub"
                              ],
                              plaintext: this.res_data["plaintext"]
                            })
                            .then(response => {
                              if (response.data["code"] === 1) {
                                this.message_list_flash();
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
                  this.msg_input = "";
                });
            } else {
              axios
                .get("http://127.0.0.1:8888/apis/user/" + id)
                .then(response => {
                  if (response.data["code"] === 1) {
                    var get_data = response.data["data"];
                    axios.post("http://localhost:8000/apis/store_friend/", {
                      userid: get_data["userid"],
                      username: get_data["username"],
                      remark: "",
                      status: 1,
                      IdentityPub: get_data["IdentityPub"],
                      SignedPub: get_data["SignedPub"],
                      OneTimePub: get_data["OneTimePub"],
                      EphemeralPub: get_data["EphemeralPub"]
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
          })
      );
    },
    // 只能通过刷新消息列表来完成接收消息了
    message_get() {
      this.message_loading = true;
      axios.get("http://127.0.0.1:8888/apis/message/").then(response => {
        if (response.data["code"] === 1) {
          get_data = response.data["data"];
        }
      });
    },
    // 切换当前对话目标，获取该目标的消息
    excheng_obj(id) {
      // console.log(id)
      this.current_obj_id = id;
      this.message_list_flash();
    },
    message_list_flash() {
      axios
        .get(
          "http://localhost:8000/apis/filter_messages/" + this.current_obj_id,
          {
            headers: {
              // "logining_userid":this.logining_userid
            }
          }
        )
        .then(response => {
          if (response.data["code"] === 1) {
            // console.log(response.data);
            this.message_list = response.data["data"];
            // console.log(this.message_list);
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
    search_friend() {
      // console.log(this.search_result)
      this.search_result = [];
      axios
        .get("http://127.0.0.1:8888/apis/user/" + this.search_input)
        .then(response => {
          if (response.data["code"] === 1) {
            // console.log(response.data["data"])
            // 返回结果应该是只有一个
            this.search_result.push(response.data["data"]);
            if (
              this.search_result[0]["userid"] === parseInt(this.logining_userid)
            ) {
              this.is_friend = 2;
            } else {
              this.is_friend = 0;
            }
            for (var i = 0; i < this.friends_list.length; i++) {
              // console.log(this.search_result)
              if (
                this.friends_list[i]["userid"] ===
                this.search_result[0]["userid"]
              ) {
                this.is_friend = 1;
              } else {
                this.is_friend = 0;
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
    friends_list_flash() {
      axios
        .get("http://localhost:8000/apis/friends_list/", {
          headers: {
            // "logining_userid":this.logining_userid
          }
        })
        .then(response => {
          if (response.data["code"] === 1) {
            // console.log(response.data)
            this.friends_list = response.data["data"];
          } else {
            this.$notify.error({
              title: "获取好友列表失败，或者好友列表为空。",
              message: "重启一下应用看看？"
              // type: 'success'
            });
          }
        });
    },
    // 对应搜索栏的结果添加好友操作
    add_friend(fri_item) {
      // console.log(fri_item)
      axios
        .post("http://localhost:8000/apis/store_friend/", {
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
            this.friends_list_flash();
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
  watch: {
    current_obj_id: function(val, newval) {
      // console.log("watch me")
    }
  }
};
</script>
<style scoped src="../assets/index.css"></style>
