<template>
  <div class="container mt-3">
    <div class="row justify-content-center">
      <div class="col m-auto mb-0 lg-block">
        <img class="flight-attendant" height="290px" src="https://github.com/nidzhat666/images/blob/main/flight-attendant.png?raw=true" alt="">
      </div>
      <div class="col p-3 col-auto">
        <h1>Contact Us</h1>
        <span>Напишите сообщение и мы вам ответим на вашу почту</span>
        <div class="row">
          <span class="col">Имя: <strong>Nidzhat Agalarov</strong></span>
          <span class="col">Почта: <strong>nagalarov@mail.ru</strong></span>
        </div>
        <div class="form-floating">
          <textarea class="form-control" placeholder="Leave a comment here" id="contact-us" style="height: 100px"></textarea>
          <label for="contact-us">Your Message</label>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Send</button>
      </div>
      <div class="col m-auto lg-block">
        <img height="290px" src="https://github.com/nidzhat666/images/blob/main/routes.png?raw=true" alt="">
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "ContactUsSection"
}
</script>

<style lang="scss" scoped>
@media screen and (max-width: 1200px){
  .lg-block{
    display: none;
  }
}

</style>
