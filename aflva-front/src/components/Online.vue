<template>
  <div class="bg-light m-3">
    <div class="container shadow-lg table-responsive p-3">
      <h3>{{ title }}</h3>
      <table class="table">
        <thead>
        <tr>
          <th></th>
          <th scope="col">Pilot</th>
          <th scope="col">Flight</th>
          <th scope="col" colspan="2">From</th>
          <th scope="col" colspan="2">To</th>
          <th scope="col">Aircraft Type</th>
          <th scope="col">Status</th>
          <th scope="col">Altitude</th>
          <th scope="col">Speed</th>
          <th scope="col">Distance</th>
        </tr>
        </thead>
        <tbody>
        <tr>
          <td><img style="width: 22px;" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
          </td>
          <td title="">Nikolai Panin</td>
          <td title="">AFL1405</td>
          <td style="margin: auto;">
            <img style="width: 18px;" src="/static/countries/ru.png" alt="">
          </td>
          <td data-bs-toggle="tooltip" data-bs-placement="top" title="Koltsovo Airport">UUEE</td>
          <td style="margin: auto;">
            <img style="width: 18px;" src="/static/countries/ru.png" alt="">
          </td>
          <td data-bs-toggle="tooltip" data-bs-placement="top" title="Koltsovo Airport">UUEE</td>
          <td>Boeing 737-8LJ(WL)</td>
          <td>Cruise</td>
          <td data-bs-toggle="tooltip" data-bs-placement="top" title="1123 m">34173 ft.</td>
          <td>394</td>
          <td>504 NM</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>

</template>

<script>
import {Tooltip} from 'bootstrap/dist/js/bootstrap.esm.min.js'

export default {
  name: "Online",
  props: {
    title: String,
    items: Array
  },
  mounted() {
    Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        .forEach(tooltipNode => {
          new Tooltip(tooltipNode)
          console.log(tooltipNode)
        })
  },
}
</script>

<style lang="scss" scoped>
</style>
