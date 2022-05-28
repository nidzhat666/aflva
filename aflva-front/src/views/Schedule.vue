<template>
  <section style="background-color: #eee;">
    <div class="container py-3">
      <div class="row">
        <div class="col">
          <nav aria-label="breadcrumb" class="bg-light rounded-3 p-3">
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item">
                <router-link :to="{name: 'Home'}">
                  Home
                </router-link>
              </li>
              <li class="breadcrumb-item active" aria-current="page">{{ $route.params.company }} Schedule</li>
            </ol>
          </nav>
        </div>
      </div>
      <div class="row mt-3">
        <div class="input-group w-auto col-sm-1">
          <span class="input-group-text" id="search-area"><b-icon-search></b-icon-search></span>
          <input type="text" class="form-control" placeholder="Search" aria-label="Search"
                 aria-describedby="search-area" v-model="search_query" @keyup="searchTimeOut">
        </div>
        <div class="col-auto">
          <button class="btn btn-sm btn-warning h-100" @click="ordering=''; search_query=''; getSchedule()"
                  :class="{disabled: !(ordering.length || search_query.length)}">
            Reset Search & Filters
            <b-icon-arrow-counterclockwise></b-icon-arrow-counterclockwise>
          </button>
        </div>
      </div>
      <div class="table-responsive mt-3">
        <table class="table bg-white rounded-3">
          <thead>
          <tr>
            <th scope="col">Company</th>
            <th scope="col" class="border-start" @click="orderBy('flightnum')">
              #
              <b-icon-caret-up-fill v-if="ordering==='flightnum'"></b-icon-caret-up-fill>
              <b-icon-caret-down-fill v-else-if="ordering==='-flightnum'"></b-icon-caret-down-fill>
            </th>
            <th scope="col" colspan="3" class="border-start" @click="orderBy('dep_icao__icao_code')">
              Departure Airport
              <b-icon-caret-down-fill v-if="ordering==='dep_icao__icao_code'"></b-icon-caret-down-fill>
              <b-icon-caret-up-fill v-else-if="ordering==='-dep_icao__icao_code'"></b-icon-caret-up-fill>
            </th>
            <th scope="col" colspan="3" class="border-start" @click="orderBy('arr_icao__icao_code')">
              Arrival Airport
              <b-icon-caret-down-fill v-if="ordering==='arr_icao__icao_code'"></b-icon-caret-down-fill>
              <b-icon-caret-up-fill v-else-if="ordering==='-arr_icao__icao_code'"></b-icon-caret-up-fill>
            </th>
            <th scope="col" class="border-start" @click="orderBy('deptime')">
              Departure Time
              <b-icon-caret-up-fill v-if="ordering==='deptime'"></b-icon-caret-up-fill>
              <b-icon-caret-down-fill v-else-if="ordering==='-deptime'"></b-icon-caret-down-fill>
            </th>
            <th class="border-start">
              Flight Time
            </th>
            <th scope="col" class="border-start pe-1" @click="orderBy('distance')">
              Distance
              <b-icon-caret-up-fill v-if="ordering==='distance'"></b-icon-caret-up-fill>
              <b-icon-caret-down-fill v-else-if="ordering==='-distance'"></b-icon-caret-down-fill>
            </th>
            <th class="border-start">
              Status
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-if="schedules.length" v-for="schedule in schedules" :key="schedule" class="align-middle">
            <td>
              <img style="width: 22px" :src="schedule.company.logo">
            </td>
            <th class="border-start" v-tooltip:top="schedule.callsign">
              {{ schedule.flightnum }}
            </th>
            <td class="border-start ">
              <country-flag :country='schedule.dep_icao.country' v-tooltip:top="schedule.dep_icao.country"
                            :rounded="true"/>
            </td>
            <td class="">{{ schedule.dep_icao.icao_code }}</td>
            <td>
              {{ schedule.dep_icao.name }}
            </td>
            <td class="border-start">
              <country-flag :country='schedule.arr_icao.country' v-tooltip:top="schedule.arr_icao.country"
                            :rounded="true"/>
            </td>
            <td>{{ schedule.arr_icao.icao_code }}</td>
            <td>
              {{ schedule.arr_icao.name }}
            </td>
            <td class="border-start ">{{ schedule.deptime }}z</td>
            <td class="border-start" v-tooltip:top="`Arrival: ${schedule.arrtime }z`">{{ schedule.flight_time }}</td>
            <td class="border-start" v-tooltip:top="`${nmConvert(schedule.distance)}km`">{{ schedule.distance }} NM</td>
            <td class="border-start">
              <button class="btn btn-sm btn-success">Свободно</button>
            </td>
          </tr>
          <tr v-else>
            <td colspan="12">OOPS No Flights Found</td>
          </tr>
          </tbody>
        </table>
        <paginate
            :page-count="total_pages"
            :page-range="3"
            :margin-pages="2"
            :click-handler="setPage"
            :prev-text="'Prev'"
            :next-text="'Next'"
            :container-class="'pagination'"
            :page-class="'page-item'"
        >
        </paginate>
      </div>
    </div>
  </section>

</template>

<script>
import {BIconSearch, BIconCaretDownFill, BIconCaretUpFill, BIconArrowCounterclockwise} from 'bootstrap-icons-vue';
import Paginate from "vuejs-paginate-next";
import axios from "axios";

export default {
  name: "Schedules",
  data() {
    return {
      schedules: [],
      page: 1,
      timer: null,
      search_query: '',
      ordering: '',
      total_pages: 0
    }
  },
  components: {
    BIconSearch,
    BIconCaretDownFill,
    BIconCaretUpFill,
    BIconArrowCounterclockwise,
    Paginate
  },
  mounted() {
    this.getSchedule()
  },
  methods: {
    getSchedule() {
      axios.get('schedule/', {
        params: {
          page: this.page,
          company__name: this.$route.params.company,
          search: this.search_query,
          ordering: this.ordering
        }
      })
          .then(response => {
            this.schedules = response.data.results
            this.total_pages = response.data.total_pages
          })
    },
    searchTimeOut() {
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = null;
      }
      this.timer = setTimeout(() => {
        this.page = 1
        this.getSchedule()
      }, 800);
    },
    setPage(pageNum) {
      this.page = pageNum
      this.getSchedule()
    },
    nmConvert(nm) {
      return Math.floor(nm * 1.852)
    },
    orderBy(field) {
      this.ordering = this.ordering === field ? '-' + field : field
      this.getSchedule()
    }
  }
}
</script>

<style lang="scss">
.page-item {
  cursor: pointer;
}
</style>
<style lang="scss" scoped>
thead tr th[scope=col] {
  cursor: pointer;
}
</style>
