<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <!-- Название сайта -->
      <router-link class="navbar-brand" to="/">Decision stumps</router-link>

      <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Ссылки навбара -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link
                class="nav-link"
                :class="{ active: isActive('/') }"
                to="/"
            >
              Главная
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
                class="nav-link"
                :class="{ active: isActive('/file') }"
                to="/file"
            >
              Загрузка файла
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRoute } from "vue-router";

export default {
  name: "Navbar",
  setup() {
    const route = useRoute();

    const isActive = (path) => route.path === path;

    return {
      isActive,
    };
  },
};
</script>

<style scoped>
.navbar-nav .nav-link.active {
  font-weight: bold;
  color: #007bff;
}
</style>
