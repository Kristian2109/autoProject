"use strict";

// The site is static. An enquiry is composed locally and opened in the visitor's email app.
const CONTACT_EMAIL = "kristian.petrov1998@gmail.com";

const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");
function closeMenu() {
  navigation?.classList.remove("is-open");
  menuToggle?.setAttribute("aria-expanded", "false");
  menuToggle?.setAttribute("aria-label", "Отвори менюто");
}
menuToggle?.addEventListener("click", () => {
  const open = menuToggle.getAttribute("aria-expanded") !== "true";
  navigation.classList.toggle("is-open", open);
  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute(
    "aria-label",
    open ? "Затвори менюто" : "Отвори менюто",
  );
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".site-header")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && navigation?.classList.contains("is-open")) {
    closeMenu();
    menuToggle.focus();
  }
});
navigation
  ?.querySelectorAll("a")
  .forEach((link) => link.addEventListener("click", closeMenu));
window.matchMedia("(min-width: 851px)").addEventListener("change", closeMenu);

const filterButtons = [...document.querySelectorAll(".filter")];
const galleryCards = [
  ...document.querySelectorAll(".gallery-grid .project-card"),
];
filterButtons.forEach((button) =>
  button.addEventListener("click", () => {
    const category = button.dataset.filter;
    filterButtons.forEach((filter) =>
      filter.setAttribute("aria-pressed", String(filter === button)),
    );
    galleryCards.forEach((card) => {
      card.hidden = category !== "all" && card.dataset.category !== category;
    });
    const count = galleryCards.filter((card) => !card.hidden).length;
    document.querySelector(".gallery-count").textContent =
      `${count} ${count === 1 ? "изработка" : "изработки"}`;
  }),
);

const lightbox = document.querySelector(".lightbox");
if (lightbox) {
  let currentIndex = 0;
  let activePhotos = [];
  let opener = null;
  const image = lightbox.querySelector(".lightbox-image");
  const caption = lightbox.querySelector(".lightbox-title");
  const counter = lightbox.querySelector(".lightbox-counter");
  const prev = lightbox.querySelector(".lightbox-prev");
  const next = lightbox.querySelector(".lightbox-next");
  function showPhoto(index) {
    currentIndex = (index + activePhotos.length) % activePhotos.length;
    const button = activePhotos[currentIndex];
    const thumbnail = button.querySelector("img");
    image.src = thumbnail.src;
    image.alt = thumbnail.alt;
    caption.textContent = button.dataset.title;
    counter.textContent = `${currentIndex + 1} / ${activePhotos.length}`;
    prev.hidden = next.hidden = activePhotos.length < 2;
  }
  document.querySelectorAll("[data-lightbox]").forEach((button) => {
    button.addEventListener("click", () => {
      opener = button;
      activePhotos = [...document.querySelectorAll("[data-lightbox]")].filter(
        (photo) => !photo.closest(".project-card").hidden,
      );
      showPhoto(activePhotos.indexOf(button));
      lightbox.showModal();
      document.body.classList.add("modal-open");
    });
  });
  lightbox
    .querySelector(".lightbox-close")
    .addEventListener("click", () => lightbox.close());
  prev.addEventListener("click", () => showPhoto(currentIndex - 1));
  next.addEventListener("click", () => showPhoto(currentIndex + 1));
  lightbox.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      showPhoto(currentIndex + (event.key === "ArrowLeft" ? -1 : 1));
    }
  });
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) lightbox.close();
  });
  lightbox.addEventListener("close", () => {
    document.body.classList.remove("modal-open");
    opener?.focus();
  });
}

const enquiryForm = document.querySelector("#enquiry-form");
enquiryForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!enquiryForm.reportValidity()) return;
  const data = new FormData(enquiryForm);
  const value = (key) => String(data.get(key) || "").trim();
  if (!value("name") || value("message").length < 10) {
    const field = enquiryForm.elements[!value("name") ? "name" : "message"];
    field.setCustomValidity(
      "Моля, попълнете име и описание от поне 10 символа.",
    );
    field.reportValidity();
    field.addEventListener("input", () => field.setCustomValidity(""), {
      once: true,
    });
    return;
  }
  const subject = `Запитване за ${value("service")} — ${value("name")}`;
  const body = [
    "Здравейте,",
    "",
    "Бих искал/а да получа информация за следното:",
    "",
    `Услуга: ${value("service")}`,
    `Автомобил / предмет: ${value("vehicle") || "Не е посочен"}`,
    "",
    value("message"),
    "",
    `Име: ${value("name")}`,
    `Имейл за отговор: ${value("email")}`,
    `Телефон: ${value("phone") || "Не е посочен"}`,
  ].join("\r\n");
  const mailto = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  const status = document.querySelector("#form-status");
  status.replaceChildren(
    document.createTextNode(
      "Писмото е подготвено. Изпратете го от пощенското си приложение. Ако то не се отвори, ",
    ),
  );
  const retry = document.createElement("a");
  retry.href = mailto;
  retry.textContent = "отворете писмото оттук";
  status.append(
    retry,
    document.createTextNode(` или пишете директно на ${CONTACT_EMAIL}.`),
  );
  status.hidden = false;
  window.location.href = mailto;
});
