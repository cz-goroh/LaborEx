document.addEventListener('DOMContentLoaded', () => {
  // * Open-Close burger-modal ==============================
  // * ======================================================
  function openCloseBurgerModal() {
    let popupsToggle = document.querySelectorAll('.open-popup');
    let popupClose = document.querySelectorAll('.close');

    popupsToggle.forEach(function (item) {
      item.addEventListener('click', function () {
        let popupName = item.getAttribute('data-popup');
        document.getElementById(popupName).style.display = 'block';
      });
    });

    popupClose.forEach(function (item) {
      item.addEventListener('click', function () {
        let popup = item.closest('.modal-open');
        popup.style.display = 'none';
      });
    });

    window.onclick = function (e) {
      if (e.target.classList.contains('modal-open')) {
        e.target.style.display = 'none';
      }
    };
  }
  openCloseBurgerModal();

  // * Added attribute "checked" ==================================
  // * ============================================================
  function addChecked() {
    const labels = document.querySelectorAll('label');

    labels.forEach(function (box) {
      box.addEventListener('click', function () {
        const el = this.previousElementSibling;

        if (!el.checked) {
          el.setAttribute('checked', true);
        } else {
          el.setAttribute('checked', false);
        }
      });
    });
  }
  addChecked();

  // * Burger-modal Tabs ==========================================
  // * ============================================================
  function burgerModalTabs() {
    document.querySelectorAll('.tabs-triggers__item').forEach((item) => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const id = e.target.getAttribute('href').replace('#', '');

        document.querySelectorAll('.tabs-triggers__item').forEach((child) => {
          child.classList.remove('tabs-triggers__item--active');
        });

        document.querySelectorAll('.tabs-content__item').forEach((child) => {
          child.classList.remove('tabs-content__item--active');
        });

        item.classList.add('tabs-triggers__item--active');
        document.getElementById(id).classList.add('tabs-content__item--active');
      });
    });
  }
  burgerModalTabs();

  // * Open-Close modals ===========================================
  // * =============================================================

  function openCloseModals() {
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
  }
  openCloseModals();

  // * Dropdown ============================================
  // * =====================================================
  function openDropdown() {
    const dropdown = document.querySelectorAll('.dropdown');

    for (item of dropdown) {
      item.addEventListener('click', function () {
        if (this.classList.contains('active')) {
          this.classList.remove('active');
        } else {
          for (el of dropdown) {
            el.classList.remove('active');
          }
          this.classList.add('active');
        }
      });
    }
  }
  openDropdown();
  //

  // * Open-Close burger list ==============================
  // * =======================================================
  function openCloseBurgerList() {
    const buttonBurger = document.querySelector('.burger__icon');
    const menuClose = document.querySelector('.burger__menu-close');
    const burgerMenu = document.querySelector('.burger__menu');

    buttonBurger.addEventListener('click', () => {
      burgerMenu.classList.toggle('active');
    });
    menuClose.addEventListener('click', () => {
      burgerMenu.classList.remove('active');
    });
  }
  openCloseBurgerList();

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

  function accordions() {
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
  }
  accordions();
});
