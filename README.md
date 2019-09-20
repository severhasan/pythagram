# Pythagram

## Info

Here is the demo on heroku: [Pythagram](https://pythagram.herokuapp.com "Pythagram")
-- This is not a complete app, there is still a need for refactoring --

#### Instagram-Like App
This was initally a project that we worked together on in a Python-Django course after learning the basics. The aim here was to something similar to Instagram, but since the time was a problem, we were only able to create some features of it.

I was later able to continue improving the application and added some new features to the application along with what I have learned in the course.

For the tutorials, I have made substantial use of tutorials of [Corey MS](https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g "Corey MS") on YouTube along with official documentation and Stack Overflow posts. Since Django relies on the ease of its class features, I felt a bit restricted and this is why I had to change a lot of code for what I originally had in my mind, so instead of classes, I had to use functions.

## Features
- Users
    - have their own  profiles
    - can follow/unfollow each other
    - like/unlike a post or comment on a post
	- request a reset link for their password
- Posts
	- have likes and comments
- Comments

Because of the file management system on Heroku, I use a AWS S3 bucket for the storage of the pictures.
I integrated Sendgrid for users to get their password reset requests.
I used middlewares and codes in functions to redirect when necessary and added flash messages when necessary.

This is not the final version, so the code needs a lot of refactoring.
