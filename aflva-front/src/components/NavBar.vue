<template>
  <div class="header">
    <div class="container d-flex flex-column flex-md-row align-items-center p-3 justify-content-center">
      <router-link :to="{name: 'Home'}" class="d-flex align-items-center text-dark text-decoration-none">
        <img class="logo" src="../assets/img/aflva_logo.png" alt="">
      </router-link>

      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto" v-bind:class="{'d-none': !$store.getters.isLoggedIn}">
        <div>
          <router-link :to="{name: 'Profile'}" class="me-3 py-2 text-dark text-decoration-none text-white">Profile</router-link>
        </div>
        <div class="dropdown">
          <a class="me-3 py-2 text-dark text-decoration-none text-white dropdown-toggle" data-bs-toggle="dropdown"
             aria-expanded="false" href="#">Schedules</a>
          <ul class="dropdown-menu shadow-lg" aria-labelledby="dropdownMenuButton1">
            <li>
              <router-link class="dropdown-item d-flex justify-content-between"
                           v-for="company in companies"  v-bind:key="company" :to="{name: 'Schedule', params:{company: company.name}}">
                {{company.name}}
                <img style=" width: 22px" :src="company.logo" alt="">
              </router-link>
            </li>
          </ul>
        </div>
        <div class="dropdown">
          <a class="me-3 py-2 text-dark text-decoration-none text-white dropdown-toggle" data-bs-toggle="dropdown"
             aria-expanded="false" href="#">Fleet</a>
          <ul class="dropdown-menu shadow-lg" aria-labelledby="dropdownMenuButton1">
            <li>
              <a class="dropdown-item d-flex justify-content-between"
                 v-for="company in companies"  v-bind:key="company" href="#">
                {{company.name}}
                <img style=" width: 22px" :src="company.logo" alt="">
              </a>
            </li>
            <hr>
            <li>
              <a class="dropdown-item d-flex justify-content-between"
                 v-for="company in retro"  v-bind:key="company" href="#">
                {{company.name}} Retro
                <img style="width: 22px" :src="company.logo" alt="">
              </a>
            </li>
          </ul>
        </div>
        <div>
          <a class="me-3 py-2 text-dark text-decoration-none text-white" href="#">Crew</a>
        </div>
        <div>
          <a class="me-3 py-2 text-dark text-decoration-none text-white" href="#">Routes</a>
        </div>

      </nav>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NavBar",
  data() {
    return {
      companies: [],
    }
  },
  computed:{
    retro(){
      return this.companies.filter(company=>company.is_retro)
    }
  },
  mounted() {
    axios.get('company/').then(response=>{
      this.companies = response.data.results
    })
  }
}
</script>

<style lang="scss" scoped>
.header {
  background-color: #02458d;

  .logo {
    max-width: 210px;
  }
}

</style>
