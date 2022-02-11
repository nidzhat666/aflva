<template>
  <div class="flight m-3" v-if="Object.keys(book).length">
    <div class="row mt-3">
      <div class="col">
        <div>Altitude</div>
        <span>{{fsuipc_data.altitude}} ft</span>
      </div>
      <div class="col">
        <div>Ground Speed</div>
        <span>{{fsuipc_data.gs}} kts</span>
      </div>
      <div class="col">
        <div v-if= "fsuipc_data.landing_vs" >
          <div>Landing rate</div>
          <span style="border: 1px dashed black;">{{fsuipc_data.landing_vs}} fpm</span>
        </div>
        <div v-else>
          <div>Vertical Speed</div>
          <span>{{fsuipc_data.vs}} fpm</span>
        </div>
      </div>
      <div class="col">
        <div>Time in the air</div>
        <span>{{normal_time}}</span>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div>Fsuipc Status</div>
        <span :style="[fsuipc_status==='Connected' ? {'background-color': '#00800070'} : {'background-color': '#ff00007d'} ]">{{fsuipc_status}}</span>
      </div>
      <div class="col">
        <div>Flight Status</div>
        <span>{{status}}</span>
      </div>
      <div class="col col-sm-6">
        <div>Aircraft Name</div>
        <span>{{fsuipc_data.aircraft}}</span>
      </div>
    </div>
    <div class="mt-3">
      <button class="btn  btn-danger m-1"  @click="ask_cancel()">Cancel</button>
      <button class="btn btn-secondary m-1"  @click="ask_save()">Send</button>
    </div>
  </div>
</template>

<script>
import fsuipc from 'fsuipc'
import axios from 'axios'
import {version} from "../../package.json";

function calcCrow(latitude1, longitude1, latitude2, longitude2)
{
  let R = 3440.0348679829;
  let dLat = toRad(latitude2-latitude1);
  let dLon = toRad(longitude2-longitude1);
  let lat1 = toRad(latitude1);
  let lat2 = toRad(latitude2);

  let a = Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2);
  let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  let d = R * c;
  return d;
}

function toRad(Value)
{
  return Value * Math.PI / 180;
}

