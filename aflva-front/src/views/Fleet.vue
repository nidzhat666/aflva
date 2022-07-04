<template>
  <section>
    <div class="container mt-3">
      <div class="row">
        <div class="col">
          <nav aria-label="breadcrumb" class="bg-light rounded-3 p-3">
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item">
                <router-link :to="{name: 'Home'}">
                  Home
                </router-link>
              </li>
              <li class="breadcrumb-item active" aria-current="page">{{ $route.params.company }} <span
                  v-if="$route.query.retro">Retro</span> Fleet
              </li>
            </ol>
          </nav>
        </div>
      </div>
      <div class="row mt-3 justify-content-center">
        <div class="col-lg-4 my-3" v-for="(fleet, icao) in fleets" :key="icao">
          <div class="card shadow-lg">
            <img class="card-img-top" :src="fleet[0].icao_image">
            <div class="card-header text-white">
              <b>{{ icao }}</b>
            </div>
            <div class="card-body p-0">
              <table class="table">
                <thead>
                <tr>
                  <th scope="col">REG</th>
                  <th scope="col">Aircraft Type</th>
                  <th scope="col">Now</th>
                  <th scope="col">Status</th>
                </tr>
                </thead>
                <tbody class="align-middle">
                <tr v-for="ai in fleet" :key="ai">
                  <th scope="row">{{ ai.aircraft_registration }}</th>
                  <td>{{ ai.aircraft_type.aircraft_name }}</td>
                  <td v-tooltip:top="ai.now.name">{{ ai.now.icao_code }}</td>
                  <td v-tooltip:top="getStatus(ai)">
                    <button class="btn btn-sm" :class="[ai.avail && !ai.booked ? 'btn-success': 'btn-danger disabled']"
                            @click="scheduleRedirect(ai)">
                      <font-awesome-icon :icon="ai.avail && !ai.booked ? 'plane': 'plane-slash'"/>
                    </button>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>

<script>
import tooltipsRemove from "@/utils/tooltipsRemove";
import axios from "axios";

export default {
  name: "Fleet",
  data() {
    return {
      fleets: {}
    }
  },
  created() {
    this.getFleet()
  },
  methods: {
    getFleet() {
      axios.get('fleet/', {
        params: {
          company__name: this.$route.params.company,
          status: this.$route.query.retro ? 'Retro' : 'Active',
        }
      }).then(response => {
        this.filterFleet(response.data)
      })
    },
    filterFleet(data) {
      data.forEach(el => {
        let icao = el.icao
        if (this.fleets[icao]) {
          this.fleets[icao].push(el)
        } else {
          this.fleets[icao] = [el]
        }
      })
    },
    getStatus(ai) {
      if (ai?.booked) {
        return 'Already Booked'
      } else if (!ai.avail) {
        return 'Unavailable'
      } else {
        return 'Book'
      }
    },
    scheduleRedirect(ai) {
      if (ai.avail && !ai.booked) this.$router.replace({
        name: 'Schedule',
        query: {'a': ai.id},
        params: {company: this.$route.params.company}
      })
      tooltipsRemove()
    }
  }
}
</script>

<style lang="scss" scoped>
.card-header {
  background-color: #02458d;
}
</style>
