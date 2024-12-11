<!-- src/views/DetailsPage.vue -->
<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Детали для: {{ tag }}</h2>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p>Загрузка данных...</p>
    </div>

    <!-- Таблица с данными -->
    <div v-else class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
        <tr>
          <th>Itemprop</th>
          <th>Соответствие</th>
          <th>Текст</th>
          <th>Статус</th>
          <th>Тег</th>
          <th>Номер страницы</th>
          <th>Ответ нейросети</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in items" :key="index">
          <td>{{ item.itemprop }}</td>
          <td>{{ item.valid }}</td>
          <td>{{ item.text }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.check }}</td>
          <td>{{ item.page }}</td>
          <td>{{ item.valid_text }}</td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Тост уведомления -->
    <div
        class="toast-container position-fixed top-0 end-0 p-3"
        style="z-index: 1100"
    >
      <div
          v-if="toast.show"
          :class="['toast align-items-center text-white border-0', toast.typeClass]"
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          @hidden.bs.toast="toast.show = false"
      >
        <div class="d-flex">
          <div class="toast-body">
            {{ toast.message }}
          </div>
          <button
              type="button"
              class="btn-close btn-close-white me-2 m-auto"
              data-bs-dismiss="toast"
              aria-label="Close"
              @click="toast.show = false"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api"; // Убедитесь, что путь верный

export default {
  name: "DetailsPage",
  props: {
    tag: { // Изменено с cardKey на tag
      type: String,
      required: true,
    },
  },
  data() {
    return {
      items: [],
      loading: false,
      toast: {
        show: false,
        message: "",
        type: "", // 'success' или 'error'
        typeClass: "",
      },
      navigateButtonClass: "btn-primary",
      isNavigateDisabled: false,
    };
  },
  methods: {
    // Функция отображения тостов
    showToast(message, type) {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;

      // Определение класса для цвета тоста
      if (type === "success") {
        this.toast.typeClass = "bg-success";
      } else if (type === "error") {
        this.toast.typeClass = "bg-danger";
      }

      // Автоматически скрыть тост через 3 секунды
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },

    // Функция навигации
    navigate(url) {
      if (url.startsWith("http://") || url.startsWith("https://")) {
        window.open(url, "_blank"); // Открываем во вкладке
      } else {
        this.$router.push(url); // Внутренняя навигация
      }
    },

    // Функция для получения данных
    async fetchData() {
      this.loading = true;
      try {
        const response = await api.get("/doc/", {
          params: {
            key: this.tag, // Используем пропс 'tag'
          },
        });

        console.log("Данные с сервера:", response.data);

        if (
            response.status === 200 &&
            response.data[this.tag] &&
            response.data[this.tag].data
        ) {
          this.items = response.data[this.tag].data;
          this.showToast("Данные успешно загружены!", "success");
        } else {
          this.showToast("Нет данных для отображения.", "error");
        }
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
        this.showToast("Ошибка при загрузке данных.", "error");
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    console.log('Received tag:', this.tag); // Для отладки
    this.fetchData();
  },
};
</script>

<style>



</style>