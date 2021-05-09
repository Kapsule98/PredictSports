<template>
    <div id="login">
        <label>Username</label>
        <input type="text" v-model="username"/>
        <label>Password</label>
        <input type="password" v-model="password"/>
        <button v-on:click="login()">Submit</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    
    data() {
        return {
            username:'',
            password:'',
        }
    },
    methods: {
        login() {
            console.log('login')
            const url = 'http://127.0.0.1:5000/login'
            const payload = {
                'username':this.username,
                'password':this.password
            }
            axios.post(url,payload).then(res => {
                if(res.status == 200){
                    this.$router.push('/homepage')
                }
                else{
                    this.router.push('/login')
                }
            }).catch(err => {
                console.log(err)
            })
        }
    }
}
</script>

<style scoped>

</style>