<template>
  <div class="modal fade modal-lg" id="bookModal" tabindex="-1" aria-labelledby="bookModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="">Flight Booking / AFL 7788 / SU 123</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body break-all ">
          <div class="row mt-2">
            <div class="col">
              <label for="DepAirport" class="form-label">Departure Airport
                <font-awesome-icon icon="plane-departure"/>
              </label>
              <input class="form-control text-center" maxlength="4"
                     id="DepAirport"
                     disabled>
            </div>
            <div class="col">
              <label for="ArrAirport" class="form-label">Arrival Airport
                <font-awesome-icon icon="plane-arrival"/>
              </label>
              <input class="form-control text-center" id="ArrAirport" maxlength="4"
                     :value="schedule?.arr_icao.icao_code" disabled>
            </div>
            <div class="col">
              <label for="AltAirport" class="form-label">Alternate Airport
                <font-awesome-icon icon="plane-circle-xmark"/>
              </label>
              <input class="form-control text-center" id="AltAirport"
                     :value="schedule?.alternate_icao.icao_code"
                     maxlength="4" v-uppercase>
            </div>
          </div>
          <div class="row mt-2">
            <div class="col">
              <label for="depTime" class="form-label">Departure Time
                <font-awesome-icon icon="clock"/>
              </label><br>
              <vue-timepicker id="depTime" input-class="form-control text-center"></vue-timepicker>
            </div>
            <div class="col">
              <label for="flightTime" class="form-label">Flight Time
                <font-awesome-icon icon="hourglass"/>
              </label><br>
              <vue-timepicker id="flightTime" input-class="form-control text-center" readonly="false"></vue-timepicker>
            </div>
            <div class="col">
              <label for="Payload" class="form-label">Payload
                <font-awesome-icon icon="weight-scale"/>
              </label>
              <input class="form-control text-center" id="Payload" value="">
            </div>
            <div class="col">
              <label for="pax" class="form-label">Passengers
                <font-awesome-icon icon="people-group"/>
              </label>
              <input class="form-control text-center" id="pax" value="">
            </div>
          </div>
          <div class="row mt-2">
            <div class="col">
              <label for="distance" class="form-label">Distance
                <font-awesome-icon icon="arrows-left-right-to-line"/>
              </label>
              <input class="form-control text-center" id="distance" value="">
            </div>
            <div class="col">
              <label for="fl" class="form-label">Flight Level
                <font-awesome-icon icon="arrows-up-down"/>
              </label>
              <input class="form-control text-center" id="fl" value="">
            </div>
            <div class="col">
              <label for="aiType" class="form-label di">Aircraft Type
                <font-awesome-icon icon="paper-plane"/>
              </label>
              <input class="form-control text-center" id="aiType" value="" disabled>
            </div>
            <div class="col">
              <label for="tailNum" class="form-label">Tail Number
                <font-awesome-icon icon="hashtag"/>
              </label>
              <input class="form-control text-center" id="tailNum" value="" disabled>
            </div>
          </div>
          <div class="mt-2">
            <label for="route" class="form-label">Route
              <font-awesome-icon icon="route"/>
            </label>
            <textarea class="form-control" id="route" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueTimepicker from 'vue3-timepicker'
import 'vue3-timepicker/dist/VueTimepicker.css'
import {library} from '@fortawesome/fontawesome-svg-core'
import {
  faClock, faPlaneDeparture, faPlaneArrival,
  faPlaneCircleXmark, faHourglass, faWeightScale, faPeopleGroup,
  faPaperPlane, faHashtag, faGaugeSimpleHigh, faXmarksLines, faRoute,
  faArrowsLeftRightToLine, faArrowsUpDown
} from '@fortawesome/free-solid-svg-icons'

library.add(faClock, faPlaneDeparture, faPlaneArrival,
    faPlaneCircleXmark, faHourglass, faWeightScale, faPeopleGroup, faPaperPlane, faHashtag,
    faGaugeSimpleHigh, faXmarksLines, faRoute, faArrowsLeftRightToLine, faArrowsUpDown
)
export default {
  name: "BookModal",
  data() {
    return {
      c: ''
    }
  },
  props: ['schedule', 'ai', 'charter'],
  components: {VueTimepicker}
}
</script>

<style lang="scss">
.vue__time-picker .dropdown ul li:not([disabled]).active {
  background: #02458d;

  &:hover {
    background: #02458d;
  }
}

.form-control[readonly] {
  background-color: white;
}
</style>
