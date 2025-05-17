// Add any form validation or other interactive JS here if needed
document.querySelector("form").addEventListener("submit", function(e) {
    e.preventDefault();
    // Placeholder function for form submission logic
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    console.log("Email: ", email);
    console.log("Password: ", password);

    // Add authentication logic or submission to server here
});