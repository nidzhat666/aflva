<template>
  <div class="container">
    <ul class="nav nav-pills mb-3 justify-content-center mt-3" id="pills-tab" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active text-uppercase" id="pills-projects-tab" data-bs-toggle="pill"
                data-bs-target="#pills-projects"
                type="button" role="tab" aria-controls="pills-projects" aria-selected="true">Наши компании
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link  text-uppercase" id="pills-news-tab" data-bs-toggle="pill" data-bs-target="#pills-news"
                type="button" role="tab" aria-controls="pills-news" aria-selected="false">Новости
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link text-uppercase" id="pills-about-tab" data-bs-toggle="pill" data-bs-target="#pills-about"
                type="button" role="tab" aria-controls="pills-about" aria-selected="false">О нас
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link text-uppercase" id="pills-ustav-tab" data-bs-toggle="pill" data-bs-target="#pills-ustav"
                type="button" role="tab" aria-controls="pills-ustav" aria-selected="false">Устав
        </button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <div class="tab-pane fade show active" id="pills-projects" role="tabpanel" aria-labelledby="pills-projects-tab">
        <img src="../assets/img/aeroflot_logo.png" alt="">
        <img src="../assets/img/azur_logo.svg" alt="">
        <img src="../assets/img/pobeda_logo.png" alt="">
        <img src="../assets/img/s7_logo.png" alt="">
        <img src="../assets/img/utair_logo.png" alt="">
      </div>
      <div class="tab-pane fade" id="pills-news" role="tabpanel" aria-labelledby="pills-news-tab"><h4>No news</h4></div>
      <div class="tab-pane fade" id="pills-about" role="tabpanel" aria-labelledby="pills-about-tab"></div>
      <div class="tab-pane fade" id="pills-ustav" role="tabpanel" aria-labelledby="pills-ustav-tab"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeTabsSection",
  data() {
    return {
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  li {
    margin-left: 10px;
    margin-right: 10px;
  }
  #pills-projects{
    img{
      width: 150px;
      margin-right: 10px;
      margin-left: 10px;
    }
  }
}
</style>
