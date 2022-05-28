<template>
  <div class="stats mt-3 text-white p-2">
    <div class="container row m-auto">
      <div class="col">
        <p>Пилотов</p>
        <h3><b>{{ this.overall_stats?.pilots }}</b></h3>
      </div>
      <div class="col">
        <p>Полетов</p>
        <h3><b>{{ this.overall_stats?.flights.count }}</b></h3>
      </div>
      <div class="col">
        <p>Самолетов</p>
        <h3><b>{{ this.overall_stats?.fleet.count }}</b></h3>
      </div>
      <div class="col">
        <p>Часов</p>
        <h3><b>{{ this.overall_stats?.flights.hours }}</b></h3>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "HomeStatsSection",
  data(){
    return{
      overall_stats: null
    }
  },
  mounted() {
    axios.get('stats/overall/').then(response=>{
      this.overall_stats = response.data
    })
  }
}
</script>

<style lang="scss" scoped>

.stats {
  background-color: #022f68;

  h3 {
    margin: 0;
  }

  p {
    margin: 0;
  }
}
</style>
