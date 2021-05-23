<template>
    <div id = "logout">
        
    </div>
</template>
<script>
import axios from 'axios'
import {BASE_URL} from '../../../utils/constants'
import eventBus from '../../../utils/eventbus'
export default {
    created(){
        const accessToken = this.$session.get('userinfo').accesstoken
        console.log(accessToken)
        const url = BASE_URL + '/logout'
        axios.get(url, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        }).then(res => {
            console.log(res)
            alert(res.data.msg)     
            if(res.data.status == 200){
                this.$session.destroy()
                eventBus.$emit('login',false);
                this.$router.push('/')
            }
        }).catch(err => {
            console.log(err);
        })
    }
}
</script>