<template>
  <div id="app">
    <el-dialog title="搜索结果" :visible.sync="dialogFormVisible" :modal-append-to-body='false'>
      <el-row>
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
          <div class="search_table_itme">{{item.id}}</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_itme">{{item.username}}</div>
        </el-col>
        <el-col :span="8">
          <div class="search_table_itme">
            <el-button type="primary" @click="add_friend(item.id)">添加</el-button>
          </div>
        </el-col>
        <el-col :span="24">
          <el-divider></el-divider>     
        </el-col>
      </el-row>
    </el-dialog>
    <div id="left">
      <div id="search_line" class=".col-md-3">
        <el-input v-model="search_input" placeholder="请输入内容" @keyup.enter.native="search_friend" required="required"
          clearable></el-input>
      </div>
      <div id="friends_list">
        <el-row class="tac">
          <el-col :span="24">
            <el-menu default-active="1" default-open="1" class="el-menu" background-color="#545c64" text-color="#fff"
              active-text-color="#ffd04b">
              <el-menu-item-group v-for="(item,index) in friends_list" :key="index">
                <el-menu-item class="friend-item" @click="excheng_obj(item.id)">{{item.username}}</el-menu-item>
              </el-menu-item-group>
            </el-menu>
          </el-col>
        </el-row>
      </div>
    </div>
    <div id="right">
      <div id="show_window" v-if="cruent_obj_id">
        <div id="show_message" >
          <el-row v-for="(item,index) in message_list" :key="index">
            <el-col :span="24" v-if="item.toUserid==logging_in"><div class="show_message_date">{{ item.date }}</div></el-col>
            <el-col :span="24" v-if="item.fromUserid==logging_in"><div class="show_message_date_self">{{item.date}}</div></el-col>
            <el-col :span="24" v-if="item.toUserid==logging_in"><div class="show_message_text">{{ item.plaintext }}</div></el-col>
            <el-col :span="24" v-if="item.fromUserid==logging_in"><div class="show_message_text_self">{{item.plaintext}}</div></el-col>
          </el-row>
        </div>
        <div id="input_box">
          <textarea type="textarea" id="textarea_box" name="" cols="50" placeholder="在这里输入"
            v-model="msg_input" autofocus></textarea>
          <div id="submit_button">
            <el-button type="primary" id="button" @click="send_message()">发送</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'friend',
    data() {
      return {
        count:20,
        loading: false,
        logging_in:234234234,
        message_num:10,
        // 该list只是对应目标的消息记录。通过侧边栏更新
        message_list: [{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:31",
          "plaintext":"testmessage1"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":23423434,
          "toUserid":234234234,
          "date":"2019年12月30日15:37:32",
          "plaintext":"testmessage2"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },{
          "fromUserid":234234234,
          "toUserid":23423434,
          "date":"2019年12月30日15:37:33",
          "plaintext":"testmessage3"
        },],
        search_input: "",
        msg_input: '',
        dialogFormVisible: false,
        friends_list: [{
          "id": 23424234,
          "username": "test",
          "last_ip": "",
          "last_port": 0
        }, {
          "id": 23423423,
          "username": "test2",
          "last_ip": "",
          "last_port": 0
        }],
        search_result: [{
          "id": 234234234,
          "username": "test3",
          "last_ip": "",
          "last_port": 0
        }, {
          "id": 234234123,
          "username": "test4",
          "last_ip": "",
          "last_port": 0
        }],
        cruent_obj_id: 0,
      }
    },
    created: function () {
      var logging_cookie = this.$cookies.get("logining_userid");
      // if(logging_cookie){
      // }else{
      //   this.$router.push("/")
      // }
      // 获取好友列表
      // 根据好友列表探查好友的存活
      // 或许可以获取所有的消息记录
    },
    computed: {
    },
    methods: {
      // 发送明文给后端加密再发送到目标的IP和端口的api
      send_message() {
        this.list.push(this.inputmsg);
        this.inputmsg = ''
      },
      // 切换当前对话目标，获取该目标的消息
      excheng_obj(id) {
        console.log(id)
        this.cruent_obj_id = id
      },
      // 对应搜索栏，启动搜索
      search_friend() {
        this.dialogFormVisible = true
      },
      // 对应搜索栏的结果添加好友操作
      add_friend(tar_id) {

      },
    },
    watch: {
      cruent_obj_id: function (val, newval) {
        console.log("watch me")
      }
    }
  }

</script>
<style scoped src="../assets/index.css">
</style>
