<template>
    <div id="login">
        <label>Username</label>
        <input type="text" v-model="username"/>
        <label>Password</label>
        <input type="password" v-model="password"/>
        <button @click="login()">Submit</button>
    </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../../../utils/eventbus'
import {BASE_URL} from '../../../utils/constants'
export default {
    
    data() {
        return {
            username:'',
            password:'',
        }
    },
    methods: {
        init() {
            this.username = '';
            this.password = '';
        },
        login() {
            const url = BASE_URL + '/login'
            const payload = {
                'username':this.username,
                'password':this.password
            }
            axios.post(url,payload).then(res => {
                if(res.data.status == 200){
                    const user_info = {
                        'username': res.data.username,
                        'accesstoken': res.data.accesstoken
                    }
                    this.$session.start()
                    this.$session.set('userinfo',user_info)
                    this.$session.set('loggedin',true)
                    eventBus.$emit('login', true)
                    this.$router.push('/')
                }
                else{
                    alert(res.data.msg)
                    this.init()
                    //this.$router.push('/login')
                }
            }).catch(err => {
                console.log(err)
            })
        }
    },
    created(){
        
    }
}
</script>

<style scoped>

</style>