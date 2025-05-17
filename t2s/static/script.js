document.querySelector(".cta-btn").addEventListener("click", function () {
  alert("Turning text into video now...");
});

// For the menu toggle on mobile view
const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

menuToggle.addEventListener("click", function () {
  menuToggle.classList.toggle("active");
  navLinks.classList.toggle("active");
});
