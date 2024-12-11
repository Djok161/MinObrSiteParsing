<template>
  <div :class="['card custom-card p-3', card.status === 'error' ? 'border-danger' : '']">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h5 :class="['fw-bold', card.status === 'error' ? 'text-danger' : '']">{{ card.tag }}</h5>
        <p class="text-muted mb-0">Последняя проверка: {{ formattedDate }}</p>
      </div>
      <div class="btn-group">
        <button
            class="btn btn-outline-info btn-lg action-btn"
            @click="openRefreshModal"
            :disabled="!canUpload"
            title="Обновить"
        >
          <i class="bi bi-arrow-clockwise"></i>
        </button>
        <button
            class="btn btn-outline-danger btn-lg action-btn"
            @click="openDeleteModal"
            :disabled="!canUpload"
            title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>

    <!-- Основное содержимое карточки -->
    <div class="flex-grow-1">
      <p v-if="card.status === 'parsing_2'" class="text-warning">
        Идет дополнительная обработка нейросетью
      </p>
      <p v-if="card.status === 'error'" class="text-danger">
        {{ statusMessages.error }}
      </p>
      <p v-if="isLoadingStatus" class="text-primary">
        {{ statusMessages[card.status] }}
      </p>
      <p v-if="!isLoadingStatus && canUpload && card.status === 'ok'" class="text-success">
        {{ statusMessages.ok }}
      </p>
    </div>
      <button
          :class="['btn btn-lg navigate-btn', navigateButtonClass]"
          @click="navigate"
          :disabled="isNavigateDisabled"
      >
        Перейти
      </button>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <DeleteModal :show="isDeleteModalVisible" @confirm="confirmDelete" @cancel="cancelDelete" />

    <!-- Модальное окно подтверждения обновления -->
    <RefreshModal :show="isRefreshModalVisible" :card="card" @confirm="handleRefreshConfirm" @cancel="() => (isRefreshModalVisible = false)" />
</template>

<script>
import { ref, computed } from 'vue';
import DeleteModal from '../components/modals/DeleteModal.vue';
import RefreshModal from '../components/modals/RefreshModal.vue';

export default {
  name: 'Card',
  components: {
    DeleteModal,
    RefreshModal,
  },
  props: {
    card: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit }) {
    const isDeleteModalVisible = ref(false);
    const isRefreshModalVisible = ref(false);

    // Открытие модального окна удаления
    const openDeleteModal = () => {
      isDeleteModalVisible.value = true;
    };

    // Подтверждение удаления
    const confirmDelete = () => {
      emit('delete', props.card);
      isDeleteModalVisible.value = false;
    };

    // Отмена удаления
    const cancelDelete = () => {
      isDeleteModalVisible.value = false;
    };

    // Открытие модального окна обновления
    const openRefreshModal = () => {
      isRefreshModalVisible.value = true;
    };

    // Подтверждение обновления
    const handleRefreshConfirm = () => {
      emit('refresh', props.card);
      isRefreshModalVisible.value = false;
    };

    // Навигация по URL карточки
    const navigate = () => {
      if (props.card.status === 'ok' || props.card.status === 'parsing_2') {
        emit('navigate', props.card.tag); // Передаём только 'tag'
      }
    };

    // Форматирование даты из Unix timestamp
    const formattedDate = computed(() => {
      if (props.card.time_start && !isNaN(props.card.time_start)) {
        const date = new Date(props.card.time_start * 1000); // Предполагается, что time_start в секундах
        return date.toLocaleString();
      }
      return 'Неизвестно';
    });

    // Сообщения для статусов
    const statusMessages = {
      ok: "Готово",
      parsing_1: "Основная стадия парсинга",
      parsing_2: "Отчет готов. Идет дополнительная стадия парсинга",
      error: "Ошибка",
      wait: "Ожидание начала парсинга",
    };

    // Определение, находится ли карточка в статусе загрузки
    const isLoadingStatus = computed(() => {
      return props.card.status === 'wait' || props.card.status === 'parsing_1';
    });

    // Определение, можно ли загружать файл
    const canUpload = computed(() => {
      return props.card.status === 'ok' || props.card.status === 'parsing_2';
    });

    // Классы прогресс-бара в зависимости от статуса
    const progressBarClasses = computed(() => {
      if (props.card.status === 'error') {
        return 'bg-danger';
      } else if (isLoadingStatus.value) {
        return 'bg-info progress-bar-striped progress-bar-animated';
      } else if (props.card.status === 'parsing_2') {
        return 'bg-warning';
      }
      return 'bg-success';
    });

    // Классы кнопки "Перейти" в зависимости от статуса
    const navigateButtonClass = computed(() => {
      if (props.card.status === 'error') {
        return 'btn-danger';
      }
      return 'btn-primary';
    });

    // Отключение кнопки "Перейти"
    const isNavigateDisabled = computed(() => {
      return props.card.status !== 'ok' && props.card.status !== 'parsing_2';
    });

    // Классы для текста "соответствие требованиям"
    const requirementsTextClass = computed(() => {
      if (props.card.status === 'error') {
        return 'text-danger';
      } else if (props.card.status === 'wait' || props.card.status === 'parsing_1') {
        return 'text-warning';
      } else if (props.card.status === 'parsing_2') {
        return 'text-warning';
      }
      return 'text-success';
    });

    return {
      isDeleteModalVisible,
      openDeleteModal,
      confirmDelete,
      cancelDelete,
      isRefreshModalVisible,
      openRefreshModal,
      handleRefreshConfirm,
      navigate,
      formattedDate,
      statusMessages,
      isLoadingStatus,
      canUpload,
      progressBarClasses,
      navigateButtonClass,
      isNavigateDisabled,
      requirementsTextClass,
    };
  },
};
</script>

