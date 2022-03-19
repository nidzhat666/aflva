<template>
  <div class="bg-light m-3">
    <div class="container shadow-lg table-responsive">
      <h3>Booked</h3>
      <table class="table">
        <thead>
        <tr>
          <th></th>
          <th scope="col">Pilot</th>
          <th scope="col">Flight</th>
          <th scope="col" colspan="2">From</th>
          <th scope="col" colspan="2">To</th>
          <th scope="col">Aircraft Type</th>
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
  mounted() {
    Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        .forEach(tooltipNode => {
          new Tooltip(tooltipNode)
        })
  },
}
</script>

<style lang="scss" scoped>
</style>
