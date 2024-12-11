<!-- src/components/SubmitLink.vue -->
<template>
  <div class="container mt-5">

    <!-- Кнопка открытия модального окна добавления -->
    <button class="btn btn-primary mb-3" @click="openAddModal">
      Добавить сайт
    </button>

    <!-- Модальное окно добавления сайта -->
    <div
        class="modal fade"
        tabindex="-1"
        ref="addModal"
        aria-labelledby="addModalLabel"
        aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addModalLabel">Добавить сайт</h5>
            <button type="button" class="btn-close" @click="closeAddModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="urlInput" class="form-label">URL сайта</label>
                <input
                    type="text"
                    class="form-control"
                    id="urlInput"
                    v-model="link"
                    placeholder="Введите URL"
                    required
                />
              </div>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Отправка...' : 'Отправить' }}
              </button>
            </form>

            <!-- Сообщения об успехе и ошибке внутри модала -->
            <div v-if="successMessage" class="alert alert-success mt-3">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert alert-danger mt-3">
              {{ errorMessage }}
            </div>
          </div>
        </div>
      </div>
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
import api from "@/services/api"; // Используйте алиас @, если настроен
import { Modal } from 'bootstrap';

export default {
  name: "SubmitLink",
  data() {
    return {
      link: "",
      loading: false,
      successMessage: "",
      errorMessage: "",
      toast: {
        show: false,
        message: "",
        type: "", // 'success' или 'error'
        typeClass: "",
      },
      addModalInstance: null, // Экземпляр модального окна
    };
  },
  mounted() {
    // Инициализируйте модальное окно Bootstrap
    this.addModalInstance = new Modal(this.$refs.addModal, {
      backdrop: true,
      keyboard: true,
      focus: true,
    });

    // Обработчик скрытия модального окна
    this.$refs.addModal.addEventListener('hidden.bs.modal', () => {
      // Сбросить поля формы и сообщения
      this.link = "";
      this.successMessage = "";
      this.errorMessage = "";
    });
  },
  methods: {
    // Открыть модальное окно добавления
    openAddModal() {
      console.log("Открытие модального окна добавления");
      this.addModalInstance.show();
      this.link = "";
      this.successMessage = "";
      this.errorMessage = "";
    },

    // Закрыть модальное окно добавления
    closeAddModal() {
      console.log("Закрытие модального окна добавления");
      this.addModalInstance.hide();
      this.link = "";
      this.successMessage = "";
      this.errorMessage = "";
    },

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

    // Обработчик отправки формы
    async handleSubmit() {
      console.log("handleSubmit вызван");

      if (!this.link) {
        console.log("URL не введён");
        this.showToast("Пожалуйста, введите URL.", "error");
        return;
      }

      if (!this.isValidUrl(this.link)) {
        console.log("Введён некорректный URL:", this.link);
        this.showToast("Пожалуйста, введите корректный URL.", "error");
        return;
      }

      this.loading = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        console.log("Отправка URL как параметра запроса:", this.link);

        const response = await api.post(
            "/site/",
            {}, // Отправляем пустое тело
            {
              params: {
                url: this.link, // Отправляем 'url' как параметр запроса
              },
              headers: {
                "Content-Type": "application/json",
              },
            }
        );

        console.log("Ответ сервера:", response);

        if (response.status === 200) {
          this.showToast("Ссылка успешно отправлена!", "success");
          this.closeAddModal();
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        } else {
          this.showToast("Ошибка при отправке ссылки.", "error");
        }
      } catch (error) {
        console.error("Ошибка отправки ссылки:", error);
        if (error.response && error.response.data && error.response.data.detail) {
          this.showToast(error.response.data.detail, "error");
        } else {
          this.showToast("Произошла ошибка при отправке ссылки.", "error");
        }
      } finally {
        this.loading = false;
      }
    },

    // Дополнительная функция для валидации URL (опционально)
    isValidUrl(url) {
      const pattern = new RegExp(
          "^(https?:\\/\\/)"+ // протокол (обязательно)
          "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // доменное имя
          "((\\d{1,3}\\.){3}\\d{1,3}))" + // или IP (v4) адрес
          "(\\:\\d+)?" + // порт
          "(\\/[-a-z\\d%_.~+]*)*" + // путь
          "(\\?[;&a-z\\d%_.~+=-]*)?" + // строка запроса
          "(\\#[-a-z\\d_]*)?$",
          "i"
      );
      return !!pattern.test(url);
    },
  },
};
</script>

<style scoped>
/* Стили для тостов */
.toast-container {
  z-index: 1100;
}

.toast {
  min-width: 250px;
}
</style>
