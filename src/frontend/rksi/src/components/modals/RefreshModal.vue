<template>
  <teleport to="body">
    <div
        class="modal fade"
        tabindex="-1"
        role="dialog"
        aria-labelledby="refreshModalLabel"
        aria-hidden="true"
        ref="modal"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="refreshModalLabel">Обновление карточки</h5>
            <button type="button" class="btn-close" @click="cancel" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            Вы уверены, что хотите обновить эту карточку?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cancel">Отмена</button>
            <button type="button" class="btn btn-primary" @click="confirm">Обновить</button>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { Modal } from 'bootstrap';
import api from '../../services/api'; // Предполагается, что у вас есть настроенный axios API

export default {
  name: 'RefreshModal',
  emits: ['confirm', 'cancel'],
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    card: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit }) {
    const modal = ref(null);
    let bsModal = null;

    const showModal = () => {
      if (bsModal) {
        bsModal.show();
      }
    };

    const hideModal = () => {
      if (bsModal) {
        bsModal.hide();
      }
    };

    const confirm = async () => {
      try {
        const response = await api.post(`/cards/refresh/${props.card.id}`);
        if (response.status === 200) {
          emit('confirm', props.card.id); // Эмитим событие для обновления карточки
          hideModal();
        } else {
          alert(`Ошибка при обновлении карточки. Код: ${response.status}`);
        }
      } catch (error) {
        console.error('Ошибка при обновлении карточки:', error);
        alert('Произошла ошибка при обновлении карточки.');
      }
    };

    const cancel = () => {
      emit('cancel');
      hideModal();
    };

    onMounted(() => {
      bsModal = new Modal(modal.value, {
        backdrop: 'static',
        keyboard: false,
      });

      modal.value.addEventListener('hidden.bs.modal', () => {
        emit('cancel');
      });

      if (props.show) {
        showModal();
      }
    });

    watch(
        () => props.show,
        (newVal) => {
          if (newVal) {
            showModal();
          } else {
            hideModal();
          }
        }
    );

    onBeforeUnmount(() => {
      if (bsModal) {
        bsModal.dispose();
      }
    });

    return {
      modal,
      confirm,
      cancel,
    };
  },
};
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>
