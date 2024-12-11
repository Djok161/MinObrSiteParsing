<template>
  <div :class="['card custom-card p-3', card.status === 'err' ? 'border-danger' : '']">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h5 :class="['fw-bold', card.status === 'err' ? 'text-danger' : '']">{{ card.name }}</h5>
        <p class="text-muted mb-0">Последняя проверка: {{ formattedDate }}</p>
      </div>
      <div class="btn-group">
        <button
            class="btn btn-outline-info btn-lg action-btn"
            @click="openRefreshModal"
            :disabled="card.status === 'load'"
            title="Обновить"
        >
          <i class="bi bi-arrow-clockwise"></i>

          <RefreshModal
              :show="isRefreshModalVisible"
              :card="card"
              @confirm="handleRefreshConfirm"
              @cancel="() => (isRefreshModalVisible = false)"></RefreshModal>

        </button>
        <button
            class="btn btn-outline-danger btn-lg action-btn"
            @click="openDeleteModal"
            :disabled="card.status === 'load'"
            title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>

    <!-- Основное содержимое карточки (можно добавить при необходимости) -->
    <div class="flex-grow-1">
      <!-- Здесь можно добавить дополнительное содержимое карточки -->
    </div>

    <!-- Надпись "соответствие требованиям" -->
    <div :class="['requirements-text mb-2', requirementsTextClass]">
      соответствие требованиям
    </div>

    <!-- Прогресс-бара и кнопка "Перейти" на одной линии внизу -->
    <div class="d-flex align-items-center mt-2">
      <div class="progress flex-grow-1 me-3" style="height: 12px;">
        <div
            :class="['progress-bar', progressBarClasses]"
            :style="progressBarStyle"
            role="progressbar"
            :aria-valuenow="progress"
            aria-valuemin="0"
            aria-valuemax="100"
        ></div>
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
  </div>
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

    const openDeleteModal = () => {
      isDeleteModalVisible.value = true;
    };

    const confirmDelete = () => {
      emit('delete', props.card);
      isDeleteModalVisible.value = false;
    };

    const cancelDelete = () => {
      isDeleteModalVisible.value = false;
    };

    const isRefreshModalVisible = ref(false);

    const openRefreshModal = () => {
      isRefreshModalVisible.value = true;
    };

    const handleRefreshConfirm = (cardId) => {
      console.log(`Карточка с ID ${cardId} обновлена`);
      isRefreshModalVisible.value = false;
      emit('refresh');
    };



    const navigate = () => {
      if (props.card.status === 'ok') {
        emit('navigate', props.card);
      }
    };

    const calculateProgress = () => {
      return Math.min(props.card.number_of_prompts_found * 10, 100);
    };

    const progress = computed(() => calculateProgress());

    const progressBarClasses = computed(() => {
      if (props.card.status === 'err') {
        return 'bg-danger';
      } else if (props.card.status === 'load') {
        return 'bg-success progress-bar-striped progress-bar-animated';
      } else {
        return 'bg-success';
      }
    });

    const progressBarStyle = computed(() => {
      if (props.card.status === 'err') {
        return { width: '0%' };
      } else if (props.card.status === 'load') {
        return { width: '100%' };
      } else {
        return { width: `${progress.value}%`, backgroundColor: '#28A745' };
      }
    });

    const navigateButtonClass = computed(() => {
      if (props.card.status === 'err') {
        return 'btn-danger';
      }
      return 'btn-primary';
    });

    const isNavigateDisabled = computed(() => {
      return props.card.status !== 'ok';
    });

    const requirementsTextClass = computed(() => {
      if (props.card.status === 'err') {
        return 'text-danger';
      } else if (props.card.status === 'load') {
        return 'text-warning';
      }
      return 'text-success';
    });

    return {
      isDeleteModalVisible,
      openDeleteModal,
      confirmDelete,
      cancelDelete,
      navigate,
      progress,
      progressBarClasses,
      progressBarStyle,
      navigateButtonClass,
      isNavigateDisabled,
      requirementsTextClass,
      isRefreshModalVisible,
      openRefreshModal,
      handleRefreshConfirm
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
  color: #dc3545 !important; /* Красный цвет для 'err' */
}

.text-warning {
  color: #ffc107 !important; /* Желтый цвет для 'load' */
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
</style>
