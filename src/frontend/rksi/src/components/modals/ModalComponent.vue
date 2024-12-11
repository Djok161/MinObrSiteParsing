<template>
  <div>
    <!-- Модальное окно -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{ title }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="linkInput" class="form-label">Введите ссылку</label>
                <input
                    type="url"
                    class="form-control"
                    id="linkInput"
                    v-model="link"
                    required
                    placeholder="https://example.com"
                />
              </div>
              <button type="submit" class="btn btn-primary">Отправить</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Тост -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1055;">
      <div
          class="toast"
          :class="toast.type === 'success' ? 'text-bg-success' : 'text-bg-danger'"
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          v-if="toast.visible"
      >
        <div class="toast-header">
          <strong class="me-auto">{{ toast.type === 'success' ? 'Успех' : 'Ошибка' }}</strong>
          <button
              type="button"
              class="btn-close"
              data-bs-dismiss="toast"
              aria-label="Close"
              @click="closeToast"
          ></button>
        </div>
        <div class="toast-body">
          {{ toast.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api.js'; // Импортируем настроенный экземпляр Axios

export default {
  props: {
    title: {
      type: String,
      default: "Добавление нового сайта для проверки",
    },
  },
  data() {
    return {
      link: "", // Сохраняем введенную ссылку
      toast: {
        visible: false,
        message: "",
        type: "", // 'success' или 'error'
      },
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await api.post('/send-link', {
          url: this.link, // Отправляемая ссылка
        });
        this.showToast('Ссылка успешно отправлена!', 'success');
        this.link = ""; // Сбрасываем поле ввода
      } catch (error) {
        console.error('Ошибка отправки ссылки:', error);
        this.showToast('Произошла ошибка при отправке ссылки.', 'error');
      }
    },
    showToast(message, type) {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.visible = true;
      setTimeout(() => {
        this.toast.visible = false;
      }, 3000); // Тост будет виден 3 секунды
    },
    closeToast() {
      this.toast.visible = false;
    },
  },
};
</script>

<style>
.toast-container {
  z-index: 1055; /* Убедитесь, что тост отображается поверх других элементов */
}
</style>
