<template>
    <div>
        <h2>Homepage</h2>
        <p>{{ msg }}</p>
    </div>
</template>
<script>
export default {
    data(){
        return {
            session_user_info : '',
            msg: ''
        }
    },
    created(){
        this.session_user_info = this.$session.get('userinfo')
        if(this.session_user_info){
            this.msg = this.session_user_info.username
        }
        else{
            this.msg = "login to view this page"
        }
    }
}
</script>
<style scoped>

</style>