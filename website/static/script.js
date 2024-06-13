

function defaultManageSettings (id) {
    // 
    id -= 1
    console.log ()
    edit_name_input = document.getElementsByClassName("edit_name") [id];
    submit_button = document.getElementsByClassName ("submit_name") [id];
    //setting the displays
    submit_button.style.display = "none";
    edit_name_input.style.display = "none";

    edit_button = document.getElementsByClassName("editname_button") [id];
    edit_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    //preventing delete button from malfunctioning (because its inside form and sends two post requests)
    delete_button = document.getElementsByClassName ("delete_button") [id]
    delete_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    editquestions_button = document.getElementsByClassName ("editquestions-button") [id]
    editquestions_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form
    
    document.getElementsByClassName ("resultsButton")[id].addEventListener('click', function(event) { event.preventDefault() });
}


function defaultEditQuestionsSettings (id) {
    // 
    id -= 1
    edit_content = document.getElementsByClassName("edit_content") [id];
    submit_content = document.getElementsByClassName ("submit_content") [id];
    //setting the displays
    submit_content.style.display = "none";
    edit_content.style.display = "none";
    


    edit_content = document.getElementsByClassName("edit_question_button") [id];
    edit_content.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    //preventing delete button from malfunctioning (because its inside form and sends two post requests)
    delete_button = document.getElementsByClassName ("delete_question_button") [id]
    delete_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    editquestions_button = document.getElementsByClassName ("edit_answers_button") [id]
    editquestions_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form
    submit_content.addEventListener('click', function(event) { event.preventDefault() });
}


function defaultEditAnswersSettings (id) {
    // 
    id -= 1
    edit_content = document.getElementsByClassName("edit_content") [id];
    submit_content = document.getElementsByClassName ("submit_content") [id];
    //setting the displays
    submit_content.style.display = "none";
    edit_content.style.display = "none";
    
    edit_content = document.getElementsByClassName("edit_answer_button") [id];
    edit_content.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    //preventing delete button from malfunctioning (because its inside form and sends two post requests)
    delete_button = document.getElementsByClassName ("delete_answer_button") [id]
    delete_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form

    status_button = document.getElementsByClassName ("status_button") [id]
    status_button.addEventListener('click', function(event) { event.preventDefault() }); //prevent the problem with the form
    submit_content.addEventListener('click', function(event) { event.preventDefault() });
}


function editNameClick (id) {
    id -= 1;
    document.getElementsByClassName("edit_name") [id].style.display = "inline-block";
    document.getElementsByClassName ("submit_name") [id].style.display = "inline-block";
    document.getElementsByClassName ("editname_button") [id].style.display = "none";
    document.getElementById ("quizaddform").style.display = "none"
}

function editQuestionClick (id) {
    id -= 1;
    document.getElementsByClassName("edit_content") [id].style.display = "inline-block";
    document.getElementsByClassName ("submit_content") [id].style.display = "inline-block";
    document.getElementsByClassName ("edit_question_button") [id].style.display = "none";
    document.getElementById ("addquestionform").style.display = 'none'

}

function deleteQuiz (quiz_id) {

    var confirmed = confirm("Are you sure that you want to delete the quiz ?");
    if (confirmed) {
    
    fetch ("/delete-quiz", {
        method: "POST",
        body: JSON.stringify ({quiz_id: quiz_id}),
    }).then ((_res) => {
        window.location.href = "manage";
    });
        }
    }

function editQuestions (quiz_id) { //makes the url
    window.location.href = `edit-questions?quizid=${quiz_id}`;
}

function deleteQuestion (quiz_id, question_id) {
    var confirmed = confirm("Are you sure that you want to delete the question ?");
    if (confirmed) {

    fetch ("/delete-question", {
        method: "POST",
        body: JSON.stringify ({question_id: question_id}),
    }).then ((_res) => {
        editQuestions (quiz_id);
    });

}   
    }

function updateQuestion (quiz_id, question_id, num) {
    num--;
    new_value = document.getElementsByName ("edit_content")[num].value
    fetch ("/update-question", {
        
        method: "POST",
        body: JSON.stringify ({question_id: question_id, new_value: new_value})
    }).then ((_res) => {
        editQuestions (quiz_id);
    });
    }

    function goToAnswers (questionId) {
        window.location.href = `edit-answers?questionid=${questionId}`;
    }
