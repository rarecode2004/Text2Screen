document.querySelector("form").addEventListener("submit", function(event) {
    // Add any custom validation or logic here
    alert("Logged in!");
    event.preventDefault(); // Prevents default form submission
});
