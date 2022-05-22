<template>
  <div class="booking">
    <div>
      <h4 v-if="flight">✈️Flight</h4>
      <h2 v-else>Booking</h2>
    </div>
    <div class="book m-3" v-if="Object.keys(book).length">
      <div class="row">
        <div class="col">
          <div>Callsign</div>
          <span>{{ book.callsign }}</span>
        </div>
        <div class="col">
          <div>Aircraft</div>
          <span>{{ book.aircraft.aircraft_type.aircraft_icao.aircraft_icao }}</span>
        </div>
        <div class="col">
          <div>Cruise</div>
          <span v-if="book.flight_level < 999">FL{{ book.flight_level }}</span>
          <span v-else>{{ book.flight_level }} feet</span>
        </div>
        <div class="col">
          <div>Flight time</div>
          <span>{{ book.flight_time }}</span>
        </div>
        <div class="col">
          <div>Pax</div>
          <span>{{ book.pax }}</span>
        </div>
        <div class="col">
          <div>Cargo</div>
          <span>{{ book.cargo }} kgs</span>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col">
          <div>Departure</div>
          <div class="justify-content-center" style="display: flex; flex-direction: row">
            <span>{{ book.dep_airport.icao_code }}</span>
            <span style="margin-left: 3px;">{{ book.dep_airport.name }}</span>
          </div>
        </div>
        <div class="col">
          <div>Arrival</div>
          <div class="justify-content-center" style="display: flex; flex-direction: row">
            <span>{{ book.arr_airport.icao_code }}</span>
            <span style="margin-left: 3px;">{{ book.arr_airport.name }}</span>
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div>
          <div>Route</div>
          <span style="max-height: 120px; overflow-y: auto">{{ book.route }}</span>
        </div>
      </div>
      <Flight v-if="flight"/>
      <div class="m-3" v-else>
        <!--      <button v-on:click="$router.push({'name':'Flight'})" class="btn btn-dark">Fly</button>-->
        <button class="btn btn-dark" @click="flight = true">Fly</button>
      </div>

    </div>
    <div class="no-books" v-else>
      <h5>No Bookings found.</h5>
    </div>
  </div>
  <ErrorModal :message="error.message" v-on:message="setErrorMessage"/>
</template>

<script>
// import fsuipc from 'fsuipc' WORKS ONLY With Windows !!!
import Flight from "@/views/Flight";
import ErrorModal from "../components/ErrorModal";

export default {
  name: "Book",
  components: {
    ErrorModal,
    Flight
  },
  data() {
    return {
      book: {},
      error: {
        message: '',
      },
      flight: false
    }
  },
  created() {
    this.reqBooks()
    setInterval(this.reqBooks, 3000)
  },
  beforeUnmount() {
  },
  watch: {
        book: function (current){
          if (!current.id) this.flight = null
        }
  },
  methods: {
    setErrorMessage(message) {
      this.error.message = message
    },
    reqBooks() {
      this.$store.dispatch('books').then(
          books => {
            if (books.length) {
              this.book = books[0]
            } else {
              this.book = {}
            }
          }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
.book {
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
.no-books{
  margin-top: 80px;
}
</style>
