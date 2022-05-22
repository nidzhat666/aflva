<template>
  <div class="parallax">
    <div class="card shadow-lg bg-gradient booking">
      <div class="card-body">
        <h5>Fast Booking</h5>
        <hr>
        <form>
          <div class="row ">
            <div class="col">
              <input type="text" class="form-control" placeholder="From">
            </div>
            <div class="col ">
              <input type="text" class="form-control" placeholder="To">
            </div>
            <div class="col">
              <input type="submit" class="form-control btn btn-primary disabled" value="Search">
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="card shadow-lg bg-gradient info">
      <div class="card-body">
        <span>Welcome to <strong>«Sky Planet Aviation Group»</strong></span>
        <hr>
        <span>Some normal TEXT #TODO</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Engine"
}
</script>

<style lang="scss" scoped>
.parallax {
  background-image: url("../assets/img/engine.jpg");
  min-height: 70vh;
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;

  .card {
    position: absolute;
  }

  .info {
    width: 380px;
    right: 10%;
    top: 10%;
  }

  @media screen and (max-width: 1200px) {
    .info {
      left: 50%;
      top: 15%;
      margin-left: -190px;
    }
  }
  .booking {
    width: 380px;
    right: 10%;
    bottom: 10%;
  }

  @media screen and (max-width: 1200px) {
    .booking {
      left: 50%;
      bottom: 20%;
      margin-left: -190px;
    }
  }
}
</style>
