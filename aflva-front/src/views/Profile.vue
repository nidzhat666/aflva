<template>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <div class="row">
        <div class="col">
          <nav aria-label="breadcrumb" class="bg-light rounded-3 p-3 mb-4">
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item">
                <router-link :to="{name: 'Home'}">
                  Home
                </router-link>
              </li>
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
              <p class="placeholder-glow m-0" v-if="!user">
                <span class="placeholder col-12"></span>
              </p>
              <h5 class="my-3" v-else>{{ user?.get_full_name }}</h5>
              <p class="placeholder-glow m-0" v-if="!user">
                <span class="placeholder col-12"></span>
              </p>
              <p class="text-muted mb-1 row justify-content-center" v-else>
                <span class="col-auto"><b>{{ user?.pilot.flights }}</b> flights</span>
                <span class="col-auto" :title="full_hours"><b>{{ hours }}</b> hours</span>
              </p>
              <p class="placeholder-glow m-0" v-if="!user">
                <span class="placeholder col-12"></span>
              </p>
              <p class="text-muted mb-1" v-else>
                <span><b>{{ user?.pilot.rating }}</b> points</span>
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
                  <p class="placeholder-glow m-0" v-if="!user">
                    <span class="placeholder col-12"></span>
                  </p>
                  <p class="text-muted mb-0" v-else>{{ user?.get_full_name }}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Country</p>
                </div>
                <div class="col-sm-9">
                  <p class="placeholder-glow m-0" v-if="!user">
                    <span class="placeholder col-12"></span>
                  </p>
                  <p class="text-muted mb-0" v-else>{{ user?.profile.location }}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Location</p>
                </div>
                <div class="col-sm-9">
                  <p class="placeholder-glow m-0" v-if="!user">
                    <span class="placeholder col-12"></span>
                  </p>
                  <p class="text-muted mb-0" :title="user?.pilot.now.name" ref="info" v-else>
                    <b>{{ user?.pilot.now.icao_code }}</b></p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Callsign</p>
                </div>
                <div class="col-sm-9">
                  <p class="placeholder-glow m-0" v-if="!user">
                    <span class="placeholder col-12"></span>
                  </p>
                  <p class="text-muted mb-0" v-else><b>AFL{{ user?.pilot.callsign }}</b></p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3" v-if="user?.profile.vatsimid">
                  <p class="mb-0">Vatsim ID</p>
                </div>
                <div class="col-sm-3" :class="{'col-sm-9': !user?.profile.ivaoid }" v-if="user?.profile.vatsimid">
                  <p class="text-muted mb-0"><b>{{ user?.profile.vatsimid }}</b></p>
                </div>
                <div class="col-sm-3" v-if="user?.profile.ivaoid">
                  <p class="mb-0">IVAO ID</p>
                </div>
                <div class="col-sm-3" :class="{'col-sm-9': !user?.profile.vatsimid }" v-if="user?.profile.ivaoid">
                  <p class="text-muted mb-0"><b>{{ user?.profile.ivaoid }}</b></p>
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
import {secToHours, secFormat} from "@/utils/timeUtil";
import {tooltipUpdate} from "@/utils/templateUtil";

export default {
  name: "Profile",
  computed: {
    user() {
      return this.$store.getters.user
    },
    hours() {
      return secToHours(this.user?.pilot.hours)
    },
    full_hours() {
      return secFormat(this.user?.pilot.hours)
    }
  },
  mounted() {
    tooltipUpdate()
  },
  created() {
    if (!this.$store.getters.user){
      this.$store.dispatch('userObtain').then(()=>{
        this.user = this.$store.getters.user
        tooltipUpdate()
      })
    } else {
      this.user = this.$store.getters.user
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
</style>
