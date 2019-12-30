<template>
  <div id="app">
    <el-dialog title="搜索结果" :visible.sync="dialogTableVisible" :modal-append-to-body='false'>
      <el-table :data="search_result">  
        <el-table-column property="id" label="ID" width="150"></el-table-column>
        <el-table-column property="username" label="username" width="200"></el-table-column>
        <el-button type="primary">添加</el-button>
      </el-table>
    </el-dialog>
    <div id="left">
      <div id="search_line" class=".col-md-3">
        <el-input v-model="search_input" placeholder="请输入内容" @keyup.enter.native="search_friend" required="required"></el-input>
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
        <div id="show_message">
        </div>
        <div id="input_box">
          <el-input class="textarea_box" type="textarea" :rows="10" name="" cols="66"  placeholder="在这里输入" v-model="msg_input" autofocus></el-input>
          <div id="submit_button">
            <el-button type="primary" id="button">发送</el-button>
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
        message_list: [],
        search_input:"",
        msg_input: '',
        dialogTableVisible: false,
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
        search_result:[{
          "id":234234234,
          "username":"test3",
        }],
        cruent_obj_id:0,
      }
    },
    created: function () {
      var logging_cookie=this.$cookies.get("logining_userid");
      // if(logging_cookie){
      // }else{
      //   this.$router.push("/")
      // }
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
      },
      search_friend(){
        this.dialogTableVisible=true
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
      position: fixed;
      width: 100%;
      height: 100%;
      border: 1px solid blue;
    }

    #left {
      width: 160px;
      height: 100%;
      border: 1px solid red;
      position: fixed;
    }

    #right {
      width: calc(100% - 160px);
      height: 100%;
      border: 1px solid rgb(240, 8, 201);
      position: relative;
      float: right;
    }

    #search_line {
      width: 100%;
      height: 35px;
      border: 1px solid rgb(121, 121, 255);
    }

    #friends_list {
      width: 100%;
      height: 96%;
      border: 1px solid green;
    }


    #show_window {
      width: auto;
      height: 100%;
      border: 1px solid brown;
      position: relative;
    }

    #show_message{
      width: auto;
      height: 65%;
      border: 1px solid pink;
      position: relative;
      margin: 5px;
      padding: 5px;
    }

    #input_box {
      width: auto;
      height: 35%;
      border: 1px solid purple;
      position: relative;
      margin: 5px;
      padding: 5px;
    }

    #textarea_box{
      width: 100%;
      height: 60%;
      position: relative;
    }

    #submit_button {
      border: 1px solid rgb(230, 255, 7);
      width: 100%;
      height: 20%;
      position: relative;
    }

    #button {
      width: 80px;
      height: 30px;
      position: relative;
      text-align: center;
      left: 45%;
      top: 25%;
    }
</style>
