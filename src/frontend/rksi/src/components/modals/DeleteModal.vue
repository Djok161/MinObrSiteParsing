<template>
  <teleport to="body">
    <div
        class="modal fade"
        tabindex="-1"
        role="dialog"
        aria-labelledby="deleteModalLabel"
        aria-hidden="true"
        ref="modal"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Подтверждение удаления</h5>
            <button type="button" class="btn-close" @click="cancel" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            Вы точно уверены, что хотите удалить эту карточку?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cancel">Выйти</button>
            <button type="button" class="btn btn-danger" @click="confirm">Подтвердить</button>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { Modal } from 'bootstrap';

export default {
  name: 'DeleteModal',
  emits: ['confirm', 'cancel'],
  props: {
    show: {
      type: Boolean,
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

    const confirm = () => {
      emit('confirm');
      hideModal();
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

      // Закрытие модалки при нажатии на кнопку закрытия или вне модалки
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
