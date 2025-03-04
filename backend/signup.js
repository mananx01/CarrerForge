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
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var pno = document.getElementById("pno").value;
    var dob = document.getElementById("dob").value;
    var password = document.getElementById("password").value;
  
    if (name === "" || email === "" || pno === "" || dob === "" || password === "") {
      alert("All fields are required");
      return false; 
    }
  
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

  
    var pnoRegex = /^\d{10}$/;
    if (!pnoRegex.test(pno)) {
      alert("Phone number must be 10 digits");
      return false; 
    }
  
    return true;
  }
  document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault(); 
    if (validateForm()) {
      this.submit();
    }
  });
  