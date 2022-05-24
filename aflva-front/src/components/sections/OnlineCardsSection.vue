<template>
  <div class="container mt-3">
    <div class="row">
      <div class="card col shadow-lg">
        <div class="card-body">
          <h5 class="card-title" v-if="online.length">Online</h5>
          <table class="table" v-if="online.length">
            <thead>
            <tr>
              <td>Airline</td>
              <td>Status</td>
              <td>Name</td>
              <td>From</td>
              <td>To</td>
            </tr>
            </thead>
            <tbody>
            <tr v-for="book in online" v-bind:key="book">
              <td>
                <span class="label label-default" v-tooltip:top="book.company.name">
                  <img style="width: 22px;" :src="book.company.logo"
                       alt="">
                </span>
              </td>
              <th>
                <span class="label label-default" v-tooltip:top="'Cruise'">
                  <img style="width: 22px;" src="@/assets/statuses/cruise.png"
                       alt="">
                </span>
              </th>
              <th>
                <span class="label label-default" v-tooltip:top="get_book_tooltip_pilot(book)">
                  {{ book.pilot.profile.get_full_name }}
                </span>
              </th>
              <td>
                <span class="label label-default" v-tooltip:top="book.dep_airport.name">
                  {{ book.dep_airport.icao_code }}
                </span>
              </td>
              <td>
                <span class="label label-default" v-tooltip:top="book.arr_airport.name">
                  {{ book.arr_airport.icao_code }}
                </span>
              </td>
            </tr>
            </tbody>
          </table>
          <h2 class="m-0" v-else>No Active Flights 💤</h2>
        </div>
      </div>
      <div class="card col shadow-lg">
        <div class="card-body">
          <h5 class="card-title" v-if="booked.length">Booked flights</h5>
          <table class="table" v-if="booked.length">
            <thead>
            <tr>
              <td>Airline</td>
              <td>Name</td>
              <td>From</td>
              <td>To</td>
            </tr>
            </thead>
            <tbody>
            <tr v-for="book in bookings" v-bind:key="book">
              <td>
                <span class="label label-default" v-tooltip:top="book.company.name">
                  <img style="width: 22px;" :src="book.company.logo"
                       alt="">
                </span>

              </td>
              <th>
                <span class="label label-default" v-tooltip:top="get_book_tooltip_pilot(book)">
                  {{ book.pilot.profile.get_full_name }}
                </span>
              </th>
              <td>
                <span class="label label-default" v-tooltip:top="book.dep_airport.name">
                  {{ book.dep_airport.icao_code }}
                </span>
              </td>
              <td>
                <span class="label label-default" v-tooltip:top="book.arr_airport.name">
                  {{ book.arr_airport.icao_code }}
                </span>
              </td>
            </tr>
            </tbody>
          </table>
          <h2 class="m-0" v-else>No Booked Flights 💤</h2>
        </div>
      </div>
      <div class="card col shadow-lg">
        <div class="card-body">
          <h5 class="card-title">The Best in {{month}}</h5>
          <table class="table">
            <thead>
            <tr>
              <td>Name</td>
              <td>Flights</td>
              <td>Score</td>
            </tr>
            </thead>
            <tbody>
            <tr v-for="pilot in pilots_top" v-bind:key="pilot">
              <td>{{ pilot.full_name }}</td>
              <td>{{ pilot.flight_count }}</td>
              <td>{{ pilot.average_rating }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "OnlineCardsSection",
  data() {
    return {
      bookings: [],
      pilots_top:[],
      month: null
    }
  },
  computed: {
    booked() {
      return this.bookings.filter((obj) => {
        if (obj.status === 'booked') return obj
      })
    },
    online() {
      return this.bookings.filter((obj) => {
        if (obj.status !== 'booked') return obj
      })
    },
  },
  mounted() {
    this.getBookings()
    this.get_top_pilots()
    this.interval = setInterval(this.getBookings, 10000)
  },
  unmounted() {
    clearInterval(this.interval)
  },
  methods: {
    getBookings() {
      axios.get('books/')
          .then(response => {
            this.tooltipsRemove()
            this.bookings = response.data
          })
    },
    get_top_pilots(){
      axios.get('stats/pilots_top/').then(response=>{
        this.pilots_top = response.data.top
        this.month = new Date(2022, response.data.month, 0).toLocaleString('default', { month: 'long' });
      })
    },
    get_book_tooltip_pilot(book) {
      return `${book.callsign} - ${book.aircraft.aircraft_type.aircraft_icao.aircraft_icao} (${book.aircraft.aircraft_registration})`
    },
    tooltipsRemove(){
      document.querySelectorAll('.tooltip').forEach(function (a) {
        a.remove()
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.col {
  margin: 1rem;
  height: 100%;
  min-width: 350px;
}
@media (min-width: 1200px) {
  .container{
    max-width: 1500px;
  }
}
</style>
