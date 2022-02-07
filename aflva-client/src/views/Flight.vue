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
        <div v-if= "landing_vs" >
          <div>Landin rate</div>
          <span style="border: 1px dashed black;">{{landing_vs}} fpm</span>
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

export default {
  name: "Flight",
  data() {
    return {
      time: 0,
      interval: null,
      fsuipc_data: {},
      fsuipc_flag: true,
      fsuipc_status: '',
      fsuipc_interval:null,
      landing_vs: 0,
      book: this.$store.state.books[0],
      penalty: {},
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
  },
  beforeUnmount() {
    if (this.fsuipc_interval) clearInterval(this.fsuipc_interval)
  },
  watch: {
    'fsuipc_data.on_ground': function (prev, current){
      if (prev === 1 && current === 0 && !this.landing_vs){
        this.landing_vs =  this.fsuipc_data.lvs
      }
    },
    'fsuipc_data.overspeed': function (prev, current){
      if (prev === 0 && current === 1){
        this.penalty.overspeed = true
      }
    },
    'fsuipc_data.stall': function (prev, current){
      if (prev === 0 && current === 1){
        this.penalty.stall = true
      }
    },
    'fsuipc_data.crash': function (prev, current){
      if (prev === 0 && current === 1){
        this.penalty.crash = true
      }
    },

  },
  computed:{
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
      if (!this.fsuipc_data.engines && !this.landing_vs && this.fsuipc_data.on_ground) return 'On stand'
      else if (this.fsuipc_data.engines && !this.landing_vs && this.fsuipc_data.on_ground) return 'Taxiing'
      else if (this.fsuipc_data.vs > 100 && !this.fsuipc_data.on_ground) return 'Climb'
      else if (this.fsuipc_data.vs < 100 && this.fsuipc_data.vs > -100 && !this.fsuipc_data.on_ground) return 'Cruise'
      else if (this.fsuipc_data.vs < -100 && !this.fsuipc_data.on_ground) return 'Descent'
      else if (this.fsuipc_data.engines && this.landing_vs && this.fsuipc_data.on_ground) return 'Arrived'
      else if (!this.fsuipc_data.engines && this.landing_vs && this.fsuipc_data.on_ground) return 'Arrived - On Stand'
      else return ''
    }
  },
  methods: {
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
              obj.add('on_ground', 0x366, fsuipc.Type.Int16);
              obj.add('overspeed', 0x36D, fsuipc.Type.SByte);
              obj.add('stall', 0x036C, fsuipc.Type.SByte);
              obj.add('crash', 0x840, fsuipc.Type.Int16);
              obj.add('engines', 0x894, fsuipc.Type.Int16);
              return obj.process().then((result) => {
                this.fsuipc_data.latitude = result.latitude * 90.0 / (10001750.0 * 65536.0 * 65536.0)
                this.fsuipc_data.longitude = result.longitude * 360 / (65536 * 65536 * 65536 * 65536)
                this.fsuipc_data.aircraft = result.aircraft
                this.fsuipc_data.vs = Math.ceil(result.vs * 60 * 3.28084 / 256)
                this.fsuipc_data.lvs = Math.ceil(result.vs * 60 * 3.28084 / 256)
                this.fsuipc_data.altitude =Math.ceil( result.altitude/65536/65536*3.28084 );
                this.fsuipc_data.gs =Math.ceil( result.gs/65536 * 3600/1852);
                this.fsuipc_data.pause = result.pause;
                this.fsuipc_data.on_ground = result.on_ground;
                this.fsuipc_data.overspeed = result.overspeed;
                this.fsuipc_data.stall = result.stall;
                this.fsuipc_data.crash = result.crash;
                this.fsuipc_data.engines = result.engines;
                if (result.pause || result.on_ground){
                  this.pause_time()
                } else {
                  this.resume_time()
                }
                fsuipc_obj.close().then(()=>{this.fsuipc_flag = true})
              })
            })
            .catch((err) => {
              this.fsuipc_status = 'Disconnected'
              console.log(err)
              fsuipc_obj.close().then(()=>{this.fsuipc_flag = true})
            });
    },
    ask_cancel(){
      if (confirm("Are you sure you want to cancel flight?")) {
        this.$parent.flight = null
        console.log("You pressed OK!");
      } else {
        console.log("You pressed Cancel!");
      }
    },
    ask_save(){
      if (confirm("Are you sure you want to save flight?")) {
        let flight_log = this.fsuipc_data
        flight_log.landing_vs = this.landing_vs
        flight_log.time = this.time
        flight_log.penalties = this.penalty
        console.log(flight_log)
        this.$parent.flight = null
        console.log("You pressed OK!");
      } else {
        console.log("You pressed Cancel!");
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