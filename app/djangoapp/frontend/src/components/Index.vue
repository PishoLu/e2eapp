<template>
  <div id="app">
    <div class="left">
      <ul v-for="(item,index) in friend_list" :key="index">
        <a href="#">{{item.id+item.name}}</a>
      </ul>
    </div>
    <div class="r-up">
      <h3>聊天详情</h3>
      <ul id="content" v-for="(item,index) in message_list" :key="index">
        <li>{{item}}</li>
      </ul>
    </div>
    <div class="r-dn">
      <textarea name="" id="" cols="66" rows="20" placeholder="在这里输入" v-model="inputmsg"/>
      <div class="sub_button">
        <button @click="submit">发送</button>
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
        friend_list: [
          {
            id: 1,
            name: '张三',
          },
          {
            id: 2,
            name: '李四',
          },
          {
            id: 3,
            name: '王五',
          },
        ]
      }
    },
    methods: {
      submit: function () {
        this.list.push(this.inputmsg);
        this.inputmsg = ''
      }
    },
    watch:{

    }
  }
</script>
<style scoped>
  #app {
    width: 1000px;
    margin: 0 auto;
  }

  .left {
    border: 1px solid pink;
    width: 20%;
    height: 800px;
    float: left;
    text-align: left;
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
