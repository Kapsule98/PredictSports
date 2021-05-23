<template>
    <div id="register">
        <h2>Register</h2>
        <label>Username</label>
        <input type="text" v-model="username"/>
        <label>Password</label>
        <input type="password" v-model="password"/>
        <button v-on:click="register()">Register</button>
    </div>    
</template>

<script>
import axios from 'axios'
import {BASE_URL} from '../../../utils/constants'
export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        init() {
            this.username = '';
            this.password = '';
        },
        register() {
            const user_info = {
                'username':this.username,
                'password': this.password
            }
            const url = BASE_URL + '/register';
            console.log(url)
            axios.post(url,user_info).then(res => {
                if(res.data.status == 200){
                    alert(res.data.msg)
                    this.$router.push('/login')
                }
                else{
                    alert(res.data.msg)
                    this.init()
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