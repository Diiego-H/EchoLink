import random
import json


questions = [
    # Inspiration and Creative Process
    "What inspires you the most when writing or performing a song?",
    "How do you overcome writer's block or performance anxiety?",
    "Do you have a specific routine or ritual before performing or recording?",
    "What’s the most unusual source of inspiration for a song you’ve written?",
    "How do you decide when a song is complete?",
    "Do you prefer performing live or recording in a studio? Why?",
    "How do you stay motivated to practice and perform consistently?",
    "What’s your favorite genre or style of music to sing, and why?",
    "How do you experiment with your vocal techniques or styles?",
    "Do you ever revisit old songs and rework or reinterpret them?",

    # Personal Journey
    "When did you first realize you wanted to be a singer?",
    "Who was your biggest supporter when you started your music career?",
    "What’s the first song you ever performed in front of an audience?",
    "How has your vocal style or range evolved over the years?",
    "What’s the most significant lesson you’ve learned as a singer?",
    "Did you have any formal training, or are you self-taught?",
    "Who are your biggest musical influences?",
    "What’s the best advice you’ve ever received about singing or performing?",
    "How do you handle criticism of your performances or music?",
    "What’s the proudest moment of your singing career so far?",

    # Artistic Philosophy
    "What message do you hope people take away from your music?",
    "How do you define success as a singer?",
    "Do you believe music should always have a deeper meaning, or can it just be for fun?",
    "How do you balance commercial success with staying true to your artistry?",
    "What role do you think music plays in society?",
    "Do you think music should challenge people or comfort them?",
    "How do you feel about collaborating with other singers or musicians?",
    "What’s your opinion on the role of technology in modern music?",
    "Do you think singing is something anyone can learn, or is it innate?",
    "How do you feel about the concept of 'music for music’s sake'?",

    # Career and Industry
    "What’s the hardest part about being a singer?",
    "How do you market yourself and your music?",
    "Have you ever faced rejection in your career? How did you handle it?",
    "What’s your favorite song or project you’ve ever worked on?",
    "How do you decide on the pricing for gigs, recordings, or performances?",
    "What’s the most challenging song or performance you’ve ever done?",
    "How do you feel about social media as a tool for singers and musicians?",
    "What’s your dream collaboration?",
    "How do you balance the business side of music with the creative side?",
    "What advice would you give to aspiring singers?",

    # Fun and Personal Questions
    "What’s your favorite song to sing, and why?",
    "If you weren’t a singer, what would you be doing?",
    "What’s your favorite song by another artist?",
    "Do you collect music memorabilia or instruments?",
    "What’s your favorite concert or music venue?",
    "If you could perform in any era of music history, which would it be?",
    "What’s your favorite microphone or piece of equipment to use?",
    "Do you have any quirky habits before or during a performance?",
    "What’s the weirdest thing you’ve incorporated into a song or performance?",
    "If you could sing anywhere in the world, where would it be?",

    # Hypothetical and Imaginative Questions
    "If you could collaborate with any musician, living or dead, who would it be?",
    "If your voice had a magical power, what would it do?",
    "If you could only sing one song for the rest of your life, which would it be?",
    "If you could design a music festival, what would it look like?",
    "If one of your songs could become a movie, which one would it be?",
    "If you could teach a masterclass on singing, what would the first lesson be?",
    "If you could perform for any famous person, living or dead, who would it be?",
    "If you could only sing one genre of music for the rest of your life, what would it be?",
    "If you could have any superpower to help with your singing, what would it be?",
    "If you could perform at any event or venue in the world, what would it be?",

    # Singing and Emotions
    "How does your mood affect your singing or performances?",
    "Do you think music can heal emotional wounds?",
    "What’s the most emotional song you’ve ever performed or written?",
    "How do you express joy in your singing?",
    "How do you channel sadness or anger into your performance?",
    "Do you think music can change the way people feel?",
    "How do you handle the vulnerability of singing in front of others?",
    "What’s the most personal song you’ve ever written or performed?",
    "How do you feel when someone connects deeply with your music?",
    "Do you think music can bring people together?",

    # Artistic Challenges
    "What’s the biggest challenge you’ve faced as a singer?",
    "How do you deal with self-doubt?",
    "Have you ever felt like giving up on your music career? What kept you going?",
    "How do you handle the pressure of deadlines for songs or performances?",
    "What’s the longest time you’ve ever worked on a single song?",
    "How do you deal with perfectionism in your music?",
    "What’s the most frustrating part of the creative process?",
    "How do you handle negative feedback or reviews?",
    "Have you ever had a performance that didn’t go as planned? What did you learn from it?",
    "How do you stay inspired during tough times?",

    # Future and Legacy
    "What’s your ultimate goal as a singer?",
    "How do you want to be remembered as a musician?",
    "What’s a dream project you haven’t done yet?",
    "Where do you see your music career in 10 years?",
    "Do you think your music will outlive you?",
    "How do you want your music to impact the world?",
    "What’s the next big thing you’re working on?",
    "Do you mentor or teach other singers?",
    "How do you think the music industry will change in the future?",
    "What’s one thing you hope never changes about music?",

    # Rapid-Fire Fun Questions
    "Pop or rock?",
    "Acoustic or electric?",
    "Morning or night for singing?",
    "Sheet music or freestyle?",
    "Solo or group performances?",
    "Favorite instrument to accompany you?",
    "Favorite music genre?",
    "Favorite snack before a performance?",
    "Most-used word in your lyrics?",
    "One word to describe your music?"
]


