<template>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <div class="row">
        <div class="col">
          <nav aria-label="breadcrumb" class="bg-light rounded-3 p-3 mb-4">
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item"><router-link :to="{name: 'Home'}">
                Home
              </router-link></li>
              <li class="breadcrumb-item active" aria-current="page">User Profile</li>
            </ol>
          </nav>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-lg-4 mb-2">
          <div class="card h-100">
            <div class="card-body text-center">
              <img src="@/assets/img/pilot-image.png" alt="avatar"
                   class="rounded-circle img-fluid" style="width: 150px;">
              <h5 class="my-3">{{user?.get_full_name}}</h5>
              <p class="text-muted mb-1 row justify-content-center">
                <span class="col-auto"><b>{{ user.pilot.flights }}</b> flights</span>
                <span class="col-auto"><b>{{ hours }}</b> hours</span>
              </p>
              <p class="text-muted mb-1">
                <span><b>100</b> points</span>
              </p>
            </div>
          </div>
        </div>
        <div class="col-lg-8 mb-2">
          <div class="card h-100">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Full Name</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{user?.get_full_name}}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Country</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{user?.profile?.location}}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Location</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0"><b>{{user?.profile?.now}}</b></p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Callsign</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0"><b>AFL7788</b></p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Vatsim ID</p>
                </div>
                <div class="col-sm-3">
                  <p class="text-muted mb-0"><b>1300611</b></p>
                </div>
                <div class="col-sm-3">
                  <p class="mb-0">IVAO ID</p>
                </div>
                <div class="col-sm-3">
                  <p class="text-muted mb-0"><b>1000225</b></p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>

<script>
import {secToHours} from "@/utils/timeUtil";

export default {
  name: "Profile",
  data(){
    return{
      user: {}
    }
  },
  computed:{
    hours(){
      return secToHours(this.user?.pilot.hours)
    }
  },
  created() {
    if (!this.$store.getters.user){
      this.$store.dispatch('userObtain').then(()=>{
        this.user = this.$store.getters.user
      })
    } else {
      this.user = this.$store.getters.user
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
