<template>
  <div class="stats mt-3 text-white p-2">
    <div class="container row m-auto">
      <div class="col">
        <p>Пилотов</p>
        <h3><b>74</b></h3>
      </div>
      <div class="col">
        <p>Полетов</p>
        <h3><b>18093</b></h3>
      </div>
      <div class="col">
        <p>Самолетов</p>
        <h3><b>520</b></h3>
      </div>
      <div class="col">
        <p>Часов</p>
        <h3><b>60073</b></h3>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: "HomeStatsSection"
}
</script>

<style lang="scss" scoped>

.stats {
  background-color: #022f68;

  h3 {
    margin: 0;
  }

  p {
    margin: 0;
  }
}
</style>
