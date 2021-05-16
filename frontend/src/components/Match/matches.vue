<template>
    <div id="matches">
        <h2> Premier League </h2>
        <div id="match" v-for="match,idx in matches" :key="idx">
            <div id="match-card" class="match-card" v-if="match.status == 'SCHEDULED'"> 
                {{match.homeTeam.name}} vs {{match.awayTeam.name}}
                <app-predict
                    :matchDetails="match"
                ></app-predict>
            </div>
        </div> 
    </div>
</template>

<script>
import axios from 'axios';
import {FOOTBALL_URL,FOOTBALL_KEY} from '../.././../utils/constants'
import eventBus from '../../../utils/eventbus'
import predict from '../Prediction/predict.vue'
export default {
    components: {
        'app-predict' : predict
    },
    data(){
        return {
            matches:[],
            prediction:''
        }
    },
    created() {
        this.getMatches()
    },
    methods: {
        getMatches(){
            const url = FOOTBALL_URL + 'competitions/2021/matches'
            axios.get(url, {
                headers: {
                    "X-Auth-Token": FOOTBALL_KEY,
                }
            }).then(res => {
                console.log(res);
                this.matches = res.data.matches
            }).catch(err => {
                console.log(err)
            })
        },
        logPrediction(){
            console.log(this.prediction)
        },
        redirectPrediction(match) {
            eventBus.$emit('makePrediction',match )
            this.$router.push('/predict')
        }
    },
    computed : {
      
    }
}
</script>

<style scoped>
    .match-card {
        background-color: beige;
        border: 1px solid blanchedalmond;
        padding: 1rem;
        margin: 1rem;
    }
</style>