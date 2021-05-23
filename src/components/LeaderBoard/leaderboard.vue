<template>
    <div id = 'leaderboard'>
        Name - Score
        <div id="user" v-for="(user, idx) in users" :key="idx">
            {{user.username}} {{user.score}}
        </div>
    </div>    
</template>

<script>
import axios from 'axios';
import {BASE_URL} from '../../../utils/constants'
export default {
    data() {
        return {
            users: []
        }
    },
    created() {
        this.getUsers()
    },
    methods: {
        getUsers(){
            console.log("get users called")
            const accessToken = this.$session.get('userinfo').accesstoken
            const url = BASE_URL + '/user'
            axios.get(url, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            }).then(res => {
                console.log(res)
                this.users = res.data.data
            }).catch(err => {
                console.log(err);
            })
        }
    }
}
</script>

<style scoped>

</style>