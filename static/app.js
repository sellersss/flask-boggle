class BoggleGame {
    constructor() {
        this.time = 60;
        this.answers = [];
    }

    startGame() {
        this.submitForm();
        this.stopwatch();
    }

    submitForm(e) {
        $('#guess-form').on('submit', this.handleSubmit.bind(this));
    }


    /* On page load, start timer for boggle */
    stopwatch() {
        let {
            time
        } = this;
        const ticking = setInterval(() => {
            time -= 1;
            $('#timer span').text(time)

            if (time === 0) {
                clearInterval(ticking);
                this.sendStats();
                this.showRestart();
            }
        }, 1000)
    }

    /* When submitting user guess, the form checks the answer */
    async handleSubmit(e) {
        // Prevent page from refreshing
        e.preventDefault();

        // Saves the guess to variable
        const guess = $('#guess')[0].value;

        // Checks the guess and returns the result
        const result = await this.checkGuess(guess);

        // Update message based on result of the guess
        this.updateMessage(result, guess);

        // Reset the value of the input
        $('#guess').val('');
    }

    /* AJAX request to send the check to the server and check it */
    async checkGuess(guess) {
        const res = await axios.get(`/check-guess`, {
            params: {
                guess: guess
            }
        });
        return res.data.result;
    }

    /* Update the message after checking the guess */
    updateMessage(res, word) {
        let {
            answers
        } = this;
        if (res == 'not-on-board') {
            $('#result-msg').text('This word is not on the board.');
        } else if (res == 'not-word') {
            $('#result-msg').text('This is not a valid word.');
        } else if (res == 'ok') {
            for (let answer of answers) {
                if (word == answer) {
                    $('#result-msg').text('You have already guessed this word.');
                    return;
                }
            }
            this.keepScore(word);
            answers.push(word);
            $('#result-msg').text('Nice! This word was found on the board.');
        }
    }

    /* Update the score after a correct guess */
    keepScore(word) {
        let score = Number($('#score span').text());
        score += word.length;
        $('#score span').text(score);
    }

    /* Send the stats for the user to the backend */
    async sendStats() {
        let score = Number($('#score span').text());

        await axios.post('/stats', {
            score: score
        });
    }

    showRestart() {
        $('#guess-form').hide();
        $('#timer').hide();
        $('#restart-btn').show();
        $('#result-msg').text('Game Over!')

        $('#restart-btn').on('click', () => {
            window.location.reload();
        })
    }
}

let player = new BoggleGame();

player.startGame();