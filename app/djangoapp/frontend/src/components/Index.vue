<template>
<div id="app">
  <div class="left">
      <ul v-for="(item,index) in friend_list" :key="index">
        <a href="#">{{item.id+item.name}}</a>
      </ul>
  </div>
  <div class="r-up">
    <h3>聊天详情</h3>
    <ul id="content" v-for="(item,index) in list" :key="index">
    <li>{{item}}</li>
    </ul>
  </div>
  <div class="r-dn">
    <textarea name="" id="" cols="66" rows="20" placeholder="在这里输入"
    v-model="inputmsg"
    ></textarea>
    <button
    @click="submit"
    >发送</button>
  </div>
</div>
</template>

<script>
export default {
  name: 'friend',
  data () {
    return {
      list: [],
      inputmsg: '',
      friend_list:[
        {
          id:1,
          name:'张三',
        },
        {
          id:2,
          name:'李四',
        },
        {
          id:3,
          name:'王五',
        },
      ]
    }
  },
  methods :{
    submit: function(){
      this.list.push(this.inputmsg)
      this.inputmsg=''
    }
  }
}
</script>
<style scoped>
  #app{
      width: 1000px;
      margin: 0 auto;
  }
  .left{
    border: 1px solid pink;
    width: 50%;
    height: 800px;
    float: left;
  }
  .r-up{
    border: 1px solid yellow;
    width: 49%;
    height: 400px;
    float: right;
  }
  .r-dn{
    border: 1px solid deepskyblue;
    width: 49%;
    height: 400px;
    float: right;
  }
  ul{
    list-style: none;
  }
  #content{
    text-align: right;
  }
</style>
