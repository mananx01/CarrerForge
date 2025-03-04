const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
function validateForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var emailReq = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var passwordReq = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;

    if(!emailReq.test(email)) {
        alert("Invalid email address!");
        return false;
    }

    if(!passwordReq.test(password)) {
        alert("Password must contain at least one digit, one lowercase and one uppercase letter, and be between 6 to 20 characters long!");
        return false;
    }

    return true;
}