<template>
  <div id="app">
    <div class="left">
      <div class="left_up">
        <el-input v-model="input" placeholder="请输入内容"></el-input>
      </div>
      <div class="left_down">
        <el-row class="tac">
          <el-col :span="24">
            <el-menu default-active="1" default-open="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
                <el-menu-item-group v-for="(item,index) in friends_list" :key="index">
                  <el-menu-item class="friend-item" @click="excheng_obj(item.id)">{{item.username}}</el-menu-item>
                </el-menu-item-group>
            </el-menu>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="r-up" v-if="!r_up_type">
      <ul id="content" v-for="(item,index) in message_list" :key="index">
        <li>{{item}}</li>
      </ul>
    </div>
    <div class="r-dn">
      <textarea name="" id="" cols="66" rows="20" placeholder="在这里输入" v-model="inputmsg" />
      <div class="sub_button">
        <button @click="send_message()">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'friend',
    data() {
      return {
        message_list: [],
        inputmsg: '',
        friends_list: [{
          "id":23424234,
          "username":"test",
          "last_ip":"",
          "last_port":0
        },{
          "id":23423423,
          "username":"test2",
          "last_ip":"",
          "last_port":0
        }],
        cruent_obj_id:0,
        // message区域可以分作几类，用于呈现不同的类型的消息。比如查询好友所得的消息，以及聊天记录的消息
        r_up_type:0
      }
    },
    created: function () {
      var logging_cookie=this.$cookies.get("logining_userid");
      // 获取好友列表
      // 根据好友列表探查好友的存活
      // 或许可以获取所有的消息记录
    },
    methods: {
      send_message() {
        this.list.push(this.inputmsg);
        this.inputmsg = ''
      },
      excheng_obj(id){
        console.log(id)
        this.cruent_obj_id=id
      },
      get_messages(){
        console.log("tets")
      }
    },
    watch:{
      cruent_obj_id:function(val, newval){
        console.log("watch me")
      }
    }
  }
</script>
<style scoped>
  #app {
    width: 1000px;
    margin: 0 auto;
  }

  .friend-item{
    width: 200px
  }

  .left{
    border: 1px solid pink;
    width: 20%;
  }

  .left_down {
    height: 760px;
    float: left;
    text-align: left;
  }

  .left_up{
    background-color: rgb(71, 79, 85);
    height: 40px;
    text-align: left;
  }

  .r-up {
    border: 1px solid yellow;
    width: 79%;
    height: 600px;
    float: right;
  }

  .r-dn {
    border: 1px solid deepskyblue;
    width: 79%;
    height: 200px;
    float: right;
  }

  .r-dn textarea {
    resize: none;
    width: 99%;
    border: 1px solid blue;
    height: 80%;
    float: left;
  }

  .sub_button{
    float: right;
    height: 19%;
  }

  ul {
    list-style: none;
  }

  #content {
    text-align: right;
  }
</style>