filename = 'backend/app/data/top_artists.json'

with open(filename, 'r', encoding='utf-8') as f:
    artists = json.load(f)


artists = [artist['name'] for artist in artists]

# List of first names
first_names = [
    "Adam", "Alan", "Alex", "Alice", "Amy", "Anna", "Ben", "Beth", "Bob", "Carl",
    "Chloe", "Chris", "Clara", "Craig", "Daisy", "Dan", "David", "Dean", "Diana", "Dylan",
    "Ella", "Emily", "Eric", "Ethan", "Eva", "Eve", "Felix", "Finn", "Frank", "Fred",
    "Grace", "Hank", "Harry", "Helen", "Holly", "Hugo", "Ian", "Isaac", "Ivy", "Jack",
    "Jake", "James", "Jane", "Jason", "Jenna", "Jenny", "Jesse", "John", "Jonah", "Julie",
    "Karen", "Kevin", "Laura", "Leo", "Liam", "Lily", "Lisa", "Louis", "Lucy", "Luke",
    "Maria", "Mark", "Mason", "Max", "Mia", "Mona", "Nina", "Noah", "Nora", "Oscar",
    "Owen", "Paul", "Peter", "Robin", "Ruby", "Ryan", "Sam", "Sarah", "Scott", "Sean",
    "Simon", "Steve", "Susan", "Tara", "Theo", "Tina", "Toby", "Tony", "Tyler", "Uma",
    "Victor", "Wendy", "Will", "Wyatt", "Yara", "Zach", "Zane", "Zoe", "Abby", "April",
    "Clara", "Elsa", "Fiona", "Hazel", "Irene"
]

# List of short surnames (<6 characters)
surnames = [
    "Adams", "Allen", "Baker", "Brown", "Clark", "Davis", "Evans", "Foster", "Garcia", "Green",
    "Hall", "Harris", "Hayes", "Hill", "James", "Jones", "Kelly", "Lewis", "Lopez", "Martin",
    "Miller", "Moore", "Perez", "Reed", "Rivera", "Ross", "Scott", "Smith", "Stone", "Taylor",
    "Thomas", "Torres", "White", "Wilson", "Young", "Abbott", "Archer", "Bailey", "Blake", "Booth",
    "Boyd", "Brady", "Brock", "Bruce", "Burke", "Burns", "Casey", "Chase", "Clark", "Craig",
    "Cross", "Dean", "Doyle", "Drake", "Dunn", "Flynn", "Frost", "Grant", "Hardy", "Hayes",
    "Heath", "Henry", "Hogan", "Holt", "House", "Irwin", "James", "Johns", "Joyce", "Kane",
    "Kelly", "Knox", "Lane", "Logan", "Lynch", "Mason", "Miles", "Nash", "North", "Owen",
    "Parks", "Perry", "Price", "Quinn", "Reese", "Reid", "Riley", "Rivers", "Rowe", "Shaw",
    "Short", "Sloan", "Snow", "Stark", "Stone", "Terry", "Todd", "Trent", "Wade", "Wells",
    "Wolfe", "York", "Zane"
]

# Number of users to generate
n = 20

# Dictionary to store user data
user_data = {}

# Generate random usernames, emails, passwords, followers, and questions
for _ in range(n):
    # Randomly select a first name and a surname
    first_name = random.choice(first_names)
    surname = random.choice(surnames)
    # Create username by combining first name and surname
    username = f"{first_name}{surname}"
    # Create email and convert it to lowercase
    email = f"{username}@test.com".lower()
    # Set password
    password = "password"

    num_followed_artists = random.randint(1, 10)
    followed_artists = random.sample(artists, num_followed_artists)

    num_questions = random.randint(1, num_followed_artists)

    # Generate questions for a random subset of followed artists
    artist_questions = {}	

    for _ in range(num_questions):
        # Randomly select an artist
        artist = random.choice(followed_artists)
        artist_questions[artist] = random.choice(questions)

    # Store in dictionary
    user_data[username] = {
        "username": username,
        "email": email,
        "password": password,
        "followers": followed_artists,
        "artist_questions": artist_questions
    }

# Print the resulting dictionary
# Define the file path
file_path = "backend/app/data/user.json"

# Write the user data to the JSON file
with open(file_path, "w") as json_file:
    json.dump(user_data, json_file, indent=4)