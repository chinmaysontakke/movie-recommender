// Dummy movie data (this would normally come from a backend or API)
const movies = [
    { title: "Movie 1", movie_id: 1 },
    { title: "Movie 2", movie_id: 2 },
    { title: "Movie 3", movie_id: 3 },
    { title: "Movie 4", movie_id: 4 },
    { title: "Movie 5", movie_id: 5 },
    // Add more movie data as needed
];

const USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
};

let loggedIn = false;
let currentUser = '';

// Function to simulate fetching poster data and ratings from an API
function fetchPoster(movieId) {
    const posterPath = `https://via.placeholder.com/500x750?text=Movie+${movieId}`; // Placeholder poster
    const rating = Math.random() * 5 + 3; // Random rating between 3 and 8
    return { posterPath, rating: rating.toFixed(1) };
}

// Function to handle login
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (USER_CREDENTIALS[username] === password) {
        loggedIn = true;
        currentUser = username;
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
        document.getElementById('username-display').textContent = username;
        populateMovieSelect();
    } else {
        document.getElementById('login-error').textContent = 'Invalid Credentials ❌';
    }
}

// Function to populate the movie select dropdown
function populateMovieSelect() {
    const movieSelect = document.getElementById('movie-select');
    movieSelect.innerHTML = '';
    movies.forEach(movie => {
        const option = document.createElement('option');
        option.value = movie.title;
        option.textContent = movie.title;
        movieSelect.appendChild(option);
    });
}

// Function to show movie recommendations
function showRecommendations() {
    const selectedMovie = document.getElementById('movie-select').value;
    const recommendations = getRecommendations(selectedMovie);
    displayMovieList(recommendations);
}

// Function to show random movies
function showRandomMovies() {
    const randomMovies = getRandomMovies();
    displayMovieList(randomMovies);
}

// Function to get movie recommendations based on selected movie
function getRecommendations(selectedMovie) {
    return movies.filter(movie => movie.title !== selectedMovie).slice(0, 5).map(movie => {
        const { posterPath, rating } = fetchPoster(movie.movie_id);
        return { name: movie.title, poster: posterPath, rating };
    });
}

// Function to get random movie picks
function getRandomMovies() {
    const randomMovies = movies.slice().sort(() => Math.random() - 0.5).slice(0, 5);
    return randomMovies.map(movie => {
        const { posterPath, rating } = fetchPoster(movie.movie_id);
        return { name: movie.title, poster: posterPath, rating };
    });
}

// Function to display movie list
function displayMovieList(movieList) {
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '';

    movieList.forEach(movie => {
        const movieItem = document.createElement('div');
        movieItem.classList.add('movie-item');
        
        const img = document.createElement('img');
        img.src = movie.poster;
        movieItem.appendChild(img);
        
        const title = document.createElement('div');
        title.classList.add('movie-title');
        title.textContent = movie.name;
        movieItem.appendChild(title);
        
        const rating = document.createElement('div');
        rating.classList.add('rating');
        rating.textContent = `⭐ ${movie.rating}`;
        movieItem.appendChild(rating);
        
        recommendationsDiv.appendChild(movieItem);
    });
}

// Logout functionality
function logout() {
    loggedIn = false;
    currentUser = '';
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('main-content').style.display = 'none';
}

// Event listeners
document.getElementById('login-form').addEventListener('submit', handleLogin);
document.getElementById('recommend-button').addEventListener('click', showRecommendations);
document.getElementById('random-button').addEventListener('click', showRandomMovies);
document.getElementById('logout-button').addEventListener('click', logout);
