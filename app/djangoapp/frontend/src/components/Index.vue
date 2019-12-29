<template>
  <div id="app">
    <div>
    <div class="left_up">
      <el-input v-model="input" placeholder="请输入内容"></el-input>
    </div>
    <div class="left_down">
      <el-row class="tac">
        <el-col :span="24">
          <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
            background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
            <el-submenu index="1">
              <template slot="title">
                <span>好友列表</span>
              </template>
              <el-menu-item-group v-for="(item,index) in friends_list" :key="index">
                <el-menu-item @click="excheng_obj(item.id)">{{item.username}}</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
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
          "username":"test"
        },{
          "id":23423423,
          "username":"test2"
        }],
        cruent_obj_id:0,
        // message区域可以分作几类，用于呈现不同的类型的消息。比如查询好友所得的消息，以及聊天记录的消息
        r_up_type:0
      }
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
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

  .left_down {
    border: 1px solid pink;
    width: 20%;
    height: 760px;
    float: left;
    text-align: left;
  }

  .left_up{
    border: 1px solid blue;
    background-color: rgb(71, 79, 85);
    height: 40px;
    text-align: left;
    width: 20%;
  }

  .r-up {
    border: 1px solid yellow;
    width: 79%;
    height: 400px;
    float: right;
  }

  .r-dn {
    border: 1px solid deepskyblue;
    width: 79%;
    height: 400px;
    float: right;
  }

  .r-dn textarea {
    resize: none;
    width: 99%;
    border: 1px solid blue;
    height: 350px;
    float: left;
  }

  .sub_button{
    float: right;
  }

  ul {
    list-style: none;
  }

  #content {
    text-align: right;
  }
</style>
