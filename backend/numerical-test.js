document.addEventListener("DOMContentLoaded", function () {
  const questions = [
      {
          question: "If a car travels at a speed of 60 miles per hour how far will it travel in 2.5 hours?",
          options: ["A. 125 miles", "B. 150 miles", "C. 175 miles", "D. 200 miles."],
          answer: "b",
      },
      {
          question: "If a rectangular garden measures 12 meters in length and 8 meters in width, what is the area of the garden?",
          options: ["A. 80 square meters", "B. 96 square meters", "C. 104 square meters", "D. 120 square meters"],
          answer: "b",
      },
      {
          question: "If a recipe calls for 2 cups of flour to make 12 cookies, how many cups of flour are needed to make 36 cookies?",
          options: ["A. 4 cups", "B. 6 cups", "C. 8 cups", "D. 12 cups"],
          answer: "b",
      },
      {
          question: "If 30% of the students in a class are girls, and there are 24 boys, how many students are in the class in total?",
          options: ["A. 40", "B. 50", "C. 60", "D. 70"],
          answer: "c",
      },
      {
          question: "A store sells a product for $20, and the cost to produce each unit is $12. What is the store's profit per unit?",
          options: ["A. $4", "B. $6", "C. $8", "D. $10"],
          answer: "b",
      },
      {
          question: "A box contains 24 red balls, 36 blue balls, and 40 green balls. What is the probability of selecting a blue ball randomly?",
          options: ["A. 1/4", "B. 1/3", "C. 1/2", "D. 2/3"],
          answer: "b",
      },
      {
          question: "If 5/8 of a number is 35, what is the number?",
          options: ["A. 56", "B. 45", "C. 55", "D. 40"],
          answer: "a",
      },
  ];

  let currentQuestionIndex = 0;
  let score = 0;
  let quizCompleted = false; // Flag to track if quiz has been completed
  const quizContainer = document.getElementById("question-container-3");
  let selectedOptions = []; // Array to store selected options
  let prevSelectedOption = null; // Variable to store previously selected option
  let correctAnswers = []; // Array to store correct answers

  // Initialize correct answers array
  questions.forEach((question) => {
      correctAnswers.push(question.answer.toLowerCase());
  });

  function createQuestion(question, index) {
      if (index === questions.length - 1) {
          // Last question, show submit button instead
          quizContainer.innerHTML = `
              <div class="question-3">
                  <p>${question.question}</p>
                  <ul class="options-3">
                      ${question.options
                          .map(
                              (option, i) =>
                                  `<li><button type="button" data-index="${i}" data-answer="${option
                                      .split(".")[0]
                                      .toLowerCase()}" ${selectedOptions[index] === i ? 'class="selected"' : ''}>${option}</button></li>`
                          )
                          .join("")}
                  </ul>
                  <button id="submit-btn-3">Submit</button>
              </div>
          `;
          
          // Handle submit button click
          document.getElementById("submit-btn-3").addEventListener("click", () => {
              quizCompleted = true;
              showScore();
              // Remove event listener for the previous button after submitting
              document.getElementById("prev-btn-3").removeEventListener("click", prevQuestion);
              document.getElementById("prev-btn-3").style.display = "none";
              document.getElementById("next-btn-3").style.display = "none";

          });
      } else {
          // Regular question, display as usual
          quizContainer.innerHTML = `
              <div class="question-3">
                  <p>${question.question}</p>
                  <ul class="options-3">
                      ${question.options
                          .map(
                              (option, i) =>
                                  `<li><button type="button" data-index="${i}" data-answer="${option
                                      .split(".")[0]
                                      .toLowerCase()}" ${selectedOptions[index] === i ? 'class="selected"' : ''}>${option}</button></li>`
                          )
                          .join("")}
                  </ul>
              </div>
          `;
      }
  
      const options = quizContainer.querySelectorAll(".options-3 button");
      options.forEach((option, i) => {
          option.addEventListener("click", () => {
              const selectedAnswer = option.getAttribute("data-answer");
              if (prevSelectedOption !== null && prevSelectedOption === correctAnswers[index] && selectedAnswer !== correctAnswers[index]) {
                  // Deduct score only if the previous option was correct and now changed to wrong, and score is greater than 0
                  if (score > 0) {
                      score -= 2;
                  }
              }
              if (selectedAnswer === correctAnswers[index]) {
                  score += 2; // Increase score by 2 for each correct answer
              }
              options.forEach((opt) => opt.classList.remove("selected")); // Remove selected class from all options
              option.classList.add("selected"); // Add selected class to the clicked option
              option.disabled = true; // Disable the selected option
              selectedOptions[index] = i; // Store the index of the selected option
              prevSelectedOption = selectedAnswer; // Update the previous selected option
              showScore(); // Update score display after answering
          });
      });
  
      updateProgressBar();
  }
  
  

  function nextQuestion() {
      if (!quizCompleted) {
          currentQuestionIndex++;
          if (currentQuestionIndex < questions.length) {
              createQuestion(questions[currentQuestionIndex], currentQuestionIndex);
          } else {
              quizCompleted = true;
              showScore();
          }
      }
  }

  document.getElementById("next-btn-3").addEventListener("click", nextQuestion);

  function prevQuestion() {
      if (currentQuestionIndex > 0) {
          currentQuestionIndex--;
          createQuestion(questions[currentQuestionIndex], currentQuestionIndex);
      }
  }

  document.getElementById("prev-btn-3").addEventListener("click", prevQuestion);

  function updateProgressBar() {
      if (currentQuestionIndex >= 0) {
          const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
          document.getElementById("progress-3").style.width = progress + "%";
      }
  }

  function showScore() {
      if (quizCompleted) {
          const perscore = (score / (questions.length * 2)) * 100;
          const normalized_score = ((perscore - 0) * (10 - 1)) / (100 - 0) + 1;
          document.getElementById("score-container-3").textContent =
              "Your score: " + parseFloat(normalized_score.toFixed(2));
      }
  }

  document.getElementById("start-btn-3").addEventListener("click", () => {
      setTimeout(() => {
          document.getElementById("start-btn-3").style.display = "none";
          document.getElementById("prev-btn-3").style.display = "inline-block";
          document.getElementById("next-btn-3").style.display = "inline-block";
          createQuestion(questions[currentQuestionIndex], currentQuestionIndex);
      }, 1000);
  });

  document
      .getElementById("aptitudeTestForm-3")
      .addEventListener("submit", (e) => {
          e.preventDefault();
      });

  document.getElementById("prev-btn-3").addEventListener("click", prevQuestion);
  document.getElementById("next-btn-3").addEventListener("click", nextQuestion);
});
