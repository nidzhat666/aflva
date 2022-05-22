<template>
  <section @mousemove="move">
    <form class="form-signin">
      <!--    <img class="mb-4" src="https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">-->
      <h1 class="h3 mb-3 font-weight-normal">Sign In</h1>
      <div class="mt-3">
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required="" autofocus="">
      </div>
      <div class="mt-3">
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required="">
      </div>
      <div class="mt-3">
        <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
      </div>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>
  </section>

</template>

<script>
export default {
  name: "Login",
  mounted() {
    const movementStrength = 25;
    const height = movementStrength / window.innerHeight;
    const width = movementStrength / window.innerWidth;
    const main = document.querySelector("body");
    const el = document.querySelector("section");
    main.addEventListener("mousemove", (e) => {
      let pageX = e.pageX - (window.innerWidth / 2);
      let pageY = e.pageY - (window.innerHeight / 2);
      let newvalueX = width * pageX * -1 - 25;
      let newvalueY = height * pageY * -1 - 50;
      el.style.backgroundPositionX = newvalueX + "px";
      el.style.backgroundPositionY = newvalueY + "px";
    });
  }
}
</script>

<style lang="scss" scoped>
section{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url("../assets/img/login_background.jpg") 0 0 ;
  background-size: calc(100% + 50px);
  width:100%;
  z-index:0;
  height:100%;
}

form {
  box-shadow: 0 0 10px rgb(0 0 0 / 50%);
  border-radius: 5%;
  background-color: white;
}

.form-signin {
  width: 100%;
  max-width: 450px;
  padding: 30px;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
</style>