export default {
  name: "Flight",
  data() {
    return {
      stopwatch: {
        start: performance.now(),
        end: performance.now(),
      },
      time:0,
      interval: null,
      fsuipc_flag: true,
      fsuipc_status: 'Disconnected',
      fsuipc_interval:null,
      book: this.$store.state.books[0],
      fsuipc_data: {
        client_version:version,
        flight_time: 0,
        aircraft:this.$store.state.books[0].aircraft.aircraft_type.aircraft_name,
        distance_flown:0,
        vs:0,
        altitude:0,
        gs:0,
        landing_vs: 0,
        book: this.$store.state.books[0].id
      },
      error: {
        message: false,
      },
    }
  },
  created() {
    this.fsuipc_interval = setInterval(this.getFsuipc, 1000)
  },
  mounted() {
    setTimeout(function() {
      this.interval = setInterval(()=>{this.time++}, 1000)
    }, 2000)
    this.status_update_interval = setInterval(this.status_update, 5000)
    setInterval(this.set_time_duration, 1000)
  },
  beforeUnmount() {
    if (this.fsuipc_interval) clearInterval(this.fsuipc_interval)
    if (this.status_update_interval) clearInterval(this.status_update_interval)
  },
  watch: {
    status: function (prev){
      if (prev === 'Taxiing') {
        if (!this.fsuipc_data.dep_time){
          this.fsuipc_data.dep_fuel = this.fsuipc_data.fuel
          this.fsuipc_data.dep_tw = this.fsuipc_data.tw
          this.fsuipc_data.dep_zfw = this.fsuipc_data.zfw
          this.fsuipc_data.dep_time = new Date().toISOString()
        }

      }
    },
    'fsuipc_data.coordinates': function (prev, current){
      if (prev && current) this.fsuipc_data.distance_flown += calcCrow(prev[0],prev[1],current[0],current[1])
    },
    'fsuipc_data.on_ground': function (prev, current){
      if (prev === 1 && current === 0 && !this.fsuipc_data.landing_vs){
        this.fsuipc_data.landing_vs =  this.fsuipc_data.lvs
        this.fsuipc_data.arr_time = new Date().toISOString()
      }
    },
    'fsuipc_data.overspeed': function (prev, current){
      if (prev === 0 && current === 1){
        this.fsuipc_data.penalty.overspeed = true
      }
    },
    'fsuipc_data.stall': function (prev, current){
      if (prev === 0 && current === 1){
        this.fsuipc_data.penalty.stall = true
      }
    },
    'fsuipc_data.crash': function (prev, current){
      if (prev === 0 && current === 1){
        this.fsuipc_data.penalty.crash = true
      }
    },

  },
  computed:{
    stopwatch_duration: function (){
      return this.stopwatch.end ? this.stopwatch.end - this.stopwatch.start : performance.now() - this.stopwatch.start
    },
    stopwatch_running: function (){
      return !this.stopwatch.end
    },
    normal_time: function(){
      let sec_num = this.time
      let hours   = Math.floor(sec_num / 3600);
      let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
      let seconds = sec_num - (hours * 3600) - (minutes * 60);

      if (hours   < 10) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      if (seconds < 10) {seconds = "0"+seconds;}
      return hours+':'+minutes+':'+seconds;
    },
    status: function(){
      if (!this.fsuipc_data.engines && !this.fsuipc_data.landing_vs && this.fsuipc_data.on_ground) return 'On stand'
      else if (this.fsuipc_data.engines && !this.fsuipc_data.landing_vs && this.fsuipc_data.on_ground) return 'Taxiing'
      else if (this.fsuipc_data.vs > 100 && !this.fsuipc_data.on_ground) return 'Climb'
      else if (this.fsuipc_data.vs < 100 && this.fsuipc_data.vs > -100 && !this.fsuipc_data.on_ground) return 'Cruise'
      else if (this.fsuipc_data.vs < -100 && !this.fsuipc_data.on_ground) return 'Descent'
      else if (this.fsuipc_data.engines && this.fsuipc_data.landing_vs && this.fsuipc_data.on_ground) return 'Arrived'
      else if (!this.fsuipc_data.engines && this.fsuipc_data.landing_vs && this.fsuipc_data.on_ground) return 'Arrived - On Stand'
      else return ''
    }
  },
  methods: {
    set_time_duration(){
      let duration = this.stopwatch.end ? this.stopwatch.end - this.stopwatch.start : performance.now() - this.stopwatch.start
      this.time = Math.floor(duration/1000)
    },
    stopwatch_start(){
      if (!this.stopwatch_running){
        this.stopwatch.start = performance.now() - this.stopwatch_duration
        this.stopwatch.end = null
      }
    },
    stopwatch_stop(){
      if (this.stopwatch_running){
        this.stopwatch.end = performance.now()
      }
    },
    status_update(){
      axios.patch('https://afl-va.ru/api/books/0/', {
            status: this.status,
            latitude: this.fsuipc_data.latitude,
            longitude: this.fsuipc_data.longitude,
            altitude: this.fsuipc_data.altitude,
            speed: this.fsuipc_data.gs,
            _method: 'patch'
          },
          {
            headers: {
              Authorization: 'Token ' + this.$store.getters.getToken
            }
          }
      ).then(() => {
      }).catch(() => {
      });
    },
    getFsuipc() {
      if(!this.fsuipc_flag){return;}
        let fsuipc_obj = new fsuipc.FSUIPC();
        fsuipc_obj.open()
            .then((obj) => {
              this.fsuipc_flag = false
              this.fsuipc_status = 'Connected'
              obj.add('latitude', 0x560, fsuipc.Type.UInt64);
              obj.add('longitude', 0x568, fsuipc.Type.UInt64);
              obj.add('altitude', 0x570, fsuipc.Type.UInt64);
              obj.add('gs', 0x2B4, fsuipc.Type.UInt32);
              obj.add('aircraft', 0x3160, fsuipc.Type.String, 64);
              obj.add('pause', 0x264, fsuipc.Type.Int16);
              obj.add('vs', 0x02C8, fsuipc.Type.Int16);
              obj.add('lvs', 0x30C, fsuipc.Type.Int16);
              obj.add('zfw', 0x3BFC, fsuipc.Type.UInt32);
              obj.add('tw', 0x30C0, fsuipc.Type.Double);
              obj.add('on_ground', 0x366, fsuipc.Type.Int16);
              obj.add('overspeed', 0x36D, fsuipc.Type.SByte);
              obj.add('stall', 0x036C, fsuipc.Type.SByte);
              obj.add('crash', 0x840, fsuipc.Type.Int16);
              obj.add('engines', 0x894, fsuipc.Type.Int16);
              return obj.process().then((result) => {
                this.fsuipc_data.latitude = result.latitude * 90.0 / (10001750.0 * 65536.0 * 65536.0)
                this.fsuipc_data.longitude = result.longitude * 360 / (65536 * 65536 * 65536 * 65536)
                this.fsuipc_data.coordinates = [this.fsuipc_data.latitude, this.fsuipc_data.longitude]
                this.fsuipc_data.aircraft = result.aircraft
                this.fsuipc_data.vs = Math.ceil(result.vs * 60 * 3.28084 / 256)
                this.fsuipc_data.lvs = Math.ceil(result.vs * 60 * 3.28084 / 256)
                this.fsuipc_data.zfw = Math.ceil((result.zfw/256)*0.45359237)
                this.fsuipc_data.tw = Math.ceil(result.tw*0.45359237)
                this.fsuipc_data.fuel = this.fsuipc_data.tw - this.fsuipc_data.zfw
                this.fsuipc_data.altitude =Math.ceil( result.altitude/65536/65536*3.28084 );
                this.fsuipc_data.gs =Math.ceil( result.gs/65536 * 3600/1852);
                this.fsuipc_data.pause = result.pause;
                this.fsuipc_data.on_ground = result.on_ground;
                this.fsuipc_data.overspeed = result.overspeed;
                this.fsuipc_data.stall = result.stall;
                this.fsuipc_data.crash = result.crash;
                this.fsuipc_data.engines = result.engines;
                if (result.pause || result.on_ground){
                  this.stopwatch_stop()
                } else {
                  this.stopwatch_start()
                }
                fsuipc_obj.close().then(()=>{this.fsuipc_flag = true})
              })
            })
            .catch((err) => {
              this.fsuipc_status = 'Disconnected'
              this.stopwatch_stop()
              console.log(err)
              fsuipc_obj.close().then(()=>{this.fsuipc_flag = true})
            });
    },
    ask_cancel(){
      if (confirm("Are you sure you want to cancel flight?")) {
        this.$parent.flight = null
      }
    },
    ask_save(){
      if (confirm("Are you sure you want to save flight?")) {
        let flight_log = this.fsuipc_data
        flight_log.flight_time = this.time
        flight_log.distance_flown = Math.ceil(flight_log.distance_flown)
        axios.post('https://afl-va.ru/api/flights/',
            {fsuipc_data: flight_log},
            {
              headers: {
                Authorization: 'Token ' + this.$store.getters.getToken
              }
            }
        ).then(() => {
          this.$parent.reqBooks()
        }).catch(() => {
        });
      }
    },
    pause_time(){
      if (this.interval) {
        clearInterval(this.interval)
        this.interval = null
      }
    },
    resume_time() {
      if (!this.interval) {
        this.interval = setInterval(()=>{this.time++}, 1000)
      }
    },
    setErrorMessage(message) {
      this.error.message = message
    },
  }
}
</script>

<style lang="scss" scoped>
.flight {
  div > div {
    div {
      font-weight: bold;
    }

    span {
      background-color: #f5f5f5;
      padding: 2px 15px;
      display: block;
      font-weight: normal;
      box-sizing: border-box;
      border: 1px solid black;
    }
  }
}
</style>