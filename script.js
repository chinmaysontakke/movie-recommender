const USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
};

let loggedIn = false;
let currentUser = '';
let movies = [];

// Fetch movie poster and rating from API
async function fetchPoster(movieId) {
    const url = `https://api.themoviedb.org/3/movie/${movieId}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        const posterPath = data.poster_path ? `https://image.tmdb.org/t/p/w500/${data.poster_path}` : 'https://via.placeholder.com/500x750?text=No+Image';
        const rating = data.vote_average || 'N/A';
        return { posterPath, rating };
    } catch (error) {
        console.error('Error fetching poster data:', error);
        return { posterPath: 'https://via.placeholder.com/500x750?text=No+Image', rating: 'N/A' };
    }
}

// Handle login
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

// Populate the movie selection dropdown
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

// Recommend movies based on the selected movie
async function recommendMovies(selectedMovie) {
    const recommendedMovies = movies.filter(movie => movie.title !== selectedMovie);
    const recommendations = [];
    for (let i = 0; i < 5; i++) {
        const movie = recommendedMovies[i];
        const { posterPath, rating } = await fetchPoster(movie.movie_id);
        recommendations.push({ name: movie.title, poster: posterPath, rating });
    }
    return recommendations;
}

// Get random movie recommendations
async function randomMovies() {
    const randomMovies = movies.sort(() => Math.random() - 0.5).slice(0, 5);
    const recommendations = [];
    for (let movie of randomMovies) {
        const { posterPath, rating } = await fetchPoster(movie.movie_id);
        recommendations.push({ name: movie.title, poster: posterPath, rating });
    }
    return recommendations;
}

// Display movies in the recommendations section
function displayMovies(movieList) {
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

// Handle logout
function logout() {
    loggedIn = false;
    currentUser = '';
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('main-content').style.display = 'none';
}

// Event listeners
document.getElementById('login-form').addEventListener('submit', handleLogin);
document.getElementById('recommend-button').addEventListener('click', async () => {
    const selectedMovie = document.getElementById('movie-select').value;
    const recommendations = await recommendMovies(selectedMovie);
    displayMovies(recommendations);
});
document.getElementById('random-button').addEventListener('click', async () => {
    const recommendations = await randomMovies();
    displayMovies(recommendations);
});
document.getElementById('logout-button').addEventListener('click', logout);

// Load movies from an external source (simulate movie data loading)
async function loadMovies() {
    // Replace with actual movie data load (e.g., from a file or API)
    movies = [
        { title: "Movie 1", movie_id: 1 },
        { title: "Movie 2", movie_id: 2 },
        { title: "Movie 3", movie_id: 3 },
        { title: "Movie 4", movie_id: 4 },
        { title: "Movie 5", movie_id: 5 },
        // Add more movies as needed
    ];
}

loadMovies();
