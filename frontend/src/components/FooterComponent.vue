<template>
  <!-- mt-top to move the header to the bottom of the viewport -->
  <footer class="footer-two section py-4 bg-img mt-auto">
    <div class="container">
      <div class="row items-gap-two justify-content-center align-items-center">
        <div class="col-auto logo-container">
          <router-link to="/" @click="scrollToTop" class="logo">
            <img src="../assets/logo.png" alt="Logo" style="max-width: 55px;" />
          </router-link>
        </div>
        <div class="col-auto footer">
          <p class="copyright ">
            &copy; <span id="copyYear">{{ new Date().getFullYear() }}</span>&nbsp;
            <router-link to="/"> EchoLink</router-link>. All Rights Reserved.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterComponent",
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  }
};
</script>

<style scoped>
.container {
  width: 100vw;
}

.logo-container {
  width: 30%;
  display: flex;
  justify-content: flex-start;
}
.footer {
  width: 70%;
  display: flex;
  justify-content: flex-end;
}

/* Hide the logo on small screens */
@media screen and (max-width: 768px) {
  .logo-container {
    display: none;

  }

  .footer{
    width: 100%;
    display: flex;
    justify-content: center;
  }


}

</style>