<style scoped>
.custom-card {
  min-height: 300px;
  border-radius: 8px; /* Уменьшаем радиус закругления для более квадратного вида */
  display: flex;
  flex-direction: column;
  height: 100%; /* Позволяет карточке занимать всю доступную высоту */
  transition: transform 0.2s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Добавляем тень */
}

.custom-card:hover {
  transform: translateY(-5px);
}

.btn-group .action-btn {
  width: 50px; /* Увеличиваем ширину кнопок */
  height: 50px; /* Увеличиваем высоту кнопок */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 6px; /* Немного уменьшаем радиус закругления */
  margin-right: 15px; /* Добавляем отступ между кнопками */
}

.btn-group .action-btn:first-child {
  margin-left: 0; /* Убираем отступ у первой кнопки */
}

.btn-group .action-btn:last-child {
  border-bottom-left-radius: 0;
  border-top-left-radius: 0;
}

.btn-group .action-btn i {
  font-size: 1.25rem; /* Увеличиваем размер иконок */
}

.navigate-btn {
  width: 140px; /* Увеличиваем ширину кнопки "Перейти" */
  height: 40px; /* Увеличиваем высоту кнопки "Перейти" */
  font-size: 1.1rem; /* Увеличиваем размер текста кнопки */
  text-align: center; /* Выровнять текст по центру */
  display: flex;
  align-items: center;
  justify-content: center;
}

.requirements-text {
  font-weight: bold;
  font-size: 1rem;
  color: #28A745; /* Зеленый цвет для 'ok' */
}

.text-danger {
  color: #dc3545 !important; /* Красный цвет для 'error' */
}

.text-warning {
  color: #ffc107 !important; /* Желтый цвет для 'wait' и 'parsing_1' */
}

.text-success {
  color: #28A745 !important; /* Зеленый цвет для 'ok' */
}

@media (max-width: 576px) {
  .btn-group .action-btn {
    width: 40px;
    height: 40px;
  }

  .navigate-btn {
    width: 100px; /* Сделать кнопку "Перейти" уже на маленьких экранах */
    height: 40px;
    font-size: 1rem;
  }

  .requirements-text {
    font-size: 0.9rem;
  }
}

/* Стиль для disabled dropzone */
.disabled-dropzone {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
