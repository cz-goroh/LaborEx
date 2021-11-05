document.addEventListener('DOMContentLoaded', () => {
  // * Open-Close modals ===========================================
  // * =============================================================

  const modalBtn = document.querySelectorAll('[data-modal]');
  const body = document.body;
  const modalClose = document.querySelectorAll('.modal__close');
  const modal = document.querySelectorAll('.modal');

  modalBtn.forEach((item) => {
    item.addEventListener('click', (event) => {
      event.preventDefault();
      let $this = event.currentTarget;
      let modalId = $this.getAttribute('data-modal');
      let modal = document.getElementById(modalId);
      let modalContent = modal.querySelector('.modal__content');


      modalContent.addEventListener('click', (event) => {
        event.stopPropagation();
      });
      modal.classList.add('show');
      body.classList.add('no-scroll');

      setTimeout(() => {
        modalContent.style.transform = 'none';
        modalContent.style.opacity = '1';
      }, 300);
    });
  });

  modalClose.forEach((item) => {
    item.addEventListener('click', (event) => {
      let currentModal = event.currentTarget.closest('.modal');

      closeModal(currentModal);
    });
  });

  modal.forEach((item) => {
    item.addEventListener('click', (event) => {
      let currentModal = event.currentTarget;

      closeModal(currentModal);
    });
  });

  function closeModal(currentModal) {
    let modalContent = currentModal.querySelector('.modal__content');
    modalContent.removeAttribute('style');

    setTimeout(() => {
      currentModal.classList.remove('show');
      body.classList.remove('no-scroll');
    }, 300);
  }

  // * Sliders =============================================
  // * =====================================================

  const reviews = new Swiper('.reviews__slider', {
    watchSlidesVisibility: true,
    slidesPerView: 3,
    loop: true,
    spaceBetween: 30,
    observer: true,
    updateOnWindowResize: true,
    navigation: {
      nextEl: '.reviews__button-next',
    },

    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },

    breakpoints: {
      992: {
        slidesPerView: 3,
        spaceBetween: 30,
      },
      576: {
        slidesPerView: 2,
        spaceBetween: 30,
      },
      319: {
        slidesPerView: 1,
        spaceBetween: 30,
        autoplay: false,
      },
    },
  });

  // * Accordions =======================================================
  // * =================================================================

  const accordions = document.querySelectorAll('.accordion__item-title');
  const contents = document.querySelectorAll('.accordion__item-content');

  accordions.forEach((itemAcc) => {
    itemAcc.addEventListener('click', (event) => {
      event.preventDefault();

      const context = itemAcc.nextElementSibling;

      if (context.style.maxHeight) {
        context.style.maxHeight = null;
        itemAcc.classList.remove('open');
      } else {
        context.style.maxHeight = context.scrollHeight + 'px';
        itemAcc.classList.add('open');
      }

      contents.forEach((itemCon) => {
        if (itemCon !== context) {
          itemCon.style.maxHeight = null;
        }
      });

      accordions.forEach((item) => {
        if (item !== itemAcc) {
          item.classList.remove('open');
        }
      });
    });
  });

  // * Open-Close burger list ==============================
  // * =======================================================

  const buttonBurger = document.querySelector('.burger__icon');
  const menuClose = document.querySelector('.burger__menu-close');
  const burgerMenu = document.querySelector('.burger__menu');

  buttonBurger.addEventListener('click', () => {
    burgerMenu.classList.toggle('active');
  });
  menuClose.addEventListener('click', () => {
    burgerMenu.classList.remove('active');
  });
});
