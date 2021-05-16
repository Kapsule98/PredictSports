<template>
  <div id="app">
    <div id="nav">
      <router-link to="/"> Home </router-link> 
      <router-link to="/about"> About </router-link> 
      <router-link v-if="!loggedin" to="/login"> Login </router-link> 
      <router-link v-if="!loggedin" to="/register"> Register </router-link> 
      <router-link v-if="loggedin" to="/logout"> Logout </router-link>
      <router-link v-if='loggedin' to="/matches"> Matches </router-link> 
      <router-link v-if='loggedin' to="/leaderboard"> Leader Board </router-link> 
    </div>
    <router-view/>
  </div>
</template>

<script>
import eventBus from '../utils/eventbus'
export default {
  data(){
    return{
      loggedin: false
    }
  },
  watch: {
  },
  created() {
    eventBus.$on('login', (data) => {
      this.loggedin = data;
      
    })
    const status = this.$session.get('loggedin')
    if(status == true){
      this.loggedin = true
    }
    else{
      this.loggedin = false
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
