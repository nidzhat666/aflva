<template>
  <div class="header">
    <div class="container d-flex flex-column flex-md-row align-items-center p-3 justify-content-center">
      <router-link :to="{name: 'Home'}" class="d-flex align-items-center text-dark text-decoration-none">
        <img class="logo" src="../assets/img/aflva_logo.png" alt="">
      </router-link>

      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto" v-bind:class="{'d-none': !$store.getters.isLoggedIn}">
        <div>
          <router-link :to="{name: 'Profile'}" class="me-3 py-2 text-dark text-decoration-none text-white">Профиль</router-link>
        </div>
        <div class="dropdown">
          <a class="me-3 py-2 text-dark text-decoration-none text-white dropdown-toggle" data-bs-toggle="dropdown"
             aria-expanded="false" href="#">Schedules</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
            </li>
          </ul>
        </div>
        <div class="dropdown">
          <a class="me-3 py-2 text-dark text-decoration-none text-white dropdown-toggle" data-bs-toggle="dropdown"
             aria-expanded="false" href="#">Fleet</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
              </a>
              <a class="dropdown-item d-flex justify-content-between" href="/schedules/?company=Aeroflot">
                Aeroflot
                <img style="margin-left: 15px; width: 22px" src="https://storage.yandexcloud.net/aflva/uploads/company/Aeroflot.png" alt="">
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
export default {
  name: "NavBar",
  data() {
    return {
      tabs: [
        {'text': 'Schedules'},
        {'text': 'Fleet'},
        {'text': 'Crew'},
        {'text': 'Online'},
        {'text': 'Route'},
        {'text': 'Admin'},
      ]
    }
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