function statusButton (id, question_id, answer_id) {
    id--;
    let new_state =false;
    let button = document.getElementsByClassName ("status_button") [id];
    if (button.innerHTML == "Correct") {
        button.innerHTML = "Wrong"
        button.classList.remove('btn-success')
        button.classList.add('btn-danger')
        new_state = false;

            //make a request to change the value;
    }else {
        button.innerHTML = "Correct"
        button.classList.remove('btn-danger')
        button.classList.add('btn-success')
        new_state = true;
    }
    changeAnswer (id, answer_id, question_id, new_state)
}



function changeAnswer (id, answer_id, question_id, new_state) {
    id--;
    fetch ("/change-answer-state", {
        method: "POST",
        body: JSON.stringify ({new_state: new_state , answer_id: answer_id})
    }).then ((_res) => {
        goToAnswers (question_id);
    });
}

function deleteAnswer (question_id, answer_id) {

    var confirmed = confirm("Are you sure that you want to delete the answer ?");
    if (confirmed) {
                
            

    fetch ("/delete-answer", {
        method: "POST",
        body: JSON.stringify ({answer_id: answer_id}),
    }).then ((_res) => {
        goToAnswers (question_id);
    });

        }

    }

    function editAnswerClick (id) {
        id -= 1;
        document.getElementsByClassName("edit_content") [id].style.display = "inline-block";
        document.getElementsByClassName ("submit_content") [id].style.display = "inline-block";
        document.getElementsByClassName ("edit_answer_button") [id].style.display = "none";
        document.getElementById ("addAnswerForm").style.display = 'none'
    }

    function updateAnswer (question_id, answer_id, num) {
        num--;
        new_value = document.getElementsByName ("edit_content")[num].value
        fetch ("/update-answer", {
            
            method: "POST",
            body: JSON.stringify ({answer_id: answer_id, new_value: new_value})
        }).then ((_res) => {
            goToAnswers (question_id);
        });
        }
    

    function clickOnAnswer (id) {

        id--;
        answer = document.getElementsByClassName ("single_answer") [id]

        input_field = document.getElementsByName ("single_answer") [id]
        if (input_field.value == "0") {

            answer.classList.add('active');
            input_field.value = '1';
        }else {
            answer.classList.remove('active');
            input_field.value = '0';
        }
        
    }
    
    // function submitAnswers () {
    //     let arr = [];
    //     let answers = document.getElementsByClassName ("single_answer")
    //     for (let i =0; i<answers.length; i++) {
    //         arr.push (answers[i].value)
    //     }
    //     //pass the array to json
    // }

    function resetDefault (buttonclass, id) {
        id--;

        document.getElementsByClassName(buttonclass) [id].addEventListener('click', function(event) { event.preventDefault() })
    }
    function goToQuizResults (quiz_id) {
        window.location.href = `results?quizid=${quiz_id}`;
    
    }

    function deleteResult (result_id, quiz_id, is_results = 0) {
    let msg; 
    if (is_results) {
        msg = "Are you sure that you want to delete ALL the results ?";
    }else {
        msg = "Are you sure that you want to delete the result ?";
    }
    var confirmed = confirm(msg);
    if (confirmed) {
        fetch ("/delete-result", {
            method: "POST",
            body: JSON.stringify ({result_id: result_id, quiz_id: quiz_id}),
        }).then ((_res) => {
            goToQuizResults (quiz_id);
            
        });
    }
    }

    class Message {
    
        
        static red(message) {

            console.log (message)
            document.getElementById('errorArea').innerHTML += `<span class='text-danger'>${message}</span><br>`;
        }
        static green(message) {
            document.getElementById('errorArea').innerHTML += `<span class='text-success'>${message}</span><br>`;
        }
    }
    // Message.red ("SAD")

    let showDropdownChildren =(id)=> {
            // Select all elements with class "dropdown_child"
        const dropdownChildren = document.querySelectorAll('.dropdown_id' + id);

    // Loop through each element
        dropdownChildren.forEach(element => {
            if (element.style.display === 'inline') {
            element.style.display = 'none';
            } else {
            element.style.display = 'inline';
            }
        });
        
    }

    const goToConstructor = (quiz_id) => {
        window.location.href = `constructor?quizid=${quiz_id}`;
    } 