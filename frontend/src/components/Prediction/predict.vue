<template>
    <div id="match">
        <label for="match">Choose a result:</label>
        <select name="match" id="match" v-model="prediction">
            <option value="HOME_TEAM">{{matchDetails.homeTeam.name}}</option>
            <option value="DRAW">Draw</option>
            <option value="AWAY_TEAM">{{matchDetails.awayTeam.name}}</option>
        </select>
        <button :disabled="prediction === 'none'" @click="makePrediction()">Predict</button>
    </div>
</template>

<script>
import axios from 'axios'
import { BASE_URL } from '../../../utils/constants'
export default {
    props : ['matchDetails'],
    created(){
    },
    data() {
        return {
            prediction:'none',
            selectedval:''
        }
    },
    methods: {
        makePrediction(){
            const payload = {
                "matchid": this.matchDetails.id,
                "username": this.$session.get('userinfo').username,
                "prediction": {
                    "winner": this.prediction
                }
            }
            const url = BASE_URL + '/makeprediction'
            const accessToken = this.$session.get('userinfo').accesstoken;
            const options = {
                headers : {
                    Authorization: `Bearer ${accessToken}`
                },
            }
            console.log(payload);
            axios.post(url ,payload,options).then(res => {
                console.log(res)
            }).catch(err => {
                console.log(err)
            })
        },
    }
}
</script>

<style scoped>

</style>